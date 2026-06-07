import os
import psycopg2
from psycopg2 import sql

class Tools:

    def __init__(self):
        pass

    '''
    Generator a connection to PostgreSQL database using environment variables.  This code does not handle the
    exception if the connection fails.  
    '''
    def get_connection(self):
        return psycopg2.connect(
            host = os.environ.get("POSTGRES_HOST"),
            database = os.environ.get("POSTGRES_DATABASE"),
            user = os.environ.get("POSTGRES_USERNAME"),
            password = os.environ.get("POSTGRES_PASSWORD"),
            port = os.environ.get("POSTGRES_PORT")
        )

    '''
    Add a table to the database if it doesn't already exist.  Include any default columns specific to the table.
    '''
    def add_table_if_not_exists(self, table_name, include_columns):
        conn = self.get_connection()

        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {include_columns}
        )
        """

        with conn.cursor() as cur:
            cur.execute(create_table_sql)

        conn.commit()
        conn.close()

    '''
    Add a column to a table if it doesn't already exists.
    '''
    def add_column_to_table_if_not_exists(self, table_name, column_to_add, column_data_type):
        # print(f"Adding column {column_to_add} to table {table_name}")
        conn = self.get_connection()

        with conn.cursor() as cur:
            cur.execute(sql.SQL(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_to_add} {column_data_type}"))
        conn.commit()
        conn.close()

    def add_data_to_table(self, table_name, data_to_add):
        conn = self.get_connection()
        # print (data_to_add)

        columns = data_to_add.keys()
        values = data_to_add.values()

        sql = f"""
        INSERT INTO {table_name} ({','.join(columns)})
        VALUES ({','.join(['%s'] * len(columns))})
        ON CONFLICT (id) DO NOTHING
        """
        # sql = sql.lower()  # Facilisight isn't terribly consistent about capitalization of the column names
        # print(sql)

        with conn.cursor() as cur:
            cur.execute(sql, list(values))

        conn.commit()
        conn.close()

    def import_trend_data(self, table_name, rows):
        conn = self.get_connection()
        sql = f"""INSERT INTO {table_name} (ts, val) 
        VALUES (%(ts)s, %(val)s) 
        ON CONFLICT (ts) DO NOTHING
        """

        with conn.cursor() as cur:
            cur.executemany(sql, rows)
        conn.commit()
        conn.close()

    def execute_read_only_query(self, query):
        conn = self.get_connection()
        results = None
        with conn.cursor() as curr:
            curr.execute(query)
            results = curr.fetchall()

        curr.close()
        conn.close()
        return results