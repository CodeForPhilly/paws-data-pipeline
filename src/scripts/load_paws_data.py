import pandas as pd
import re
import os
import datetime

from datasource_manager import DATASOURCE_MAPPING
from config import engine
from flask import current_app
from config import CURRENT_SOURCE_FILES_PATH
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

meta = MetaData(engine, reflect=True)
if not engine.dialect.has_table(engine, 'petpoint'):
    Table('petpoint', meta,
          Column('animal_num', String),
          Column('outcome_person_num', String),
          Column('outcome_person_name', String),
          Column('out_street_address', String),
          Column('out_unit_number', Integer),
          Column('out_city', String),
          Column('out_province', String),
          Column('out_postal_code', String),
          Column('out_email', String),
          Column('out_home_phone', String),
          Column('out_cell_phone', String),
          Column('json', JSONB),
          Column('created_date', DateTime),
          Column('archived_date', DateTime)
          )
    Table('volgistics', meta,
          Column('number', String),
          Column('last_name', String),
          Column('first_name', String),
          Column('middle_name', String),
          Column('complete_address', String),
          Column('street_1', String),
          Column('street_2', String),
          Column('street_3', String),
          Column('city', String),
          Column('state', String),
          Column('zip', String),
          Column('all_phone_numbers', String),
          Column('home', String),
          Column('work', String),
          Column('cell', String),
          Column('email', String),
          Column('json', JSONB),
          Column('created_date', DateTime),
          Column('archived_date', DateTime)
          )
    Table('salesforcecontacts', meta,
          Column('contact_id', String),
          Column('first_name', String),
          Column('last_name', String),
          Column('mailing_street', String),
          Column('mailing_city', String),
          Column('mailing_state_province', String),
          Column('mailing_zip_postal_code', String),
          Column('phone', String),
          Column('mobile', String),
          Column('email', String),
          Column('json', JSONB),
          Column('created_date', DateTime),
          Column('archived_date', DateTime)
          )
    meta.create_all(engine)


def start(file_path_list, should_drop_first_col=False):
    result = {
        "new_rows": {},
        "updated_rows": {}
    }

    for uploaded_file in file_path_list:
        file_path = os.path.join(CURRENT_SOURCE_FILES_PATH, uploaded_file)
        table_name = file_path.split('/')[-1].split('-')[0]

        current_app.logger.info('running load_paws_data on: ' + uploaded_file)

        df = pd.read_csv(file_path, encoding='cp1252')
        df = __clean_raw_data(df, should_drop_first_col)
        df.to_sql(table_name + '_stage', engine, index=False, if_exists='replace')
        current_app.logger.info('looking for new rows ')
        __find_new_rows(result, table_name)
        # __find_updated_rows(result, table_name)
        current_app.logger.info('   - finish load_paws_data on: ' + uploaded_file)

    return result


def __find_new_rows(result, table_name):
    source_id = DATASOURCE_MAPPING[table_name]['id']
    current_app.logger.info(table_name + ' ' + source_id)
    with engine.connect() as conn:
        # find new rows
        rows = conn.execute(
            'select t.* from {} t left join {} v on v."{}" = t."{}" where v."{}" is null'.format(
                table_name + "_stage", table_name, source_id, source_id, source_id))

        rows_data = []
        now = datetime.now()
        tracked_columns = DATASOURCE_MAPPING[table_name]['tracked_columns']

        for row in rows:
            row_dict = {}
            json_dict = {}

            for key_value in row.items():
                if key_value[0] in tracked_columns:
                    if key_value[0] == DATASOURCE_MAPPING['volgistics']['id']:
                        row_dict[key_value[0]] = str(key_value[1])
                    else:
                        row_dict[key_value[0]] = key_value[1]
                json_dict[key_value[0]] = key_value[1]

            row_dict['json'] = json_dict
            row_dict['created_date'] = now
            rows_data.append(row_dict)

        result['new_rows'][table_name] = rows_data
        ins = meta.tables[table_name].insert()
        conn.execute(ins, rows_data)


def __find_updated_rows(found_rows, table_name):
    table_name_temp = table_name + '_temp'
    primary_key = DATASOURCE_MAPPING[table_name]['id']
    tracked_columns = DATASOURCE_MAPPING[table_name]['tracked_columns']
    tracked_column_str = ''
    for column in tracked_columns:
        tracked_column_str += '"' + column + '", '
    tracked_column_str = tracked_column_str[:-2]

    with engine.connect() as connection:
        # find updated rows
        updated_query = '''
            select * from {} where "{}" in (
                select "{}" from (
                    select {} 
                    from {} t 
                    where exists (select 1 from {} c where c."{}" = t."{}" and c.deleted_date is null)
                    except 
                    select {} 
                    from {} where deleted_date is null
            	) a
        )
        '''.format(table_name_temp, primary_key, primary_key, tracked_column_str, table_name_temp, table_name,
                   primary_key, primary_key, tracked_column_str, table_name)
        rows = connection.execute(updated_query)
        row_data = []
        for row in rows:
            row_data.append(row.items())
        updates = {table_name: row_data}
        found_rows['updated_rows'] = updates

        # mark old version of updated rows as deleted
        mark_deleted = '''
        update {} set deleted_date = now() where "{}" in (
	        select "{}" from (
			    select {}
			    from {} t 
			    where exists (select 1 from {} c where c."{}" = t."{}" and c.deleted_date is null)
			    except 
			    select {}
			    from {} where deleted_date is null
	        ) a
        ) and deleted_date is null
        '''.format(table_name, primary_key, primary_key, tracked_column_str, table_name_temp, table_name, primary_key,
                   primary_key, tracked_column_str, table_name)
        connection.execute(mark_deleted)

        # insert new updated rows


def __create_table(df, engine, table_name):
    result = engine.dialect.has_table(engine, table_name)

    if not result:
        df['created_date'] = datetime.datetime.now()
        df['deleted_date'] = None
        df.to_sql(table_name, engine, index=False)

    return result


def __clean_raw_data(df, should_drop_first_col):
    # drop the first column - so far all csvs have had a first column that's an index and doesn't have a name
    if should_drop_first_col:
        df = df.drop(df.columns[0], axis=1)

    # strip whitespace and periods from headers, convert to lowercase
    df.columns = df.columns.str.lower().str.strip()
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('#', 'num')
    df.columns = df.columns.str.replace('/', '_')
    df.columns = df.columns.map(lambda x: re.sub(r'\.+', '_', x))

    return df
