from rest_framework import serializers
from word_guesser.models import Game


class GuessCharacterRequestValidationSerializer(serializers.Serializer):
    guessed_character = serializers.CharField(
        max_length=1, required=True, allow_null=False, allow_blank=False
    )

    def validate(self, attrs):
        if not attrs["guessed_character"].isalpha():
            raise serializers.ValidationError(
                "Guessed character must be in between a-z or A-Z"
            )
        return attrs


class GameDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            "word",
            "guessed_letters",
            "total_guesses",
            "incorrect_guesses",
            "maximum_incorrect_guesses",
            "status",
        )
