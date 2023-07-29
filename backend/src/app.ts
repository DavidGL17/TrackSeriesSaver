import express from "express";
import cors from "cors";
import morgan from "morgan";
import { app } from "./routes";
import { logger } from "./utils/logger";
import mongoose from "mongoose";
import dotenv from "dotenv";
import { ensureDefaultUser } from "./models/User";

const mainApp = express();

// Use the login middleware
mainApp.use(express.json()); // Parse JSON request bodies
mainApp.use(cors()); // Enable CORS
mainApp.use(app);

// Set up Morgan to log HTTP requests
app.use(
  morgan("combined", { stream: { write: (message) => logger.info(message) } }),
);

const dbURI = "mongodb://localhost:27019/data_storage";

mongoose
  .connect(dbURI, {
    // @ts-ignore
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    logger.info("Connected to MongoDB");
  })
  .catch((error) => {
    logger.error(error);
    process.exit(1);
  });

// init dotenv
dotenv.config();

// Ensure we have a default user
ensureDefaultUser();

// Start the server
mainApp.listen(3001, "0.0.0.0", () => {
  logger.info("Server started at http://localhost:3001");
});
