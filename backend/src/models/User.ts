// a user model, that contains a username, password, and a list of series
import { Document, Schema, Model, model } from "mongoose";
import { ISerie } from "./Serie";

interface IUser extends Document {
  username: string;
  password: string;
  series: ISerie[];
}

const UserSchema: Schema<IUser> = new Schema({
  username: { type: String, required: true, unique: true },
  password: { type: String, required: false },
  series: [{ type: Schema.Types.ObjectId, ref: "Serie" }],
});

const User: Model<IUser> = model("User", UserSchema);

export { IUser, User };
