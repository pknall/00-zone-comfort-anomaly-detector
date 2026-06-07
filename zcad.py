# This is a sample Python script.
from numpy.testing.print_coercion_tables import print_new_cast_table

from pk.utils.postgres.Tools import Tools as PSQL_Tools
import pandas as pd

SITE_TABLE_NAME = "site_metadata"
ROOM_TABLE_NAME = "room_metadata"
TREND_TABLE_NAME = "trend_metadata"

TARGET_TREND_DOMAIN_NAMES = ('desiredCoolingTemp', 'desiredHeatingTemp', 'currentTemp')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    psql_tools = PSQL_Tools()
    # Get a list of Sites.  Until more sites are populated only Canal Park Stadium is used.
    site_ref = "20a474cf-1eb8-405b-af54-6a5d059dafcf"   # Canal Park Stadium

    # Get a list of rooms from that site ###############################################################################
    room_query_string = f"SELECT * FROM {ROOM_TABLE_NAME} WHERE siteref = '{site_ref}'"
    # print(room_query_string)
    room_results = psql_tools.execute_read_only_query(room_query_string)
    # print(room_results)
    rooms_df = pd.DataFrame(room_results)
    # print(rooms_df)

    # Get a list of trends from that room ##############################################################################
    for room_id in rooms_df[0]:
        # print(room_id)
        trend_query_string = f"SELECT * FROM {TREND_TABLE_NAME} WHERE roomref = '{room_id}' and domainname in {TARGET_TREND_DOMAIN_NAMES};"
        print(trend_query_string)
        trend_results = psql_tools.execute_read_only_query(trend_query_string)
        trend_df = pd.DataFrame(trend_results)
        for trend_id in trend_df[0]:
            print(trend_id)

    # Get a trend values from those trends for some period #############################################################


        break   # run once