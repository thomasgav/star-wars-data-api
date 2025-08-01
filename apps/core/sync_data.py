import requests
from django.db import transaction

from .models import Planet, Species, Character, Vehicle, Starship, Film
from api.exceptions import SyncFailed


def fetch_all(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        raise e


@transaction.atomic
def sync():
    try:
        planets = sync_planets()
        species = sync_species(planets)
        characters = sync_characters(planets, species)
        vehicles = sync_vehicles(characters)
        starships = sync_starships(characters)
        films = sync_films(characters, planets, species, vehicles, starships)
    except Exception as e:
        raise SyncFailed()


def sync_planets():
    planet_map = {}
    retrieved_planets = fetch_all("https://swapi.info/api/planets/")
    for item in retrieved_planets:
        obj, _ = Planet.objects.update_or_create(
            name=item['name'],
            defaults={
                "rotation_period": item["rotation_period"],
                "orbital_period": item["orbital_period"],
                "diameter": item["diameter"],
                "climate": item["climate"],
                "gravity": item["gravity"],
                "terrain": item["terrain"],
                "surface_water": item["surface_water"],
                "population": item["population"]
            }
        )
        planet_map[item["url"]] = obj
    return planet_map


def sync_species(planets):
    species_map = {}
    retrieved_species = fetch_all("https://swapi.info/api/species/")
    for item in retrieved_species:
        obj, _ = Species.objects.update_or_create(
            name=item["name"],
            defaults={
                "classification": item["classification"],
                "designation": item["designation"],
                "average_height": item["average_height"],
                "skin_colors": item["skin_colors"],
                "hair_colors": item["hair_colors"],
                "eye_colors": item["eye_colors"],
                "average_lifespan": item["average_lifespan"],
                "language": item["language"],
                "planet": planets.get(item["homeworld"], None),
            }
        )
        species_map[item["url"]] = obj
    return species_map


def sync_characters(planets_map, species_map):
    character_map = {}
    for item in fetch_all("https://swapi.info/api/people/"):
        obj, _ = Character.objects.update_or_create(
            name=item["name"],
            defaults={
                "height": item["height"],
                "mass": item["mass"],
                "hair_color": item["hair_color"],
                "skin_color": item["skin_color"],
                "eye_color": item["eye_color"],
                "birth_year": item["birth_year"],
                "gender": item["gender"],
                "planet": planets_map.get(item["homeworld"], None),
            }
        )

        species_to_be_added = []
        for url in item.get("species", []):
            if url in species_map:
                species_to_be_added.append(species_map[url])
        obj.species.set(species_to_be_added)

        character_map[item["url"]] = obj
    return character_map


def sync_vehicles(character_map):
    vehicle_map = {}
    for item in fetch_all("https://swapi.info/api/vehicles/"):
        obj, _ = Vehicle.objects.update_or_create(
            name=item["name"],
            defaults={
                "model": item["model"],
                "manufacturer": item["manufacturer"],
                "cost_in_credits": item["cost_in_credits"],
                "length": item["length"],
                "max_atmosphering_speed": item["max_atmosphering_speed"],
                "crew": item["crew"],
                "passengers": item["passengers"],
                "cargo_capacity": item["cargo_capacity"],
                "consumables": item["consumables"],
                "vehicle_class": item["vehicle_class"],
            }
        )

        character_to_be_added = []
        for url in item.get("pilots", []):
            if url in character_map:
                character_to_be_added.append(character_map[url])
        obj.pilots.set(character_to_be_added)

        vehicle_map[item["url"]] = obj
    return vehicle_map


def sync_starships(character_map):
    starship_map = {}
    for item in fetch_all("https://swapi.info/api/starships/"):
        obj, _ = Starship.objects.update_or_create(
            name=item["name"],
            defaults={
                "model": item["model"],
                "manufacturer": item["manufacturer"],
                "cost_in_credits": item["cost_in_credits"],
                "length": item["length"],
                "max_atmosphering_speed": item["max_atmosphering_speed"],
                "crew": item["crew"],
                "passengers": item["passengers"],
                "cargo_capacity": item["cargo_capacity"],
                "consumables": item["consumables"],
                "hyperdrive_rating": item["hyperdrive_rating"],
                "MGLT": item["MGLT"],
                "starship_class": item["starship_class"],
            }
        )

        character_to_be_added = []
        for url in item.get("pilots", []):
            if url in character_map:
                character_to_be_added.append(character_map[url])
        obj.pilots.set(character_to_be_added)

        starship_map[item["url"]] = obj
    return starship_map


def sync_films(character_map, planet_map, species_map, vehicle_map, starship_map):
    for item in fetch_all("https://swapi.info/api/films/"):
        obj, _ = Film.objects.update_or_create(
            title=item["title"],
            defaults={
                "episode_id": item["episode_id"],
                "opening_crawl": item["opening_crawl"],
                "director": item["director"],
                "producer": item["producer"],
                "release_date": item["release_date"],
            }
        )

        characters_to_be_added = []
        for url in item.get("characters", []):
            if url in character_map:
                characters_to_be_added.append(character_map[url])
        obj.characters.set(characters_to_be_added)

        planets_to_be_added = []
        for url in item.get("planets", []):
            if url in planet_map:
                planets_to_be_added.append(planet_map[url])
        obj.planets.set(planets_to_be_added)

        species_to_be_added = []
        for url in item.get("species", []):
            if url in species_map:
                species_to_be_added.append(species_map[url])
        obj.species.set(species_to_be_added)

        vehicles_to_be_added = []
        for url in item.get("vehicles", []):
            if url in vehicle_map:
                vehicles_to_be_added.append(vehicle_map[url])
        obj.vehicles.set(vehicles_to_be_added)

        starships_to_be_added = []
        for url in item.get("starships", []):
            if url in starship_map:
                starships_to_be_added.append(starship_map[url])
        obj.starships.set(starships_to_be_added)
