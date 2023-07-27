import winston from "winston";

// Set up Winston logger
const logger = winston.createLogger({
  level: "info", // Set the minimum log level to be recorded
  format: winston.format.combine(
    winston.format.timestamp(), // Add timestamp to log entries
    winston.format.json(), // Log entries in JSON format for better parsing
  ),
  transports: [
    new winston.transports.Console(), // Log to the console (you can add more transports here if needed)
    new winston.transports.File({ filename: "error.log", level: "error" }), // Log errors to a file
    new winston.transports.File({ filename: "combined.log" }), // Log all other entries to another file
  ],
});

export { logger };
