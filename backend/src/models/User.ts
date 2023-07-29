// a user model, that contains a username, password, and a list of series
import { Document, Schema, Model, model } from "mongoose";
import { Serie } from "./Serie";
import { logger } from "../utils/logger";
import { saveSeries } from "../api/trackseries";

interface IUser extends Document {
  username: string;
  password: string;
  series: (typeof Serie)[];
}

const UserSchema: Schema<IUser> = new Schema({
  username: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  series: [{ type: Schema.Types.ObjectId, ref: "Serie" }],
});

const User: Model<IUser> = model<IUser>("User", UserSchema);

async function createUser(username: string, password: string) {
  // creates a user and fetches the series

  await User.create({
    username,
    password,
    series: [],
  });
  const imagePath: string = process.env.IMAGE_PATH || "images";
  await saveSeries(username, password, imagePath);
}

// Function to ensure the default user exists
async function ensureDefaultUser() {
  try {
    // Load the default user information from environment variables
    const defaultUsername = process.env.DEFAULT_USER_USERNAME;
    const defaultPassword = process.env.DEFAULT_USER_PASSWORD;
    const existingUser = await User.findOne({ username: defaultUsername });

    if (!existingUser) {
      logger.info("Creating default user");
      createUser(defaultUsername, defaultPassword);
    }
  } catch (error) {
    console.error("Error ensuring default user:", error);
  }
}

export { IUser, User, ensureDefaultUser };
