import requests
import json

class Read:
    def __init__(self):
        self.url = "https://api.75f.io/haystack/read"

    def get_query(self, read_argument, subscription_key, authorization_key):
        self.hdr = {
            'Authorization': authorization_key,
            'Accept': 'application/json',
            'Content-Type': 'text/zinc',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': subscription_key,
        }
        data = self.get_body(read_argument)
        try:
            response = requests.post(self.url, data=data, headers=self.hdr, timeout=30)
            return json.loads(response.text)
        except Exception as e:
            raise Exception(f"""Exception during read(): {e}
            Argument: {read_argument}
            """)

    def get_body(self, read_argument):
        raise Exception("Read should not be used directly.  Use one of the 'ReadyBy' children instead.")