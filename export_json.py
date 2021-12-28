import json
import psycopg2


username = 'postgres'
password = 'postgres'
database = 'lab2'
host = 'localhost'
port = '5432'

OUTPUT_FILE_JSON = 'pobiedimska_DB_{}.json'

TABLES = [
    'houses',
    'neighbourhoods',
    'sales'
]

con = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)


data = {}
with con:
    cur = con.cursor()

    for table in TABLES:
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]
        for row in cur:
            rows.append(dict(zip(fields, row)))
        data[table] = rows


with open(OUTPUT_FILE_JSON, 'w') as outf:
    json.dump(data, outf, default=str)
