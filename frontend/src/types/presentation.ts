export type Presentation = {
  id: string;
  title: string;
  description: string;
  created_at: string;
  heart: number;
  thumbs_up: number;
  laugh: number;
  surprise: number;
};

export type CreatePresentationRequest = {
  title: string;
  description?: string;
};

export type CreatePresentationResponse = {
  success: boolean;
  id: string;
  title: string;
  description: string;
};

export type GetPresentationResponse = {
  success: boolean;
} & Presentation;

export type ReactionType = "thumbs_up" | "heart" | "laugh" | "surprise";

export type AddReactionRequest = {
  id: string;
  reactionType: ReactionType;
};

export type AddReactionResponse = {
  success: boolean;
  id: string;
};
