import { JwtPayload } from "jsonwebtoken";

declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload;
    }
  }
}

export interface CustomRequest extends Express.Request {
  headers: any;
  user?: JwtPayload;
}
