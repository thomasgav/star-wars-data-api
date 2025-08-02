from rest_framework import serializers
from .models import Film, Character, Planet, Species, Vehicle, Starship


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



# class PlanetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Planet
#         fields = '__all__'
#         read_only_fields = ['created_at', 'updated_at']


# class SpeciesSerializer(serializers.ModelSerializer):
#     planet = PlanetSerializer()

#     class Meta:
#         model = Species
#         fields = '__all__'
#         read_only_fields = ['created_at', 'updated_at']


# class CharacterSerializer(serializers.ModelSerializer):
#     species = SpeciesSerializer(many=True)

#     class Meta:
#         model = Character
#         fields = '__all__'
#         read_only_fields = ['created_at', 'updated_at']


# class VehicleSerializer(serializers.ModelSerializer):
#     pilots = CharacterSerializer(many=True)

#     class Meta:
#         model = Vehicle
#         fields = '__all__'
#         read_only_fields = ['created_at', 'updated_at']


# class StarshipSerializer(serializers.ModelSerializer):
#     pilots = CharacterSerializer(many=True)

#     class Meta:
#         model = Starship
#         fields = '__all__'
#         read_only_fields = ['created_at', 'updated_at']


# class FilmSerializer(serializers.ModelSerializer):
#     characters = CharacterSerializer(many=True)
#     planets = PlanetSerializer(many=True)
#     starships = StarshipSerializer(many=True)
#     vehicles = VehicleSerializer(many=True)
#     species = SpeciesSerializer(many=True)

#     class Meta:
#         model = Film
#         fields = '__all__'
#         read_only_fields = ['created_at', 'updated_at']
