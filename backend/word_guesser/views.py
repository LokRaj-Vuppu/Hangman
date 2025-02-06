from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random, math
from word_guesser.models import WORDS_LIST, Game
from word_guesser.serializers import (
    GuessCharacterRequestValidationSerializer,
    GameDetailsSerializer,
)


class CreateGame(APIView):
    """
    API to create a game and return game id
    """

    def post(self, request):
        try:
            word = random.choice(WORDS_LIST)
            maximum_incorrect_guesses = math.ceil(len(word) / 2)
            game = Game.objects.create(
                word=word, maximum_incorrect_guesses=maximum_incorrect_guesses
            )
            return Response(
                {
                    "SUCCESS": True,
                    "message": "Your game is started!",
                    "game_id": game.slug,
                    "word_length": len(game.word),
                    "masked_word": game.get_display_word(),
                    "incorrect_guesses": game.incorrect_guesses,
                    "maximum_incorrect_guesses": game.maximum_incorrect_guesses,
                    "game_status": game.status,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as error:
            return Response(
                {"SUCCESS": False, "message": "Something went wrong, please try again"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GameStatus(APIView):
    """
    API to return the game status based on game ID
    """

    def post(self, request, game_id):
        try:
            if len(game_id) != 4:
                return Response(
                    {
                        "SUCCESS": False,
                        "message": "Invalid Request !",
                        "error": "game_id should be exactly 4 charcters",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                game = Game.objects.get(slug=game_id)
            except Game.DoesNotExist as error:
                return Response(
                    {
                        "SUCCESS": False,
                        "message": "Unable to find Game, please check game_id",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {
                    "SUCCESS": True,
                    "game_status": game.status,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                {"SUCCESS": False, "message": "Something went wrong, please try again"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GuessCharacter(APIView):
    """
    API to guess a character
    """

    def post(self, request, game_id):
        if len(game_id) != 4:
            return Response(
                {
                    "SUCCESS": False,
                    "message": "Invalid Request !",
                    "error": "game_id should be exactly 4 charcters",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        request_data = GuessCharacterRequestValidationSerializer(data=request.data)
        if not request_data.is_valid():
            return Response(
                {
                    "SUCCESS": False,
                    "message": "Invalid Request!",
                    "errors": request_data.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        guessed_character = request_data.validated_data["guessed_character"].lower()

        try:
            game = Game.objects.get(slug=game_id)
        except Game.DoesNotExist as error:
            return Response(
                {
                    "SUCCESS": False,
                    "message": "Unable to find Game, please check game_id",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_correct_guess = guessed_character in game.word.lower()
        message = "That’s the right guess!" if is_correct_guess else "Incorrect guess!"

        if guessed_character not in game.guessed_letters:
            game.guessed_letters += guessed_character

        if (
            not is_correct_guess
            and game.incorrect_guesses < game.maximum_incorrect_guesses
        ):
            game.incorrect_guesses += 1

        if "_" not in game.get_display_word():
            game.status = "Won"
            game.save()
            game_details_serialized = GameDetailsSerializer(game).data
            return Response(
                {
                    "SUCCESS": True,
                    "message": "Game Won!",
                    "game_details": game_details_serialized,
                },
                status=status.HTTP_200_OK,
            )

        if game.incorrect_guesses >= game.maximum_incorrect_guesses:
            game.status = "Lost"
            game.save()
            game_details_serialized = GameDetailsSerializer(game).data
            return Response(
                {
                    "SUCCESS": True,
                    "message": "Game Lost",
                    "game_details": game_details_serialized,
                },
                status=status.HTTP_200_OK,
            )
        game.total_guesses += 1
        game.save()

        return Response(
            {
                "SUCCESS": True,
                "message": message,
                "masked_word": game.get_display_word(),
                "word_length": len(game.word),
                "incorrect_guesses": game.incorrect_guesses,
                "maximum_incorrect_guesses": game.maximum_incorrect_guesses,
                "game_status": game.status,
            },
            status=status.HTTP_200_OK,
        )
