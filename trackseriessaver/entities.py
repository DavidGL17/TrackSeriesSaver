from dataclasses import dataclass


@dataclass
class Episode:
    serieId: int
    id: int
    directors: list(str)
    title: str
    number: int
    seasonNumber: int
    overview: str
    image: str
    watched: bool
    imdbId: str
    tvdbId: int


@dataclass
class Season:
    number: int
    posterImage: str
    numEpisodes: int
    numEpisodesWatched: int
    episodes: list(Episode)


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
    seasons: list(Season)
