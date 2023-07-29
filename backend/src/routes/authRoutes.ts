import express, { Request, Response } from "express";
import { User } from "../models/User";
import { generateToken } from "../middleware/loginMiddleware";
import { logger } from "../utils/logger";

const authRouter = express.Router();
const baseAuthPath: string = "/auth";

// Middleware to handle login requests
authRouter.post(
  "/login",
  async (req: Request, res: Response): Promise<void> => {
    logger.info("POST request to " + baseAuthPath + "/login");
    try {
      const { username, password } = req.body;

      // Find the user in the database
      const user = await User.findOne({ username });

      if (!user) {
        res.status(401).json({ error: "Invalid credentials" });
        return;
      }

      // Compare the provided password with the given password (compare two strings)
      const passwordMatch = password === user.password;

      if (!passwordMatch) {
        res.status(401).json({ error: "Invalid credentials" });
        return;
      }

      // If the login is successful, generate a JWT token
      const token = generateToken({ username });

      // Send the token as a response with the user information
      res.json({
        token,
        user: { username },
      });
    } catch (error) {
      console.error("Error logging in:", error);
      res.status(500).json({ error: "Internal server error" });
    }
  },
);

export { authRouter, baseAuthPath };
