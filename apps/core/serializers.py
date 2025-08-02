from rest_framework import serializers

from .models import Film, Character, Starship


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class StarshipReadOnlySerializer(serializers.ModelSerializer):
    pilots = CharacterSerializer(many=True)

    class Meta:
        model = Starship
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class StarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starship
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class FilmReadOnlySerializer(serializers.ModelSerializer):
    characters = CharacterSerializer(many=True)
    starships = StarshipSerializer(many=True)

    class Meta:
        model = Film
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
