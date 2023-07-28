import { Document, Schema, Model, model } from "mongoose";

interface IEpisode extends Document {
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

interface ISeason extends Document {
  number: number;
  posterImage: string;
  numEpisodes: number;
  numEpisodesWatched: number;
  episodes: IEpisode[];
}

interface ISerie extends Document {
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
  seasons: ISeason[];
}

const EpisodeSchema: Schema<IEpisode> = new Schema({
  serieId: { type: Number, required: true },
  id: { type: Number, required: true, unique: true },
  directors: { type: [String], required: true },
  title: { type: String, required: true },
  number: { type: Number, required: true },
  seasonNumber: { type: Number, required: true },
  overview: { type: String, required: true },
  image: { type: String, required: true },
  watched: { type: Boolean, required: true },
  imdbId: { type: String, required: true },
  tvdbId: { type: Number, required: true },
  airDate: { type: String, required: true },
});

const SeasonSchema: Schema<ISeason> = new Schema({
  number: { type: Number, required: true },
  posterImage: { type: String, required: true },
  numEpisodes: { type: Number, required: true },
  numEpisodesWatched: { type: Number, required: true },
  episodes: [EpisodeSchema],
});

const SerieSchema: Schema<ISerie> = new Schema({
  id: { type: Number, required: true, unique: true },
  name: { type: String, required: true },
  numEpisodes: { type: Number, required: true },
  numEpisodesWatched: { type: Number, required: true },
  numSeasons: { type: Number, required: true },
  overview: { type: String, required: true },
  imdbId: { type: String, required: true },
  tvdbId: { type: Number, required: true },
  posterImage: { type: String, required: true },
  bannerImage: { type: String, required: true },
  fanartImage: { type: String, required: true },
  status: { type: String, required: true },
  seasons: [SeasonSchema],
});

const Serie: Model<ISerie> = model<ISerie>("Serie", SerieSchema);

export { Serie, ISerie, ISeason, IEpisode };
