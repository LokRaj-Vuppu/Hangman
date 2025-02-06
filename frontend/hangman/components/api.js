import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/game";

export const startNewGame = async () => {
  try {
    const response = await axios.post(`${BASE_URL}/new/`);
    return response.data;
  } catch (error) {
    console.error("Error starting game:", error);
    throw error;
  }
};

export const getGameState = async (gameId) => {
  try {
    const response = await axios.post(`${BASE_URL}/${gameId}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching game state:", error);
    throw error;
  }
};

export const makeGuess = async (gameId, guessed_character) => {
  try {
    const response = await axios.post(`${BASE_URL}/${gameId}/guess/`, { guessed_character });
    return response.data;
  } catch (error) {
    console.error("Error making guess:", error);
    throw error;
  }
};
