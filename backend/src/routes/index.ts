import express from "express";
import { baseDataPath, dataRouter } from "./dataRoutes";
import { authRouter, baseAuthPath } from "./authRoutes";

const app = express();

app.use(express.json());

app.use(baseAuthPath, authRouter);
app.use(baseDataPath, dataRouter);

export { app };
