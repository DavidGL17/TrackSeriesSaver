# make a post request to an url and save the response in a file

import json
from trackseriessaver.settings import username, password


def main():
    login_response = login(username, password)
    print(login_response)
    access_token = login_response["access_token"]
    series = get_series(access_token)
    print(len(series))
    # save it to json
    with open("data/series.json", "w") as outfile:
        json.dump(series, outfile)


if __name__ == "__main__":
    main()
