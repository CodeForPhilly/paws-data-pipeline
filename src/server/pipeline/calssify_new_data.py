import pandas as pd
import re
import os
import io
import datetime

from datasource_manager import DATASOURCE_MAPPING, SOURCE_NORMALIZATION_MAPPING
from flask import current_app
from config import CURRENT_SOURCE_FILES_PATH
from datetime import datetime
from models import Base


def start(pdp_contacts_df, normalized_data):
    result = {
        "new": pd.DataFrame(columns=pdp_contacts_df.columns),
        "updated": pd.DataFrame(columns=pdp_contacts_df.columns)
    }

    partial_merge = normalized_data.merge(pdp_contacts_df, how="outer", indicator="_indication",
                                          left_on=["source_id", "source_type"], right_on=["source_id", "source_type"])

    result["new"] = partial_merge[partial_merge["_indication"] == "left_only"]



    # overlapping_rows = partial_merge[partial_merge["_indication"] == "both"]
    # old_only_rows = partial_merge[partial_merge["_indication"] == "left_only"]

    return result


def __find_updated_rows(connection, found_rows, table_name):
    table_name_temp = table_name + '_stage'
    primary_key = DATASOURCE_MAPPING[table_name]['id']
    tracked_columns = DATASOURCE_MAPPING[table_name]['tracked_columns']
    tracked_column_str = ''
    for column in tracked_columns:
        tracked_column_str += '"' + column + '", '
    tracked_column_str = tracked_column_str[:-2]

    # find updated rows
    updated_query = '''
        select * from {} where "{}" in (
            select "{}" from (
                select {} 
                from {} t 
                where exists (select 1 from {} c where c."{}" = t."{}" and c.archived_date is null)
                except 
                select {} 
                from {} where archived_date is null
            ) a
    )
    '''.format(table_name_temp, primary_key, primary_key, tracked_column_str, table_name_temp, table_name,
               primary_key, primary_key, tracked_column_str, table_name)
    rows = connection.execute(updated_query)
    row_data = __create_row_dicts(rows, tracked_columns)

    if row_data:
        updates = {table_name: row_data}
        found_rows['updated_rows'] = updates

    # mark old version of updated rows as archived
    mark_deleted = '''
    update {} set archived_date = now() where "{}" in (
        select "{}" from (
            select {}
            from {} t 
            where exists (select 1 from {} c where c."{}" = t."{}" and c.archived_date is null)
            except 
            select {}
            from {} where archived_date is null
        ) a
    ) and archived_date is null
    '''.format(table_name, primary_key, primary_key, tracked_column_str, table_name_temp, table_name, primary_key,
               primary_key, tracked_column_str, table_name)
    connection.execute(mark_deleted)

    # insert new updated rows ....eeek that's confusing
    ins = Base.metadata.tables[table_name].insert()
    connection.execute(ins, row_data)


def __create_row_dicts(rows, tracked_columns):
    rows_data = []
    now = datetime.now()
    for row in rows:
        row_dict = {}
        json_dict = {}
        for key_value in row.items():
            if key_value[0] in tracked_columns:
                row_dict[key_value[0]] = key_value[1]
            json_dict[key_value[0]] = key_value[1]
        row_dict['json'] = json_dict
        row_dict['created_date'] = now
        rows_data.append(row_dict)
    return rows_data
