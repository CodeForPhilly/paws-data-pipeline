import pandas as pd
from flask import current_app

"""
def determine_update(df):
    print(1)


def remove_y_strip_x(df):
    columns_to_remove = [c for c in df.columns if c.endswith("$y")]
    df = df[df.columns.drop(columns_to_remove)]

    df = df.rename(lambda x: x[:-2] if x.endswith("$x") else x, axis=1)
    df = df.drop(columns=["_indication", "_id"])

    return df
"""

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
    print("TEMP: INCOMING DTYPES: {}".format(normalized_data.dtypes))
    print("TEMP: EXISTING DTYPES: {}".format(pdp_contacts_df.dtypes))

    # TODO: @urirot should verify that the old TODO is fixed (todo - seems to not return what's expected on update)
    incoming_ids = normalized_data[["source_id", "source_type"]].drop_duplicates()
    existing_ids = pdp_contacts_df[["source_id", "source_type"]].drop_duplicates()
    new_ids, reused_ids, old_ids = venn_diagram_join(incoming_ids, existing_ids)
    print("TEMP: NUMBER OF UNIQUE INCOMING AND EXISTING IDs: {}, {}".format(incoming_ids.shape[0], existing_ids.shape[0]))
    print("TEMP: IDs IDENTIFIED AS {}, {}, {}".format(new_ids.shape[0], reused_ids.shape[0], old_ids.shape[0]))

    result["new"] = filter_rows_by_ids(normalized_data, new_ids)
    result["old"] = filter_rows_by_ids(pdp_contacts_df, old_ids)

    # Process updated results
    incoming_reused_rows = filter_rows_by_ids(normalized_data, reused_ids)
    existing_reused_rows = filter_rows_by_ids(pdp_contacts_df, reused_ids)
    fresh_rows, unchanged_rows, old_version_rows = venn_diagram_join(incoming_reused_rows, existing_reused_rows)
    # We don't need to consider unchanged rows, since we've already recorded that data and matching
    result["updated"] = fresh_rows
    # TODO: ADDING UNCHANGES ROWS BACK TO "OLD", PERHAPS WITH AN APPEND OF SOME SORT

    current_app.logger.info(
        " - Classified {} new rows and {} updated rows in the normalized data"
        .format(result["new"].shape[0], result["updated"].shape[0])
    )


    """
    partial_merge = normalized_data.merge(pdp_contacts_df, how="outer", indicator="_indication",
                                          left_on=["source_id", "source_type"], right_on=["source_id", "source_type"])

    result["new"] = partial_merge[partial_merge["_indication"] == "left_only"]
    # strips suffix that was used for merge
    result["new"] = remove_y_strip_x(result["new"])

    overlapping_rows = partial_merge[partial_merge["_indication"] == "both"]

    # todo: find rows that were changed and add them. strip $x or $y
    result["updated"] = determine_update(overlapping_rows)

    # todo: when removing a row from the existing data, an entry should be found here - should invetigate why it's being added the "new" instead
    # todo: remove y strip $y
    result["old"] = partial_merge[partial_merge["_indication"] == "right_only"]
    """

    return result
