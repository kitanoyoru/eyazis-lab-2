import axios from "axios";

const protocol = "http";

const host = "127.0.0.1";
const port = "8000";

const baseURL = `${protocol}://${host}:${port}`;

export interface GetContextRequest {
  word: string;
  length: number;
  count: number;
}

export interface GetContextResponse {
  context: string;
}

export const getContextCall = async (
  request: GetContextRequest,
): Promise<GetContextResponse> => {
  const config = {
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Max-Age": 600,
    },
  };

  try {
    const response = await axios.post(
      `${baseURL}/api/v0/context`,
      request,
      config,
    );
    return response.data;
  } catch (error) {
    console.error("Error making POST request:", error);
    throw error;
  }
};
