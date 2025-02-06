# from django.conf import Path
from django.urls import path
from word_guesser.views import CreateGame, GameStatus, GuessCharacter


urlpatterns = [
    path("new/", CreateGame.as_view()),
    path("<str:game_id>/", GameStatus.as_view()),
    path("<str:game_id>/guess/", GuessCharacter.as_view()),
]
