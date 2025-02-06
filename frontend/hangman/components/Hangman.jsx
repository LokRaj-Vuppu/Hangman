import React, { useState } from "react";
import { startNewGame, makeGuess } from "./api";

const Hangman = () => {
    const [gameState, setGameState] = useState({
        gameId: "",
        maskedWord: "",
        gameStatus: "",
        incorrectGuesses: "",
        maximumIncorrectGuesses: ""
    });
    const [guessedLetter, setGuessedLetter] = useState("");

    const handleStartNewGame = async () => {
        try {
            const response = await startNewGame();
            if (response.SUCCESS === true) {
                setGameState({
                    gameId: response.game_id,
                    maskedWord: response.masked_word,
                    gameStatus: response.game_status.toLowerCase(),
                    incorrectGuesses: response.incorrect_guesses,
                    maximumIncorrectGuesses: response.maximum_incorrect_guesses
                });
            }
        } catch (error) {
            console.error("Error starting a new game:", error);
        }
    };

    const handleNewGuess = async () => {
        if (!guessedLetter.trim()) return;

        try {
            const response = await makeGuess(gameState.gameId, guessedLetter);
            if (response?.game_details) {
                setGameState((prev) => ({
                    ...prev,
                    gameStatus: response.game_details.status.toLowerCase(),
                }));
            } else {
                setGameState({
                    gameId: gameState.gameId,
                    maskedWord: response.masked_word,
                    gameStatus: response.game_status.toLowerCase(),
                    incorrectGuesses: response.incorrect_guesses,
                    maximumIncorrectGuesses: response.maximum_incorrect_guesses
                });
            }
            setGuessedLetter("");
        } catch (error) {
            console.error("Error making a guess:", error);
        }
    };

    return (
        <div style={styles.container}>
            <h1 style={styles.title}>🎭 Hangman Game</h1>
            
            <button 
                onClick={handleStartNewGame} 
                disabled={gameState.gameStatus === "inprogress"}
                style={{
                    ...styles.startButton,
                    backgroundColor: gameState.gameStatus === "inprogress" ? "gray" : "blue"
                }}
            >
                Start New Game
            </button>

            {gameState.gameStatus === "inprogress" && (
                <div style={styles.gameContainer}>
                    <div style={styles.wordDisplay}>
                        <h2 style={styles.maskedWord}>{gameState.maskedWord}</h2>
                        <h3 style={styles.status}>Status: {gameState.gameStatus === "inprogress" ? "In Progress" : gameState.gameStatus}</h3>
                        <h3 style={styles.status}>Incorrect Guess: {gameState.incorrectGuesses} / {gameState.maximumIncorrectGuesses}</h3>
                    </div>

                    <div style={styles.inputContainer}>
                        <input
                            type="text"
                            maxLength="1"
                            value={guessedLetter}
                            onChange={(e) => {
                                const value = e.target.value;
                                if (/^[A-Za-z]?$/.test(value)) {
                                    setGuessedLetter(value);
                                }
                            }}
                            style={styles.input}
                        />
                        <button
                            onClick={handleNewGuess}
                            disabled={!guessedLetter}
                            style={{
                                ...styles.guessButton,
                                backgroundColor: guessedLetter ? "#4CAF50" : "#ccc",
                                cursor: guessedLetter ? "pointer" : "not-allowed",
                            }}
                        >
                            Guess
                        </button>
                    </div>
                </div>
            )}

            {gameState.gameStatus === "won" && (
                <div style={styles.resultMessage}>
                    <h1 style={{ color: "#4CAF50" }}>🎉 Congratulations! You won!</h1>
                </div>
            )}

            {gameState.gameStatus === "lost" && (
                <div style={styles.resultMessage}>
                    <h1 style={{ color: "#E74C3C" }}>😞 Oh no! You lost.</h1>
                </div>
            )}
        </div>
    );
};

const styles = {
    container: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        backgroundColor: "lightGray",
        fontFamily: "'Arial', sans-serif",
    },
    title: {
        fontSize: "32px",
        fontWeight: "bold",
        marginBottom: "20px",
    },
    startButton: {
        fontSize: "20px",
        padding: "10px 20px",
        border: "none",
        borderRadius: "5px",
        color: "white",
        cursor: "pointer",
        transition: "0.3s",
        marginBottom: "20px",
    },
    gameContainer: {
        backgroundColor: "white",
        padding: "30px",
        borderRadius: "10px",
        boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.2)",
        textAlign: "center",
        width: "350px",
    },
    wordDisplay: {
        marginBottom: "20px",
    },
    maskedWord: {
        fontSize: "28px",
        fontWeight: "bold",
        letterSpacing: "5px",
    },
    status: {
        fontSize: "18px",
        color: "#555",
    },
    inputContainer: {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    },
    input: {
        fontSize: "20px",
        padding: "5px",
        textAlign: "center",
        width: "50px",
        marginRight: "10px",
        border: "2px solid #333",
        borderRadius: "5px",
    },
    guessButton: {
        fontSize: "18px",
        padding: "10px 20px",
        border: "none",
        borderRadius: "5px",
        color: "white",
        transition: "0.3s",
    },
    resultMessage: {
        marginTop: "20px",
        padding: "20px",
        borderRadius: "10px",
        textAlign: "center",
    },
};

export default Hangman;
