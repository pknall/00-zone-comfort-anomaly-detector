import os
import requests
import re
import json
from pk.apis.seventyfivef.ReadyByFIlter import ReadByFilter as read

class API:

    def __init__(self):
        """
        Frequently used functions for the seventyfivef Platforms.
        :param username: Facilisight Username
        :param password: Facilisight Password
        :param subscription_key: Platforms Key from seventyfivef Platforms Management portal
        """
        self.username = os.environ.get("75F API Username")
        self.password = os.environ.get("75F API Password")
        self.subscription_key = os.environ.get("75F API Subscription Key")
        self.authorization_key = self.get_authorization(self.username, self.password, self.subscription_key)

    """
    Retrieves historical data from the 75F API using "POST hisReadMany".  It is up to the caller to format the ids
    and date range correctly:

    Examples of Data format (Note: "id" and the subsequent list of ids must be on their own line with no extra whitespace).
        date-time range: ver:"3.0" range:"2020-01-01T12:00:00-04:00 New_York,2020-01-03T00:00:00-04:00 New_York" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
        date range: ver:"3.0" range:"2020-01-01,2020-01-07" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
        date: ver:"3.0" range:"2020-01-01" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
        latest: ver:"3.0" range:"latest" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
        today: ver:"3.0" range:"today" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
        yesterday: ver:"3.0" range:"yesterday" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418

    Args:
        ids (list): A list of ids to retrieve historical data for (see README.md)
        date_range (string): The date range to pull historical data for

    Returns:
        results (dict):
    """
    def get_trend_records(self, id, date_range):
        url = "https://api.75f.io/haystack/hisReadMany"
        hdr ={
            'Authorization': self.authorization_key,
            'Accept': 'application/json',
            'Content-Type': 'text/zinc',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }
        id = "\n@" + id
        data = f"ver:\"3.0\" range:\"{date_range}\"\nid\n{id}"
        try:
            response = requests.post(url, data=data, headers=hdr, timeout=30)
            return json.loads(response.text)
        except Exception as e:
            print(f"""Exception during SeventyFiveF.hisReadMany.post(): {e}
            id: {id}
            date_range: {date_range}
            """)


    def get_json_by_filter(self, query_string):
        """
        Retrieves data from the 75F Platform and stores it in a JSON object.
        :param query_string: A Haystack Query to select the desired data.
        :return: JSON object with the data returned from the Platforms.
        :exception: Raises exception for caller to handle
        """
        try:
            return read().get_query(query_string, self.subscription_key, self.authorization_key)
        except Exception as e:
            raise Exception(f"Error during get_df_by_filter(\'{query_string}\': {e}")

    def get_authorization(self, username, password, subscription_key):
        """
        Retrieves the Authorization Key using the username, password, and subscription key.  Prepends 'Bearer '
        to the Authorization Code per the 75F documentation.
        Args:
            username (string):  The Facilisight username that has Platforms privileges
            password (string):  The password for the above username
            subscription_key (string): The subscription key for the above username from the 75F Platforms website

        Returns:
            Authorization Key (string): The authorization code from the 75F Platforms for use during future requests.
            Returns an empty string ("") if an Authorization Key is not returned.
        """

        url = "https://api.75f.io/oauth/token"

        hdr = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': subscription_key
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": username,
            "client_secret": password
        }

        try:
            response = requests.post(url, data=data, headers=hdr, timeout=15)
        except Exception as e:
            raise Exception(
                f"Exception while requesting Authentication Key in get_authorization():\n{e}")

        matches = re.findall(r'"(.*?)"', response.text)
        if (matches is None) or (len(matches) == 0):
            raise Exception(
                f"Exception while retrieving Authentication Key from Response:  No Matches found in response.")
        elif len(matches) < 2:
            raise Exception(f"Exception while retrieving Authentication Key from Response: Only one field returned: ")
        elif len(matches) >= 2:
            if len(matches[1]) < 855:
                raise Exception(f"Authorization Key is not 855 characters: {len(matches[1])} : {matches[1]}")
            authorization_string = 'Bearer ' + matches[1]
        else:
            raise Exception(f"Unknown error in SeventyFiveF_Auth.get_authorization().")

        return authorization_string