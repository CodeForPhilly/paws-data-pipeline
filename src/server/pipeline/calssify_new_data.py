import pandas as pd
from flask import current_app


def venn_diagram_join(df1, df2):
    # Calculates the join between two dataframes like a Venn diagram
    #
    # Join criteria is all columns in common between them.
    # Returns which rows are rows are only present in the left, which overlap,
    # and which are only on the right table.
    #
    # An evolution of earlier work from match_data.join_on_all_columns
    venn_indicator = '_merge'  # temporary column name for designating the match type
    join_results = df1.merge(df2, how='outer', indicator=venn_indicator)
    return (
        join_results[join_results[venn_indicator] == 'left_only'].drop(columns=venn_indicator),
        join_results[join_results[venn_indicator] == 'both'].drop(columns=venn_indicator),
        join_results[join_results[venn_indicator] == 'right_only'].drop(columns=venn_indicator)
    )


def filter_rows_by_ids(df, ids):
    assert "source_id" in ids and "source_type" in ids and len(ids.columns) == 2
    return df.merge(ids, how="inner")  # rows in df with the expected id


def start(pdp_contacts_df, normalized_data):
    current_app.logger.info("Starting classification of rows")
    current_app.logger.info(" - {} rows in incoming data and {} in existing pdp_contacts".format(
        normalized_data.shape[0], pdp_contacts_df.shape[0]
    ))
    result = {
        "new": pd.DataFrame(columns=pdp_contacts_df.columns),
        "updated": pd.DataFrame(columns=pdp_contacts_df.columns),
        "old": pd.DataFrame(columns=pdp_contacts_df.columns)
    }

    incoming_ids = normalized_data[["source_id", "source_type"]].drop_duplicates()
    existing_ids = pdp_contacts_df[["source_id", "source_type"]].drop_duplicates()
    #probably need a smarter method of dropping duplicates, e.g. row with least amount of null values
    normalized_data = normalized_data.drop_duplicates(["source_id", "source_type"])
    new_ids, reused_ids, old_ids = venn_diagram_join(incoming_ids, existing_ids)
    current_app.logger.info(" - ID's identified as {} new, {} reused, and {} old".format(
        new_ids.shape[0], reused_ids.shape[0], old_ids.shape[0]
    ))

    # Process updated results
    incoming_reused_rows = filter_rows_by_ids(normalized_data, reused_ids)
    existing_reused_rows = filter_rows_by_ids(pdp_contacts_df, reused_ids)
    fresh_rows, unchanged_rows, old_version_rows = venn_diagram_join(incoming_reused_rows, existing_reused_rows)
    # We don't need to consider unchanged rows, since we've already recorded that data and matching.
    result["updated"] = fresh_rows
    result["old"] = pd.concat([filter_rows_by_ids(pdp_contacts_df, old_ids), unchanged_rows])
    # could also consider adding old_version_rows to result["old"]
    result["new"] = filter_rows_by_ids(normalized_data, new_ids)

    current_app.logger.info(
        " - Classified {} new rows and {} updated rows in the normalized data"
        .format(result["new"].shape[0], result["updated"].shape[0])
    )

    return result
