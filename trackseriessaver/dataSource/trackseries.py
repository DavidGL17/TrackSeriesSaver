import requests
import json
from trackseriessaver.entities import Serie, Season, Episode
from trackseriessaver.settings import image_path

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


def processEpisodes(episodes: json, imgPath: str) -> list(Episode):
    episodes: list(Episode) = []
    for episode in episodes:
        serieId: int = episode["serieId"]
        id: int = episode["id"]
        directors: list(str) = episode["directors"]
        title: str = episode["title"]
        number: int = episode["number"]
        seasonNumber: int = episode["seasonNumber"]
        overview: str = episode["overview"].encode("utf-8").decode("utf-8")
        image: str = episode["image"]
        watched: bool = episode["watched"]
        imdbId: str = episode["ids"]["imdbId"]
        tvdbId: int = episode["ids"]["tvdbId"]
        # get the image from the url
        img = requests.get(image)
        # save it to a file
        with open(f"{imgPath}/{number}.jpg", "wb") as f:
            f.write(img.content)
        image = f"{imgPath}/{number}.jpg"
        episodes.append(
            Episode(
                serieId=serieId,
                id=id,
                directors=directors,
                title=title,
                number=number,
                seasonNumber=seasonNumber,
                overview=overview,
                image=image,
                watched=watched,
                imdbId=imdbId,
                tvdbId=tvdbId,
            )
        )
    return episodes


def processSeasons(seasons: json, imagePath: str) -> list(Season):
    for season in seasons:
        number: int = season["number"]
        posterImage: str = season["posterImage"]
        numEpisodes: int = season["progress"]["numEpisodes"]
        numEpisodesWatched: int = season["progress"]["numEpisodesWatched"]
        episodes: list(Episode) = processEpisodes(season["episodes"], imagePath)
        seasons.append(
            Season(
                number=number,
                posterImage=posterImage,
                numEpisodes=numEpisodes,
                numEpisodesWatched=numEpisodesWatched,
                episodes=episodes,
            )
        )


def processSerie(serie: json) -> Serie:
    id: int = serie["id"]
    name: str = serie["name"]
    numEpisodes: int = serie["numEpisodes"]
    numEpisodesWatched: int = serie["numEpisodesWatched"]
    numSeasons: int = serie["numSeasons"]
    overview: str = serie["overview"]
    imdbId: str = serie["imdbId"]
    tvdbId: int = serie["tvdbId"]
    posterImage: str = serie["posterImage"]
    bannerImage: str = serie["bannerImage"]
    fanartImage: str = serie["fanartImage"]
    status: str = serie["status"]
    imagePath = image_path + "/" + str(id)
    seasons: list(Season) = processSeasons(serie["seasons"], imagePath)
    return Serie(
        id=id,
        name=name,
        numEpisodes=numEpisodes,
        numEpisodesWatched=numEpisodesWatched,
        numSeasons=numSeasons,
        overview=overview,
        imdbId=imdbId,
        tvdbId=tvdbId,
        posterImage=posterImage,
        bannerImage=bannerImage,
        fanartImage=fanartImage,
        status=status,
        seasons=seasons,
    )
