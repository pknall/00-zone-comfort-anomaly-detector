from unittest import TestCase
from pk.utils.postgres.Tools import Tools as PSQL_Tools
from datetime import timedelta

class TestTools(TestCase):
    def test_get_connection(self):
        # self.pass()
        pass

    '''
    Remember to add the client's IP address to pg_hba.conf
    '''
    def test_real_connection(self):
        psql_tools = PSQL_Tools()
        try:
            conn = psql_tools.get_connection()
            conn.close()
        except Exception as e:
            print(e)

    def test_execute_read_only_query(self):
        psql_tools = PSQL_Tools()
        uuid = "uuid_0c194706_eadb_466d_801a_0551eb62f4b9"
        sql = f"""SELECT ts FROM {uuid} ORDER BY ts DESC LIMIT 1;"""
        last_record = psql_tools.execute_read_only_query(sql)

        # The above query returns a list of tuples, the [0][0] selects the first item of the first tuple
        # ...which should be the only result

        last_date = last_record[0][0]
        print(f"\nResults: {last_date}")
        print(f"\nResults: {type(last_date)}")
        last_date += timedelta(minutes=1)
        print(f"\nResults: {last_date}")