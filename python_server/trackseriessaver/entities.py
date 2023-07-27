from dataclasses import dataclass
from json import JSONEncoder
from persistent import Persistent


@dataclass
class Episode(Persistent):
    """
    The episode of a serie.

    Attributes:
        serieId (int): The id of the serie.
        id (int): The id of the episode.
        directors (list[str]): The directors of the episode.
        title (str): The title of the episode.
        number (int): The number of the episode.
        seasonNumber (int): The number of the season.
        overview (str): The overview of the episode.
        image (str): The image of the episode.
        watched (bool): Whether the episode is watched.
        imdbId (str): The imdb id of the episode.
        tvdbId (int): The tvdb id of the episode.
        airDate (str): The air date of the episode.
    """

    serieId: int
    id: int
    directors: list[str]
    title: str
    number: int
    seasonNumber: int
    overview: str
    image: str
    watched: bool
    imdbId: str
    tvdbId: int
    airDate: str


@dataclass
class Season(Persistent):
    """
    The season of a serie.

    Attributes:
        number (int): The number of the season.
        posterImage (str): The poster image of the season.
        numEpisodes (int): The number of episodes of the season.
        numEpisodesWatched (int): The number of episodes watched of the season.
        episodes (list[Episode]): The episodes of the season.
    """

    number: int
    posterImage: str
    numEpisodes: int
    numEpisodesWatched: int
    episodes: list[Episode]


@dataclass
class Serie(Persistent):
    """
    The serie.

    Attributes:
        id (int): The id of the serie.
        name (str): The name of the serie.
        numEpisodes (int): The number of episodes of the serie.
        numEpisodesWatched (int): The number of episodes watched of the serie.
        numSeasons (int): The number of seasons of the serie.
        overview (str): The overview of the serie.
        imdbId (str): The imdb id of the serie.
        tvdbId (int): The tvdb id of the serie.
        posterImage (str): The poster image of the serie.
        bannerImage (str): The banner image of the serie.
        fanartImage (str): The fanart image of the serie.
        status (str): The status of the serie.
        seasons (list[Season]): The seasons of the serie.
    """

    id: int
    name: str
    numEpisodes: int
    numEpisodesWatched: int
    numSeasons: int
    overview: str
    imdbId: str
    tvdbId: int
    posterImage: str
    bannerImage: str
    fanartImage: str
    status: str
    seasons: list[Season]


class SerieEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Serie):
            # handle the case where the object Serie contains a list of Seasons
            seasons = []
            for season in o.seasons:
                # handle the case where the object Season contains a list of Episodes
                episodes = []
                for episode in season.episodes:
                    episodes.append(episode.__dict__)
                season.episodes = episodes
                seasons.append(season.__dict__)
            o.seasons = seasons
            return o.__dict__


def decodeSerie(jsonContent: dict) -> Serie:
    # take the json and convert it to a Serie object
    # handle the case where the json contains a list of Seasons
    seasons = []
    for season in jsonContent["seasons"]:
        # handle the case where the json contains a list of Episodes
        episodes = []
        for episode in season["episodes"]:
            episodes.append(Episode(**episode))
        season["episodes"] = episodes
        seasons.append(Season(**season))
    jsonContent["seasons"] = seasons
    return Serie(**jsonContent)
