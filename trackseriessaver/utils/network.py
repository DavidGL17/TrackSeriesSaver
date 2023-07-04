import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from requests.models import Response
import time

# Create a session
session = requests.Session()

# Set the number of retries
retries = 3
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)


def get_url(url: str, headers={}) -> Response:
    """
    A function that returns the content of a url

    :param url: the url to get the content from

    :return: the content of the url
    """
    while True:
        try:
            # Make the request
            response = session.get(url, headers=headers)
            return response
        except ConnectionError as e:
            print(f"Connection error occurred: {e}")
            time.sleep(1)
