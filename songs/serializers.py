from rest_framework import serializers

from .models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title", "duration", "album_id"]
        read_only_fields = ("id", "album_id")
        extra_kwargs = {"title": {"max_length": 255}, "duration": {"max_length": 255}}

    def create(self, validated_data):
        return Song.objects.create(**validated_data)
