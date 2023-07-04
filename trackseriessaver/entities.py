from dataclasses import dataclass
from json import JSONEncoder


@dataclass
class Episode:
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

    def __eq__(self, other) -> bool:
        if not isinstance(other, Episode):
            print(f"not an episode: {type(other)}")
            return False
        if self.serieId != other.serieId:
            print(f"serieId: {self.serieId} != {other.serieId}")
            return False
        if self.id != other.id:
            print(f"id: {self.id} != {other.id}")
            return False
        if self.directors != other.directors:
            print(f"directors: {self.directors} != {other.directors}")
            return False
        if self.title != other.title:
            print(f"title: {self.title} != {other.title}")
            return False
        if self.number != other.number:
            print(f"number: {self.number} != {other.number}")
            return False
        if self.seasonNumber != other.seasonNumber:
            print(f"seasonNumber: {self.seasonNumber} != {other.seasonNumber}")
            return False
        if self.overview != other.overview:
            print(f"overview: {self.overview} != {other.overview}")
            return False
        if self.image != other.image:
            print(f"image: {self.image} != {other.image}")
            return False
        if self.watched != other.watched:
            print(f"watched: {self.watched} != {other.watched}")
            return False
        if self.imdbId != other.imdbId:
            print(f"imdbId: {self.imdbId} != {other.imdbId}")
            return False
        if self.tvdbId != other.tvdbId:
            print(f"tvdbId: {self.tvdbId} != {other.tvdbId}")
            return False
        if self.airDate != other.airDate:
            print(f"airDate: {self.airDate} != {other.airDate}")
            return False
        return True


@dataclass
class Season:
    number: int
    posterImage: str
    numEpisodes: int
    numEpisodesWatched: int
    episodes: list[Episode]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Season):
            print(f"not a season: {type(other)}")
            return False
        if self.number != other.number:
            print(f"number: {self.number} != {other.number}")
            return False
        if self.posterImage != other.posterImage:
            print(f"posterImage: {self.posterImage} != {other.posterImage}")
            return False
        if self.numEpisodes != other.numEpisodes:
            print(f"numEpisodes: {self.numEpisodes} != {other.numEpisodes}")
            return False
        if self.numEpisodesWatched != other.numEpisodesWatched:
            print(f"numEpisodesWatched: {self.numEpisodesWatched} != {other.numEpisodesWatched}")
            return False
        for thisEpisode, otherEpisode in zip(self.episodes, other.episodes):
            if not thisEpisode.__eq__(otherEpisode):
                return False
        return True


@dataclass
class Serie:
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

    # define the equality operator
    def __eq__(self, other) -> bool:
        if not isinstance(other, Serie):
            print("nope")
            return False
        if self.id != other.id:
            print(f"id: {self.id} != {other.id}")
            return False
        if self.name != other.name:
            print(f"name: {self.name} != {other.name}")
            return False
        if self.numEpisodes != other.numEpisodes:
            print(f"numEpisodes: {self.numEpisodes} != {other.numEpisodes}")
            return False
        if self.numEpisodesWatched != other.numEpisodesWatched:
            print(f"numEpisodesWatched: {self.numEpisodesWatched} != {other.numEpisodesWatched}")
            return False
        if self.numSeasons != other.numSeasons:
            print(f"numSeasons: {self.numSeasons} != {other.numSeasons}")
            return False
        if self.overview != other.overview:
            print(f"overview: {self.overview} != {other.overview}")
            return False
        if self.imdbId != other.imdbId:
            print(f"imdbId: {self.imdbId} != {other.imdbId}")
            return False
        if self.tvdbId != other.tvdbId:
            print(f"tvdbId: {self.tvdbId} != {other.tvdbId}")
            return False
        if self.posterImage != other.posterImage:
            print(f"posterImage: {self.posterImage} != {other.posterImage}")
            return False
        if self.bannerImage != other.bannerImage:
            print(f"bannerImage: {self.bannerImage} != {other.bannerImage}")
            return False
        if self.fanartImage != other.fanartImage:
            print(f"fanartImage: {self.fanartImage} != {other.fanartImage}")
            return False
        if self.status != other.status:
            print(f"status: {self.status} != {other.status}")
            return False
        for thisSeason, otherSeason in zip(self.seasons, other.seasons):
            if not thisSeason.__eq__(otherSeason):
                return False
        return True


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
