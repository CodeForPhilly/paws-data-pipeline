import pandas as pd


def determine_update(df):
    print(1)


def remove_y_strip_x(df):
    columns_to_remove = [c for c in df.columns if c.endswith("$y")]
    df = df[df.columns.drop(columns_to_remove)]

    df = df.rename(lambda x: x[:-2] if x.endswith("$x") else x, axis=1)
    df = df.drop(columns=["_indication", "_id"])

    return df


def start(pdp_contacts_df, normalized_data):
    result = {
        "new": pd.DataFrame(columns=pdp_contacts_df.columns),
        "updated": pd.DataFrame(columns=pdp_contacts_df.columns),
        "old": pd.DataFrame(columns=pdp_contacts_df.columns)
    }

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

    return result
