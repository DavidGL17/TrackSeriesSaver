import express from "express";
import { dataRouter } from "./dataRoute";

const app = express();

app.use(express.json());

app.use("/data", dataRouter);

export { app };
