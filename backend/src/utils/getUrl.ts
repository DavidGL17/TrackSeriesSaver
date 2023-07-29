import axios, { AxiosInstance } from "axios";
import { logger } from "./logger";

// Create a session with Axios
const session: AxiosInstance = axios.create();

// Define the function signature for the Response object
interface Response {
  data: any;
  status: number;
  statusText: string;
  headers: any;
  config: any;
}

async function getURL(url: string, headers: any = {}): Promise<Response> {
  /**
   * A function that returns the content of a url
   *
   * @param url - the url to get the content from
   *
   * @return the content of the url
   */

  while (true) {
    try {
      // Make the request
      const response: Response = await session.get(url, { headers });
      return response;
    } catch (e) {
      if (axios.isAxiosError(e)) {
        // Extract the error message
        const errorMessage = e.message;

        logger.error(`Connection error occurred: ${errorMessage}`);
        await new Promise((resolve) => setTimeout(resolve, 1000));
      } else {
        // Re-throw the error if it's not an AxiosError
        throw e;
      }
    }
  }
}

export { getURL };
