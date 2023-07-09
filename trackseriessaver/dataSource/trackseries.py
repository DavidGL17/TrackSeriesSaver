import requests
import json
import os
import time
import transaction
from persistent.dict import PersistentDict
import concurrent.futures

from ..entities import Serie, Season, Episode, SerieEncoder
from ..utils.network import get_url
from ..database import zodb
from ..utils.logger import logger
from ..utils.config import num_threads

BASE_URL = "https://api.trackseries.tv/v1"


def threaded_save_serie(access_token: str, id: int, image_path: str, name: str) -> Serie:
    """
    A threaded function to optimize the saving of the series

    Args:
        access_token (str): the access token of the user
        id (int): the id of the serie
        image_path (str): the path to the image folder

    Returns:
        Serie: the serie related to the id as given by the processSerie function
    """
    logger.info(f"Processing serie : {name}")
    return processSerie(get_serie(access_token, id), image_path)


def save_series(username: str, password: str, image_path: str):
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

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        start = time.time()
        futures = []
        for serie in series:
            id: int = serie["id"]
            future = executor.submit(threaded_save_serie, access_token, id, image_path, serie["name"])
            futures.append(future)

        for future, serie in zip(futures, series):
            processedSerie: Serie = future.result()
            id: int = serie["id"]
            zodb.dbroot["app_data"][username][id] = processedSerie
        transaction.commit()
        end = time.time()
        logger.info(f"Processing took {end - start} seconds")

    # print the first 5 series in the database into a json file
    for serie in list(zodb.dbroot["app_data"][username].values())[:5]:
        with open(f"tmp_data/{serie.id}.json", "w") as f:
            json.dump(serie, f, indent=4, cls=SerieEncoder)


def login(username: str, password: str) -> dict:
    """
    Login to the trackseries api. Returns a dict with the access_token and more info on the user

    Args:
        username (str): the username of the user
        password (str): the password of the user

    Returns:
        dict: a dict with the access_token and more info on the user. If the login failed, the dict will contain an error message under the key "message"
    """
    url: str = BASE_URL + "/Account/Login"
    payload = {"username": username, "password": password}
    headers = {"content-type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()


def get_series(access_token: str) -> list[dict]:
    """
    Get all the series the user is following

    Args:
        access_token (str): the access_token of the user

    Returns:
        list[dict]: a list of dicts with the info of the series the user is following
    """
    url: str = BASE_URL + "/Follow/Series"
    headers = {"Authorization": "Bearer " + access_token}
    response = get_url(url, headers=headers)
    return response.json()


def get_serie(access_token: str, serie_id: int) -> dict:
    """
    Get the info of a specific serie

    Args:
        access_token (str): the access_token of the user
        serie_id (int): the id of the serie

    Returns:
        dict: a list with the info of the serie, including the seasons and episodes with detailed info
    """
    url: str = f"{BASE_URL}/Follow/Series/{serie_id}/extended"
    headers = {"Authorization": "Bearer " + access_token}
    response = get_url(url, headers=headers)
    return response.json()


def save_image(url: str, path: str) -> None:
    """
    Save an image from a url to a file

    Args:
        url (str): the url of the image
        path (str): the path to save the image to
    """
    # if the image already exists, don't download it again
    if os.path.exists(path):
        return
    # get the image from the url
    img = get_url(url)
    # save it to a file
    with open(path, "wb") as f:
        f.write(img.content)


def processEpisodes(episodes: list[dict], imgPath: str) -> list[Episode]:
    result: list[Episode] = []
    for episode in episodes:
        serieId: int = episode["serieId"]
        id: int = episode["id"]
        directors: list[str] = episode["directors"]
        title: str = episode["title"]
        number: int = episode["number"]
        seasonNumber: int = episode["seasonNumber"]
        if episode["overview"] is None:
            overview: str = ""
        else:
            overview: str = episode["overview"].encode("utf-8").decode("utf-8")
        image: str = episode["image"]
        watched: bool = episode["watched"]
        imdbId: str = episode["ids"]["imdb"]
        tvdbId: int = episode["ids"]["tvdb"]
        airDate: str = episode["firstAired"]
        save_image(image, f"{imgPath}/{number}.jpg")
        image: str = f"{imgPath}/{number}.jpg"
        result.append(
            Episode(
                serieId=serieId,
                id=id,
                directors=directors,
                title=title,
                number=number,
                seasonNumber=seasonNumber,
                overview=overview,
                image=f"{imgPath}/{number}.jpg",
                watched=watched,
                imdbId=imdbId,
                tvdbId=tvdbId,
                airDate=airDate,
            )
        )
    return result


def processSeasons(seasons: list[dict], imagePath: str) -> list[Season]:
    result: list[Season] = []
    for season in seasons:
        number: int = season["seasonNumber"]
        # make the directory, if it doesn't exist
        seasonPath = imagePath + "/" + str(number)
        if not os.path.exists(seasonPath):
            os.mkdir(seasonPath)
        posterImage: str = season["poster"]
        save_image(posterImage, f"{seasonPath}/season{number}Poster.jpg")
        numEpisodes: int = season["progress"]["numEpisodes"]
        numEpisodesWatched: int = season["progress"]["numEpisodesWatched"]
        episodes: list[Episode] = processEpisodes(season["episodes"], seasonPath)
        result.append(
            Season(
                number=number,
                posterImage=f"{seasonPath}/season{number}Poster.jpg",
                numEpisodes=numEpisodes,
                numEpisodesWatched=numEpisodesWatched,
                episodes=episodes,
            )
        )
    return result


def processSerie(serie: dict, baseImagePath: str) -> Serie:
    id: int = serie["id"]
    name: str = serie["name"]
    numEpisodes: int = serie["progress"]["numEpisodes"]
    numEpisodesWatched: int = serie["progress"]["numEpisodesWatched"]
    numSeasons: int = len(serie["seasons"])
    overview: str = serie["overview"]
    imdbId: str = serie["imdbId"]
    tvdbId: int = serie["tvdbId"]
    posterImage: str = serie["images"]["poster"]
    bannerImage: str = serie["images"]["banner"]
    fanartImage: str = serie["images"]["fanart"]
    imagePath = baseImagePath + "/" + str(id)
    # make the directory, if it doesn't exist
    if not os.path.exists(imagePath):
        os.mkdir(imagePath)
    for img, fileName in [
        (posterImage, f"posterImage_{id}"),
        (bannerImage, f"bannerImage_{id}"),
        (fanartImage, f"fanartImage_{id}"),
    ]:
        save_image(img, f"{imagePath}/{fileName}.jpg")
    status: str = serie["status"]
    seasons: list[Season] = processSeasons(serie["seasons"], imagePath)
    return Serie(
        id=id,
        name=name,
        numEpisodes=numEpisodes,
        numEpisodesWatched=numEpisodesWatched,
        numSeasons=numSeasons,
        overview=overview,
        imdbId=imdbId,
        tvdbId=tvdbId,
        posterImage=f"{imagePath}/posterImage_{id}.jpg",
        bannerImage=f"{imagePath}/bannerImage_{id}.jpg",
        fanartImage=f"{imagePath}/fanartImage_{id}.jpg",
        status=status,
        seasons=seasons,
    )
