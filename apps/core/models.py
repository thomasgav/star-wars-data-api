from django.db import models
from api.models import BaseModel


class Character(BaseModel):
    name = models.CharField(max_length=255)
    height = models.CharField(max_length=50)
    mass = models.CharField(max_length=50)
    hair_color = models.CharField(max_length=100)
    skin_color = models.CharField(max_length=100)
    eye_color = models.CharField(max_length=100)
    birth_year = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Starship(BaseModel):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    cost_in_credits = models.CharField(max_length=50)
    length = models.CharField(max_length=50)
    max_atmosphering_speed = models.CharField(max_length=50)
    crew = models.CharField(max_length=50)
    passengers = models.CharField(max_length=50)
    cargo_capacity = models.CharField(max_length=50)
    consumables = models.CharField(max_length=100)
    hyperdrive_rating = models.CharField(max_length=50)
    MGLT = models.CharField(max_length=50)
    starship_class = models.CharField(max_length=100)
    pilots = models.ManyToManyField(Character, blank=True, related_name="starships")

    def __str__(self):
        return "Startship " + self.name


class Film(BaseModel):
    title = models.CharField(max_length=255)
    episode_id = models.IntegerField()
    opening_crawl = models.TextField()
    director = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    release_date = models.DateField()
    characters = models.ManyToManyField(Character, blank=True, related_name="films")
    starships = models.ManyToManyField(Starship, blank=True, related_name="films")

    def __str__(self):
        return self.title
