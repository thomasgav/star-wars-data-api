from datetime import date
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..models import Character, Starship, Film

User = get_user_model()


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass1234", email="example12@email.com")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class CharacterTests(BaseAPITestCase):
    def create_dummy_character(self):
        character = Character.objects.create(
            name="Random dude",
            height="190",
            mass="80",
            hair_color="Brown",
            skin_color="Light",
            eye_color="Brown",
            birth_year="2000",
            gender="Male"
        )

        return character

    def test_create_character(self):
        url = reverse("character-list")
        data = {
            "name": "Thomas Gav",
            "height": "180",
            "mass": "85",
            "hair_color": "Black",
            "skin_color": "Fair",
            "eye_color": "Brown",
            "birth_year": "1997",
            "gender": "Male"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Character.objects.count(), 1)

    def test_list_characters(self):
        character = self.create_dummy_character()

        url = reverse("character-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_character(self):
        character = self.create_dummy_character()

        url = reverse("character-detail", args=[character.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Random dude")

    def test_update_character(self):
        character = self.create_dummy_character()

        url = reverse("character-detail", args=[character.id])
        data = {"name": "Another dude"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Another dude")

    def test_delete_character(self):
        character = self.create_dummy_character()

        url = reverse("character-detail", args=[character.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Character.objects.count(), 0)

    def test_create_character_unauthenticated(self):
        url = reverse("character-list")
        data = {
            "name": "Thomas Gav",
            "height": "180",
            "mass": "85",
            "hair_color": "Black",
            "skin_color": "Fair",
            "eye_color": "Brown",
            "birth_year": "1997",
            "gender": "Male"
        }
        client = APIClient()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Character.objects.count(), 0)

    def test_create_character_fail_not_null_value_missing(self):
        url = reverse("character-list")
        data = {
            "name": "Thomas Gav",
            "mass": "85",
            "hair_color": "Black",
            "skin_color": "Fair",
            "eye_color": "Brown",
            "birth_year": "1997",
            "gender": "Male"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('height', response.data['errors'])
        self.assertIn('This field is required.', str(response.data['errors']['height']))

    def test_retrieve_characters_unauthenticated(self):
        character = self.create_dummy_character()
        client = APIClient()

        url = reverse('character-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_character_unauthenticated(self):
        character = self.create_dummy_character()

        url = reverse("character-detail", args=[character.id])
        data = {"name": "Another dude"}
        client = APIClient()
        response = client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_character_unauthenticated(self):
        character = self.create_dummy_character()

        url = reverse("character-detail", args=[character.id])
        client = APIClient()
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class StarshipTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.pilot = Character.objects.create(
            name="Thomas Gav",
            height="180",
            mass="85",
            hair_color="Black",
            skin_color="Fair",
            eye_color="Brown",
            birth_year="1997",
            gender="Male"
        )

    def create_dummy_starship(self):
        starship = Starship.objects.create(
            name="Amazing Starship",
            model="Latest Model 3",
            manufacturer="Ferrari",
            cost_in_credits="23000000",
            length="15",
            max_atmosphering_speed="1050",
            crew="25",
            passengers="30",
            cargo_capacity="110",
            consumables="1 week",
            hyperdrive_rating="1.0",
            MGLT="100",
            starship_class="Starfighter"
        )
        starship.pilots.set([self.pilot])
        return starship

    def test_create_starship(self):
        url = reverse("starship-list")
        data = {
            "name": "Amazing Starship",
            "model": "Latest Model 3",
            "manufacturer": "Ferrari",
            "cost_in_credits": "23000000",
            "length": "15",
            "max_atmosphering_speed": "1050",
            "crew": "25",
            "passengers": "30",
            "cargo_capacity": "110",
            "consumables": "1 week",
            "hyperdrive_rating": "1.0",
            "MGLT": "100",
            "starship_class": "Starfighter",
            "pilots": [self.pilot.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Starship.objects.count(), 1)
        self.assertEqual(response.data["pilots"][0]["name"], "Thomas Gav")

    def test_list_starships(self):
        starship = self.create_dummy_starship()

        url = reverse("starship-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_starship(self):
        starship = self.create_dummy_starship()

        url = reverse("starship-detail", args=[starship.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Amazing Starship")
        self.assertEqual(response.data["pilots"][0]["name"], "Thomas Gav")

    def test_update_starship(self):
        starship = self.create_dummy_starship()

        url = reverse("starship-detail", args=[starship.id])
        data = {"model": "Latest Model 5"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["model"], "Latest Model 5")

    def test_delete_starship(self):
        starship = self.create_dummy_starship()

        url = reverse("starship-detail", args=[starship.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Starship.objects.count(), 0)

    def test_create_starship_unauthenticated(self):
        url = reverse("starship-list")
        data = {
            "name": "Amazing Starship",
            "model": "Latest Model 3",
            "manufacturer": "Ferrari",
            "cost_in_credits": "23000000",
            "length": "15",
            "max_atmosphering_speed": "1050",
            "crew": "25",
            "passengers": "30",
            "cargo_capacity": "110",
            "consumables": "1 week",
            "hyperdrive_rating": "1.0",
            "MGLT": "100",
            "starship_class": "Starfighter",
            "pilots": [self.pilot.id]
        }
        client = APIClient()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_starships_unauthenticated(self):
        starship = self.create_dummy_starship()

        url = reverse("starship-list")
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_starship_unauthenticated(self):
        starship = self.create_dummy_starship()

        url = reverse("starship-detail", args=[starship.id])
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_starship_unauthenticated(self):
        starship = self.create_dummy_starship()

        url = reverse("starship-detail", args=[starship.id])
        data = {"model": "Latest Model 5"}
        client = APIClient()
        response = client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_starship_unauthenticated(self):
        starship = self.create_dummy_starship()

        url = reverse("starship-detail", args=[starship.id])
        client = APIClient()
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FilmTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.char1 = Character.objects.create(
            name="Thomas Gav",
            height="180",
            mass="85",
            hair_color="Black",
            skin_color="Fair",
            eye_color="Brown",
            birth_year="1997",
            gender="Male"
        )
        self.ship1 = Starship.objects.create(
            name="Amazing Starship",
            model="Latest Model 3",
            manufacturer="Ferrari",
            cost_in_credits="23000000",
            length="15",
            max_atmosphering_speed="1050",
            crew="25",
            passengers="30",
            cargo_capacity="110",
            consumables="1 week",
            hyperdrive_rating="1.0",
            MGLT="100",
            starship_class="Starfighter"
        )
        self.ship1.pilots.set([self.char1])

    def create_dummy_film(self):
        film = Film.objects.create(
            title="New Star Wars Movie",
            episode_id=12,
            opening_crawl="In a galaxy far far way ......",
            director="Christopher Nolan",
            producer="Unknown",
            release_date=date(2026, 5, 19)
        )
        film.starships.set([self.ship1])
        film.characters.set([self.char1])
        return film

    def test_create_film(self):
        url = reverse("film-list")
        data = {
            "title": "New Star Wars Movie",
            "episode_id": 12,
            "opening_crawl": "In a galaxy far far way ......",
            "director": "Christopher Nolan",
            "producer": "Unknown",
            "release_date": "2026-05-19",
            "characters": [self.char1.id],
            "starships": [self.ship1.id]
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(response.data["characters"][0]["name"], "Thomas Gav")
        self.assertEqual(response.data["starships"][0]["name"], "Amazing Starship")

    def test_list_films(self):
        film = self.create_dummy_film()

        url = reverse("film-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_film(self):
        film = self.create_dummy_film()

        url = reverse("film-detail", args=[film.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New Star Wars Movie")
        self.assertEqual(response.data["characters"][0]["name"], "Thomas Gav")
        self.assertEqual(response.data["starships"][0]["name"], "Amazing Starship")
        self.assertEqual(response.data["starships"][0]["pilots"][0]["name"], "Thomas Gav")

    def test_update_film(self):
        film = self.create_dummy_film()

        url = reverse("film-detail", args=[film.id])
        data = {"title": "The Newest Star Wars Movie"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "The Newest Star Wars Movie")

    def test_delete_film(self):
        film = self.create_dummy_film()

        url = reverse("film-detail", args=[film.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Film.objects.count(), 0)

    def test_create_film_unauthenticated(self):
        url = reverse("film-list")
        data = {
            "title": "New Star Wars Movie",
            "episode_id": 12,
            "opening_crawl": "In a galaxy far far way ......",
            "director": "Christopher Nolan",
            "producer": "Unknown",
            "release_date": "2026-05-19",
            "characters": [self.char1.id],
            "starships": [self.ship1.id]
        }
        client = APIClient()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_films_unauthenticated(self):
        film = self.create_dummy_film()

        url = reverse("film-list")
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_film_unauthenticated(self):
        film = self.create_dummy_film()

        url = reverse("film-detail", args=[film.id])
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_film_unauthenticated(self):
        film = self.create_dummy_film()

        url = reverse("film-detail", args=[film.id])
        data = {"title": "The Newest Star Wars Movie"}
        client = APIClient()
        response = client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_film_unauthenticated(self):
        film = self.create_dummy_film()

        url = reverse("film-detail", args=[film.id])
        client = APIClient()
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
