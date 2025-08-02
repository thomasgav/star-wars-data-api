import requests
from django.db import transaction

from .models import Character, Starship, Film
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
        characters = sync_characters()
        starships = sync_starships(characters)
        films = sync_films(characters, starships)
    except Exception as e:
        raise SyncFailed()


def sync_characters():
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
            }
        )

        character_map[item["url"]] = obj
    return character_map


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

        characters_to_be_added = []
        for url in item.get("pilots", []):
            if url in character_map:
                characters_to_be_added.append(character_map[url])

        obj.pilots.set(characters_to_be_added)

        starship_map[item["url"]] = obj
    return starship_map


def sync_films(character_map, starship_map):
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

        starships_to_be_added = []
        for url in item.get("starships", []):
            if url in starship_map:
                starships_to_be_added.append(starship_map[url])
        obj.starships.set(starships_to_be_added)
