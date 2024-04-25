import axios from "axios";

const protocol = "http";

const host = "127.0.0.1";
const port = "8000";

const baseURL = `${protocol}://${host}:${port}`;

export interface GetWordsRequest {
  text: string;
}

export interface GetWordsResponse {
  [key: string]: { frequency: number; additional_information: string };
}

export const getWordsCall = async (
  request: GetWordsRequest,
): Promise<GetWordsResponse> => {
  const config = {
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Max-Age": 600,
    },
  };

  try {
    const response = await axios.post(
      `${baseURL}/api/v0/words`,
      request,
      config,
    );
    return response.data;
  } catch (error) {
    console.error("Error making POST request:", error);
    throw error;
  }
};
