from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .pagination import StandardResultsSetPagination
from .sync_data import sync


class SyncView(APIView):
    def post(self, request):
        sync()
        return Response({"detail": "Star Wars data synced successfully"}, status=status.HTTP_200_OK)


class FilmViewSet(viewsets.ModelViewSet):
    # queryset = Film.objects.prefetch_related(
    #     Prefetch("characters", queryset=Character.objects.select_related("planet").prefetch_related("species")),
    #     "planets",
    #     "starships__pilots",
    #     "vehicles__pilots",
    #     "species"
    # )
    # queryset = Film.objects.prefetch_related(
    #     # Prefetch characters and their related data
    #     Prefetch(
    #         "characters",
    #         queryset=Character.objects.select_related("planet").prefetch_related(
    #             # Prefetch species and their related planet
    #             Prefetch(
    #                 "species",
    #                 queryset=Species.objects.select_related("planet")
    #             )
    #         )
    #     ),
    #     # Prefetch planets (top-level relationship to Film)
    #     "planets",
    #     # Prefetch starships and their pilots, and the pilots' related data
    #     Prefetch(
    #         "starships",
    #         queryset=Starship.objects.prefetch_related(
    #             Prefetch(
    #                 "pilots",
    #                 queryset=Character.objects.select_related("planet").prefetch_related(
    #                     Prefetch(
    #                         "species",
    #                         queryset=Species.objects.select_related("planet")
    #                     )
    #                 )
    #             )
    #         )
    #     ),
    #     # Prefetch vehicles and their pilots, and the pilots' related data
    #     Prefetch(
    #         "vehicles",
    #         queryset=Vehicle.objects.prefetch_related(
    #             Prefetch(
    #                 "pilots",
    #                 queryset=Character.objects.select_related("planet").prefetch_related(
    #                     Prefetch(
    #                         "species",
    #                         queryset=Species.objects.select_related("planet")
    #                     )
    #                 )
    #             )
    #         )
    #     ),
    #     # Prefetch species and their related planet
    #     Prefetch(
    #         "species",
    #         queryset=Species.objects.select_related("planet")
    #     )
    # )
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = StandardResultsSetPagination


class CharacterViewSet(viewsets.ModelViewSet):
    # queryset = Character.objects.select_related("planet").prefetch_related("species")
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = StandardResultsSetPagination


class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = StandardResultsSetPagination


class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = Species.objects.all()
    # queryset = Species.objects.select_related("planet")
    serializer_class = SpeciesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = StandardResultsSetPagination


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    # queryset = Vehicle.objects.prefetch_related("pilots__species", "pilots__planet")
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = StandardResultsSetPagination


class StarshipViewSet(viewsets.ModelViewSet):
    # queryset = Starship.objects.prefetch_related("pilots__species", "pilots__planet")
    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = StandardResultsSetPagination
