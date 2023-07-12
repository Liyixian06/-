from connect_db import connect_create_tables as cct
def insert_sql():
    need = cct.connect_mysql()
    cur = need[0]
    conn = need[1]