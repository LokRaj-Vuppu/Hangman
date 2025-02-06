from django.db import models
from randomslugfield import RandomSlugField


WORDS_LIST = ["Hangman", "Python", "Audacix", "Bottle", "Pen"]

GAME_STATUS = (("InProgress", "InProgress"), ("Won", "Won"), ("Lost", "Lost"))


class TimeStamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Game(TimeStamps):
    slug = RandomSlugField(length=4)
    word = models.CharField(max_length=10, null=True, blank=True)
    guessed_letters = models.CharField(max_length=10, blank=True, default="")
    total_guesses = models.PositiveIntegerField(default=0)
    incorrect_guesses = models.PositiveIntegerField(default=0)
    maximum_incorrect_guesses = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=15, choices=GAME_STATUS, default="InProgress")

    def get_display_word(self):
        return "".join(
            [
                letter if letter.lower() in self.guessed_letters else "_"
                for letter in self.word
            ]
        )

    def __str__(self):
        return f" word - {self.word} | status - {self.status} | incorrect Guesses - {self.incorrect_guesses} | Max Guesses - {self.maximum_incorrect_guesses}"
