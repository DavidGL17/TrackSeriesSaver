from trackseriessaver.dataSource.trackseries import login, get_series, get_serie, processSerie
from trackseriessaver.entities import Serie
from trackseriessaver.config import username, password, image_path
from trackseriessaver.database import zodb
import transaction
import json
import os
import time
from persistent.dict import PersistentDict


def save_series():
    """
    A function that saves the series the user is following to a json file in the database, along with the images of the series
    """
    access_token: str = login(username, password)["access_token"]
    series = get_series(access_token)

    # prepare the folders
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    # prepare the database
    if username not in zodb.dbroot["app_data"]:
        zodb.dbroot["app_data"][username] = PersistentDict()

    start = time.time()
    for serie in series:
        print(f"Processing serie : {serie['name']}")
        id: int = serie["id"]
        processedSerie: Serie = processSerie(get_serie(access_token, id), image_path)
        zodb.dbroot["app_data"][username][id] = processedSerie
        transaction.commit()
    end = time.time()
    print(f"Processing took {end - start} seconds")

    # print the first 5 series in the database into a json file
    for serie in list(zodb.dbroot["app_data"][username].values())[:5]:
        with open(f"tmp_data/{serie.id}.json", "w") as f:
            json.dump(serie, f, indent=4)


def main():
    save_series()


if __name__ == "__main__":
    main()
