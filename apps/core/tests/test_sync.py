from unittest.mock import patch, Mock
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Character, Starship, Film

User = get_user_model()

mock_characters_response = [{
    "name": "Thomas Gav",
    "height": "180",
    "mass": "85",
    "hair_color": "Black",
    "skin_color": "Fair",
    "eye_color": "Brown",
    "birth_year": "1997",
    "gender": "Male",
    "url": "https://swapi.info/api/people/1/"
}]

mock_starships_response = [{
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
    "pilots": ["https://swapi.info/api/people/1/"],
    "url": "https://swapi.info/api/starships/1/"
}]

mock_films_response = [{
    "title": "New Star Wars Movie",
    "episode_id": 12,
    "opening_crawl": "In a galaxy far far way ......",
    "director": "Christopher Nolan",
    "producer": "Unknown",
    "release_date": "2026-05-19",
    "characters": ["https://swapi.info/api/people/1/"],
    "starships": ["https://swapi.info/api/starships/1/"],
}]


def make_mock_response(json_data, status_code):
    mock = Mock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    mock.raise_for_status.side_effect = (
        None if status_code == 200 else Exception(f"HTTP {status_code}")
    )
    return mock


class SyncTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass1234", email="example12@email.com")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch("apps.core.sync_data.requests.get")
    def test_sync_success(self, mock_get):

        mock_get.side_effect = [
            make_mock_response(mock_characters_response, 200),
            make_mock_response(mock_starships_response, 200),
            make_mock_response(mock_films_response, 200),
        ]

        url = reverse("sync")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Star Wars data synced successfully!")

        self.assertEqual(Character.objects.count(), 1)
        self.assertEqual(Starship.objects.count(), 1)
        self.assertEqual(Film.objects.count(), 1)

    @patch("apps.core.sync_data.requests.get")
    def test_sync_fail(self, mock_get):

        mock_get.side_effect = [
            make_mock_response(mock_characters_response, 200),
            make_mock_response(mock_starships_response, 400),
            make_mock_response(mock_films_response, 200),
        ]

        url = reverse("sync")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Syncing of data from SWAPI has failed!")

        self.assertEqual(Character.objects.count(), 0)
        self.assertEqual(Starship.objects.count(), 0)
        self.assertEqual(Film.objects.count(), 0)

    @patch("apps.core.sync_data.requests.get")
    def test_sync_fail_unauthenticated(self, mock_get):

        mock_get.side_effect = [
            make_mock_response(mock_characters_response, 200),
            make_mock_response(mock_starships_response, 200),
            make_mock_response(mock_films_response, 200),
        ]
        client = APIClient()
        url = reverse("sync")
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(Character.objects.count(), 0)
        self.assertEqual(Starship.objects.count(), 0)
        self.assertEqual(Film.objects.count(), 0)