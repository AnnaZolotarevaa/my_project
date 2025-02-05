import psycopg2
from psycopg2 import sql

db_user = 'postgres'  
db_password = '1234'
owner = 'postgres'
db_host = 'localhost'
db_port = '5432'  
new_db_name = 'transport_db'  

conn = psycopg2.connect(
    dbname='postgres',
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

conn.autocommit = True
cur = conn.cursor()
cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))

cur.execute(sql.SQL("ALTER DATABASE {} OWNER TO {}").format(
    sql.Identifier(new_db_name),
    sql.Identifier(owner)
))
cur.close()
conn.close()
print(f"База данных '{new_db_name}' успешно создана и владельцем установлено '{owner}'.")
