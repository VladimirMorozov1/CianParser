from cian_parser import parser
import psycopg2
from psycopg2.extras import Json
import datetime


today_date = datetime.date.today().strftime("%d%m%Y")

conn = psycopg2.connect(database = "cian") # name of DB is here
cur = conn.cursor()
#conn.rollback()

try:
    cur.execute(f"CREATE TABLE data{today_date} (id SERIAL PRIMARY KEY, link VARCHAR(256), name VARCHAR(256), address VARCHAR(2048), main_attributes JSON, description VARCHAR(8192), additional_attributes JSON, house_attributes JSON)")
    conn.commit()
    print('TABLE HAS BEEN CREATED')
except psycopg2.errors.DuplicateTable:
    print("TABLE ALREADY EXISTS")


for page_num in range(1,2731):
    links = parser.collect_links(page_num, page_num+1)

    for link in links:
        data = parser.collect_flat_data(link)
        print(data)
        with conn:
            with conn.cursor() as curs:
                curs.execute(f"INSERT INTO data{today_date} (link, name, address, main_attributes, description, additional_attributes, house_attributes) VALUES ('{data['Link']}','{data['Name']}','{data['Address']}',{Json(data['Main_attributes'])},'{data['Description']}',{Json(data['Additional_attributes'])},{Json(data['House_attributes'])})")
                conn.commit()
