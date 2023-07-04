import requests
import json
import os
from trackseriessaver.entities import Serie, Season, Episode

BASE_URL = "https://api.trackseries.tv/v1"


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
    response = requests.get(url, headers=headers)
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
    response = requests.get(url, headers=headers)
    return response.json()


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
        # get the image from the url
        img = requests.get(image)
        # save it to a file
        with open(f"{imgPath}/{number}.jpg", "wb") as f:
            f.write(img.content)
        image = f"{imgPath}/{number}.jpg"
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
        posterImage: str = season["poster"]
        img = requests.get(posterImage)
        seasonPath = imagePath + "/" + str(number)
        # make the directory, if it doesn't exist
        if not os.path.exists(seasonPath):
            os.mkdir(seasonPath)
        # save it to a file
        with open(f"{seasonPath}/season{number}Poster.jpg", "wb") as f:
            f.write(img.content)
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
        # get the image from the url
        img = requests.get(img)
        # save it to a file
        with open(f"{imagePath}/{fileName}.jpg", "wb") as f:
            f.write(img.content)
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
