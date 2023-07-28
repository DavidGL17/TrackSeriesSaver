import { logger } from "../utils/logger";
import express, { Request, Response } from "express";
import { User } from "../models/User";

const dataRouter = express.Router();

dataRouter.get("/", async (req: Request, res: Response): Promise<void> => {
  logger.info("GET /");
  try {
    const username = req.body;
    const password = req.body;

    const user = await User.findOne({ username, password }).populate("series");

    if (user) {
      res.status(200).json(user.series);
    } else {
      res.status(401).send("Invalid username or password");
    }
  } catch (error) {
    logger.error("Error in GET /: " + error);
    res.status(500).send("Internal server error");
  }
});

export { dataRouter };
