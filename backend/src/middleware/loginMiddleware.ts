import jwt, { JwtPayload, VerifyErrors } from "jsonwebtoken";
import { Response, NextFunction } from "express";
import { CustomRequest } from "../types/custom";

// Middleware to verify JWT token
const authenticateToken = (
  req: CustomRequest,
  res: Response,
  next: NextFunction,
): void => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(" ")[1];

  if (!token) {
    res.sendStatus(401); // Unauthorized
    return;
  }

  new Promise<void>((resolve, reject) => {
    jwt.verify(
      token,
      "your-secret-key",
      (err: VerifyErrors | null, data: JwtPayload | undefined) => {
        if (err) {
          reject(err);
          return;
        }

        if (!data) {
          reject(new Error("Invalid token"));
          return;
        }

        const user = data;

        // If the token is valid, save the user object in the request for further use
        req.user = user as JwtPayload;

        resolve();
      },
    );
  })
    .then(() => {
      // Call the next middleware
      next();
    })
    .catch(() => {
      res.sendStatus(403); // Forbidden
    });
};

// Helper function to generate JWT token
function generateToken(user: JwtPayload): string {
  const token = jwt.sign(user, "your-secret-key");
  return token;
}

export { authenticateToken, generateToken };
