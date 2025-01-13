import { Schema, model } from "mongoose";

const accountSchema = new Schema({
  accountId: { type: Number },
// @generation**
});

export default model("Accounts", accountSchema);
