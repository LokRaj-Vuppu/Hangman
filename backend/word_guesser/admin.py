from django.contrib import admin
from word_guesser.models import Game


class ReadOnlyFieldGame(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", "slug")


admin.site.register(Game, ReadOnlyFieldGame)
