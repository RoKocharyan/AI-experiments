import { Schema, model } from "mongoose";

const accountSchema = new Schema({
  accountId: { type: Number },
// @generation**
  onboardingLink: { type: String },
  status: { type: String },
});

export default model("Accounts", accountSchema);
