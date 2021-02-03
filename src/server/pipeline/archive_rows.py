
def archive(pdp_db, updated_rows):
    for index, row in updated_rows.iterrows():
        source_type = row["source_type"]
        source_id = row["source_id"]

        mark_deleted = '''update pdp_contacts set archived_date = now() \
         where source_type like '{}' and \
         source_id like '{}' and archived_date is null'''.format(source_type, source_id)

        pdp_db.execute(mark_deleted)
