import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_query(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"instance/database.db"
    sql_query1 = """ DROP TABLE cars"""
    conn = create_connection(database)
    sql_query2 = """ CREATE TABLE cars (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    name text NOT NULL,
                    price text,
                    brand text,
                    type text,
                    year text,
                    km text,
                    fuell text,
                    gearbox text
                ); """

    # create tables
    if conn is not None:
        execute_query(conn, sql_query1)
        execute_query(conn, sql_query2)
    else:
        print("Error! cannot create the database connection.")


def insert_data(conn, project):
    sql = '''INSERT INTO cars(name, price, brand, type, year, km, fuell, gearbox)
              VALUES(?,?,?,?,?,?,?,?);'''
    cur = conn.cursor()
    cur.executemany(sql, project)
    conn.commit()
    return cur.lastrowid


if __name__ == '__main__':
    main()