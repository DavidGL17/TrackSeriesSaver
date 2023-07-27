import express from "express";
import cors from "cors";
import morgan from "morgan";
import { app } from "./routes";
import { logger } from "./utils/logger";

const mainApp = express();

// Use the login middleware
mainApp.use(express.json()); // Parse JSON request bodies
mainApp.use(cors()); // Enable CORS
mainApp.use(app);

// Set up Morgan to log HTTP requests
app.use(
  morgan("combined", { stream: { write: (message) => logger.info(message) } }),
);

// // Protected route that requires authentication
// mainApp.get("/protected", authenticateToken, (req, res) => {
//   // Access the authenticated user object
//   const { username } = req.user;

//   // Return a response
//   res.send(`Welcome, ${username}! You've accessed the protected route.`);
// });

// Start the server
mainApp.listen(3002, "0.0.0.0", () => {
  console.log("Server is running on port 3002");
});
