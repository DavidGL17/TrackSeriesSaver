import { getURL } from "../utils/getUrl";
import { logger } from "../utils/logger";
import fs from "fs";
import {
  Serie,
  Season,
  Episode,
  IEpisode,
  ISeason,
  ISerie,
} from "../models/Serie";
import { User } from "../models/User";

const baseUrl: string = "https://api.trackseries.tv/v1";

async function threadedSaveSerie(
  accessToken: string,
  id: number,
  imagePath: string,
  name: string,
): Promise<ISerie> {
  /**
   * A threaded function to optimize the saving of the series
   *
   * @param access_token - the access token of the user
   * @param id - the id of the serie
   * @param image_path - the path to the image folder
   *
   * @return the serie related to the id as given by the processSerie function
   */

  logger.info(`Processing serie : ${name}`);
  return processSerie(await getSerie(accessToken, id), imagePath);
}

async function saveSeries(
  username: string,
  password: string,
  imagePath: string,
) {
  /**
   * A function that saves the series the user is following to a json file in the database, along with the images of the series
   *
   * @param username - the username of the user
   * @param password - the password of the user
   * @param image_path - the path to the image folder
   *
   * @return void
   *
   * @throws an error if the login failed
   *
   * @sideeffect saves the series to the database
   * @sideeffect saves the images of the series to the database
   * @sideeffect creates a folder for the images if it doesn't exist yet
   *
   **/
  const accessToken: string = login(username, password)["access_token"];
  const series = await getSeries(accessToken);

  // prepare the folders
  if (!fs.existsSync(imagePath)) {
    fs.mkdirSync(imagePath);
  }

  // start the processing
  const promises: Promise<ISerie>[] = [];
  for (const serie of series) {
    const id: number = serie.id;
    promises.push(threadedSaveSerie(accessToken, id, imagePath, serie.name));
  }
  const processedSeries: ISerie[] = await Promise.all(promises);

  // Saving series to the database
  const user = await User.findOne({ username }); // Find the user by username
  if (!user) {
    console.error("User not found.");
    return;
  }

  for (const processedSerie of processedSeries) {
    const serie = await Serie.findOne({ id: processedSerie.id }); // Find the serie by id
    // Add the saved serie to the user's series list
    user.series.push(serie._id); // Assuming that the Serie model returns an object with the _id field
  }
  await user.save(); // Save the user to the database

  logger.info("Finished saving series for user: " + username);
}

async function login(username: string, password: string): Promise<any> {
  /**
   * Login to the trackseries api. Returns a dict with the access_token and more info on the user
   *
   * @param username - the username of the user
   * @param password - the password of the user
   *
   * @return a dict with the access_token and more info on the user. If the login failed, the dict will contain an error message under the key "message"
   */

  const url: string = baseUrl + "/Account/Login";
  const payload = { username, password };
  const headers = { "content-type": "application/json" };
  fetch(url, {
    method: "POST",
    body: JSON.stringify(payload),
    headers,
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      return data;
    })
    .catch((error) => {
      logger.error(`Error in login: ${error}`);
    });
}

async function getSeries(accessToken: string): Promise<any> {
  /**
   * Get all the series the user is following
   *
   * @param access_token - the access_token of the user
   *
   * @return a list of dicts with the info of the series the user is following
   */

  const url: string = baseUrl + "/Follow/Series";
  const headers = { Authorization: "Bearer " + accessToken };
  const response = await getURL(url, headers);
  return response.data;
}

async function getSerie(accessToken: string, serieId: number): Promise<any> {
  /**
   * Get the info of a specific serie
   *
   * @param access_token - the access_token of the user
   * @param serie_id - the id of the serie
   *
   * @return a list with the info of the serie, including the seasons and episodes with detailed info
   */

  const url: string = baseUrl + "/Follow/Series/" + serieId + "/extended";
  const headers = { Authorization: "Bearer " + accessToken };
  const response = await getURL(url, headers);
  return response.data;
}

async function saveImage(url: string, filePath: string): Promise<void> {
  if (fs.existsSync(filePath)) {
    return;
  }
  const response = await getURL(url);
  fs.writeFileSync(filePath, response.data);
}

interface IEpisodeRaw {
  serieId: number;
  id: number;
  directors: string[];
  title: string;
  number: number;
  seasonNumber: number;
  overview: string;
  firstAired: string;
  image: string;
  watched: boolean;
  ids: {
    imdb: string;
    tvdb: number;
  };
}

async function processEpisodes(
  episodes: IEpisodeRaw[],
  imgPath: string,
): Promise<IEpisode[]> {
  const result: IEpisode[] = [];
  for (const episode of episodes) {
    const serieId: number = episode.serieId;
    const id: number = episode.id;
    const directors: string[] = episode.directors;
    const title: string = episode.title;
    const number: number = episode.number;
    const seasonNumber: number = episode.seasonNumber;
    const overview: string = episode.overview;
    const image: string = episode.image;
    const watched: boolean = episode.watched;
    const imdbId: string = episode.ids.imdb;
    const tvdbId: number = episode.ids.tvdb;
    const airDate: string = episode.firstAired;
    await saveImage(image, `${imgPath}/${number}.jpg`);
    const res = await Episode.create({
      serieId,
      id,
      directors,
      title,
      number,
      seasonNumber,
      overview,
      image: `${imgPath}/${number}.jpg`,
      watched,
      imdbId,
      tvdbId,
      airDate,
    });
    result.push(res);
  }
  return result;
}

interface ISeasonRaw {
  seasonNumber: number;
  poster: string;
  progress: {
    numEpisodes: number;
    numEpisodesWatched: number;
    numEpisodesAired: number;
    numEpisodesUnseen: number;
  };
  episodes: IEpisodeRaw[];
}

async function processSeasons(
  seasons: ISeasonRaw[],
  imagePath: string,
): Promise<ISeason[]> {
  const result: ISeason[] = [];
  for (const season of seasons) {
    const number: number = season.seasonNumber;
    // make the directory, if it doesn't exist
    const seasonPath = imagePath + "/" + String(number);
    if (!fs.existsSync(seasonPath)) {
      fs.mkdirSync(seasonPath);
    }
    const posterImage: string = season.poster;
    await saveImage(posterImage, `${seasonPath}/season${number}Poster.jpg`);
    const numEpisodes: number = season.progress.numEpisodes;
    const numEpisodesWatched: number = season.progress.numEpisodesWatched;
    const episodes: IEpisode[] = await processEpisodes(
      season.episodes,
      seasonPath,
    );
    const res = await Season.create({
      number,
      posterImage: `${seasonPath}/season${number}Poster.jpg`,
      numEpisodes,
      numEpisodesWatched,
      episodes,
    });
    result.push(res);
  }
  return result;
}

interface ISerieRaw {
  id: number;
  name: string;
  progress: {
    numEpisodes: number;
    numEpisodesWatched: number;
    numEpisodesAired: number;
    numEpisodesUnseen: number;
  };
  followers: number;
  firstAired: string;
  country: string;
  overview: string;
  runtime: number;
  status: string;
  network: string;
  airDay: string;
  airTime: string;
  contentRating: string;
  imdbId: string;
  tvdbId: number;
  language: string;
  images: {
    poster: string;
    fanart: string;
    banner: string;
  };
  seasons: ISeasonRaw[];
}

async function processSerie(
  serie: ISerieRaw,
  baseImagePath: string,
): Promise<ISerie> {
  const id: number = serie.id;
  const name: string = serie.name;
  const numEpisodes: number = serie.progress.numEpisodes;
  const numEpisodesWatched: number = serie.progress.numEpisodesWatched;
  const overview: string = serie.overview;
  const imdbId: string = serie.imdbId;
  const tvdbId: number = serie.tvdbId;
  const posterImage: string = serie.images.poster;
  const fanartImage: string = serie.images.fanart;
  const bannerImage: string = serie.images.banner;
  // make the directory, if it doesn't exist
  const imagePath = baseImagePath + "/" + String(id);
  if (!fs.existsSync(imagePath)) {
    fs.mkdirSync(imagePath);
  }
  await saveImage(posterImage, `${imagePath}/poster.jpg`);
  await saveImage(fanartImage, `${imagePath}/fanart.jpg`);
  await saveImage(bannerImage, `${imagePath}/banner.jpg`);
  const seasons: ISeason[] = await processSeasons(serie.seasons, imagePath);
  const result = await Serie.create({
    id,
    name,
    numEpisodes,
    numEpisodesWatched,
    numSeasons: seasons.length,
    overview,
    imdbId,
    tvdbId,
    posterImage: `${imagePath}/poster.jpg`,
    fanartImage: `${imagePath}/fanart.jpg`,
    bannerImage: `${imagePath}/banner.jpg`,
    seasons,
  });
  return result;
}

export { saveSeries };
