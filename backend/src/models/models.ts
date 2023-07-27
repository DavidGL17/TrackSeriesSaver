interface Episode {
  serieId: number;
  id: number;
  directors: string[];
  title: string;
  number: number;
  seasonNumber: number;
  overview: string;
  image: string;
  watched: boolean;
  imdbId: string;
  tvdbId: number;
  airDate: string;
}

interface Season {
  number: number;
  posterImage: string;
  numEpisodes: number;
  numEpisodesWatched: number;
  episodes: Episode[];
}

interface Serie {
  id: number;
  name: string;
  numEpisodes: number;
  numEpisodesWatched: number;
  numSeasons: number;
  overview: string;
  imdbId: string;
  tvdbId: number;
  posterImage: string;
  bannerImage: string;
  fanartImage: string;
  status: string;
  seasons: Season[];
}

export { Episode, Season, Serie };
