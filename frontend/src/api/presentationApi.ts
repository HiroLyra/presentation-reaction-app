import axios from "axios";
import type {
  AddReactionRequest,
  AddReactionResponse,
  CreatePresentationRequest,
  CreatePresentationResponse,
  GetPresentationResponse,
  ReactionType,
} from "../types/presentation";
const api = axios.create({
  baseURL: "https://presentation-reaction-api.onrender.com",
  timeout: 30000,
});

export const createPresentation = async (
  data: CreatePresentationRequest
): Promise<CreatePresentationResponse> => {
  const response = await api.post("/presentations/create/", data);
  return response.data;
};

export const getPresentation = async (
  id: string
): Promise<GetPresentationResponse> => {
  const response = await api.get(`/presentations/${id}/`);
  return response.data;
};

export const addReaction = async (
  data: AddReactionRequest
): Promise<AddReactionResponse> => {
  const response = await api.post(`/presentations/${data.id}/reactions/`, {
    reaction_type: data.reactionType,
  });
  return response.data;
};
