from rest_framework import serializers

from .models import *


#============== write only serializers ==============
class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class StarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starship
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


#============== read only serializers ==============
class SpeciesReadOnlySerializer(serializers.ModelSerializer):
    planet = PlanetSerializer()

    class Meta:
        model = Species
        fields = '__all__'


class CharacterReadOnlySerializer(serializers.ModelSerializer):
    planet = PlanetSerializer()
    species = SpeciesReadOnlySerializer(many=True)

    class Meta:
        model = Character
        fields = '__all__'


class VehicleReadOnlySerializer(serializers.ModelSerializer):
    pilots = CharacterReadOnlySerializer(many=True)

    class Meta:
        model = Vehicle
        fields = '__all__'


class StarshipReadOnlySerializer(serializers.ModelSerializer):
    pilots = CharacterReadOnlySerializer(many=True)

    class Meta:
        model = Starship
        fields = '__all__'


class FilmReadOnlySerializer(serializers.ModelSerializer):
    characters = CharacterReadOnlySerializer(many=True)
    planets = PlanetSerializer(many=True)
    starships = StarshipReadOnlySerializer(many=True)
    vehicles = VehicleReadOnlySerializer(many=True)
    species = SpeciesReadOnlySerializer(many=True)

    class Meta:
        model = Film
        fields = '__all__'
