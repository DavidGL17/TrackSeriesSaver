# make a post request to an url and save the response in a file

import requests
import json
from trackseriessaver.settings import username, password

BASE_URL = "https://api.trackseries.tv/v1"


def login(username: str, password: str) -> json:
    url: str = BASE_URL + "/Account/Login"
    payload = {"username": username, "password": password}
    headers = {"content-type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()


def get_series(access_token: str) -> json:
    url: str = BASE_URL + "/Follow/Series"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.json()


def get_serie(access_token: str, serie_id: int) -> json:
    url: str = f"{BASE_URL}/Follow/Series/{serie_id}/extended"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    return response.json()


def main():
    login_response = login(username, password)
    print(login_response)
    access_token = login_response["access_token"]
    series = get_series(access_token)
    # save it to json
    with open("series.json", "w") as outfile:
        json.dump(series, outfile)

    # for every series, compare the episodesNumber with the episodesWatched in the progress object, and if they are different, do smth
    for serie in series:
        if serie["progress"]["episodesNumber"] != serie["progress"]["watchedEpisodes"]:
            print(serie["id"])
            serie_id = serie["id"]
            serie = get_serie(access_token, serie_id)
            print(serie)
            with open(f"{serie_id}.json", "w") as outfile:
                json.dump(serie, outfile)
            exit()


if __name__ == "__main__":
    main()
