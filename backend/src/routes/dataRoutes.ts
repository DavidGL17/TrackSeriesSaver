import { logger } from "../utils/logger";
import express, { Request, Response } from "express";
import { User } from "../models/User";
import { Serie } from "../models/Serie";
import { authenticateToken } from "../middleware/loginMiddleware";

const dataRouter = express.Router();
const baseDataPath: string = "/data";

dataRouter.get(
  "/",
  authenticateToken,
  async (req: Request, res: Response): Promise<void> => {
    logger.info("GET request to " + baseDataPath + "/");
    try {
      const { username } = req.user;
      const user = await User.findOne({ username });

      if (user) {
        // Retrieve the serieIds from the user's series array
        const serieIds = user.series;

        // Retrieve the Serie documents using the serieIds
        const series = await Serie.find({ _id: { $in: serieIds } }).exec();

        // Assign the populated series to the user's series property
        res.status(200).json({ series });
      } else {
        res.status(401).send("Invalid username or password");
      }
    } catch (error) {
      logger.error("Error in GET /: " + error);
      res.status(500).send("Internal server error");
    }
  },
);

export { dataRouter, baseDataPath };
