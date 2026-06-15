# This is a sample Python script.
from numpy.testing.print_coercion_tables import print_new_cast_table

from pk.utils.postgres.Tools import Tools as PSQL_Tools
import pandas as pd

SITE_TABLE_NAME = "site_metadata"
ROOM_TABLE_NAME = "room_metadata"
TREND_TABLE_NAME = "trend_metadata"

TARGET_TREND_DOMAIN_NAMES = ('desiredTempCooling', 'desiredTempHeating', 'currentTemp')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    psql_tools = PSQL_Tools()

    # Get a list of Sites.  Until more sites are populated only Canal Park Stadium is used.
    site_ref = "20a474cf-1eb8-405b-af54-6a5d059dafcf"   # Canal Park Stadium

    # Get a list of rooms from that site ###############################################################################
    room_query_string = f"SELECT id FROM {ROOM_TABLE_NAME} WHERE siteref = '{site_ref}'"
    room_results = psql_tools.execute_read_only_query(room_query_string)
    rooms_df = pd.DataFrame(room_results)
    rooms_df.to_csv("csv\\a_rooms.csv", index=False)

    # Get a list of trends from that room ##############################################################################
    for room_id in rooms_df[0]:
        # Get the desired trend ids from the room and package them in a DataFrame
        trend_query_string = f"SELECT id,domainname FROM {TREND_TABLE_NAME} WHERE roomref = '{room_id}' and domainname in {TARGET_TREND_DOMAIN_NAMES};"
        trend_results = psql_tools.execute_read_only_query(trend_query_string)
        trend_list_df = pd.DataFrame(trend_results)

        # If nothing was returned → SKIP
        if trend_list_df.shape[0] <= 1:
            print(f"Trending room: {room_id} is empty")
            continue

        # Initialize trend search variables
        today = pd.Timestamp.today().normalize()
        start = today - pd.Timedelta(days=1)
        end = today
        merged = pd.DataFrame()
        first = True

        # Retrieve the trends and merge into one dataframe on "ts"
        for trend_id, trend_name in zip(trend_list_df[0], trend_list_df[1]):
            trend_data = psql_tools.get_trend_data_with_uuid(trend_id, start ,end)
            if first:
                first = False
                merged = trend_data
            else:
                merged = merged.merge(trend_data, on="ts", how="outer")
            last_name = merged.columns[-1]
            merged.rename(columns={last_name: trend_name}, inplace=True)
            merged[trend_name] = merged[trend_name].astype(float)

        merged.to_csv("csv\\merged.csv")

    # Get a trend values from those trends for some period #############################################################


        break   # run once