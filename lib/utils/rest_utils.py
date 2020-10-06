import requests
import json

def download_json(url):
    """
    Retrieve a document or it's summary from the database
    :param url: the base url of the REST server + document or summary
    :returns response.text: document or it's summary is returned if successful
    """
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)
    elif response.status_code == 404:
        return "Not Found"
    else:
        return response.status_code