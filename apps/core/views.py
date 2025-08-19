from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .pagination import StandardResultsSetPagination
from .sync_data import sync


class SyncView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sync()
        return Response({"message": "Star Wars data synced successfully!"}, status=status.HTTP_200_OK)


class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name']
    pagination_class = StandardResultsSetPagination


class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = Species.objects.select_related("planet")
    # queryset = Species.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SpeciesReadOnlySerializer
        return SpeciesSerializer

    def create(self, request, *args, **kwargs):
        #write serializer to handle only ids in the foreign key fields (less complexity)
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        film = write_serializer.save()

        #read_only serializer for a more clear response
        read_serializer = SpeciesReadOnlySerializer(film)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        #write serializer to handle only ids in the foreign key fields (less complexity)
        write_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        write_serializer.is_valid(raise_exception=True)
        film = write_serializer.save()

        #read_only serializer for a more clear response
        read_serializer = SpeciesReadOnlySerializer(film)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.select_related("planet").prefetch_related("species")
    # queryset = Character.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CharacterReadOnlySerializer
        return CharacterSerializer

    def create(self, request, *args, **kwargs):
        #write serializer to handle only ids in the foreign key fields (less complexity)
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        film = write_serializer.save()

        #read_only serializer for a more clear response
        read_serializer = CharacterReadOnlySerializer(film)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        #write serializer to handle only ids in the foreign key fields (less complexity)
        write_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        write_serializer.is_valid(raise_exception=True)
        film = write_serializer.save()

        #read_only serializer for a more clear response
        read_serializer = CharacterReadOnlySerializer(film)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().prefetch_related(
        Prefetch(
            "pilots",
            queryset=Character.objects.select_related("planet").prefetch_related("species")
        )
    )
    # queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return VehicleReadOnlySerializer
        return VehicleSerializer

    def create(self, request, *args, **kwargs):
        #write serializer to handle only ids in the foreign key fields (less complexity)
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        film = write_serializer.save()

        #read_only serializer for a more clear response
        read_serializer = VehicleReadOnlySerializer(film)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        #write serializer to handle only ids in the foreign key fields (less complexity)
        write_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        write_serializer.is_valid(raise_exception=True)
        film = write_serializer.save()

        #read_only serializer for a more clear response
        read_serializer = VehicleReadOnlySerializer(film)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class StarshipViewSet(viewsets.ModelViewSet):
    queryset = Starship.objects.all().prefetch_related(
        Prefetch(
            "pilots",
            queryset=Character.objects.select_related("planet").prefetch_related("species")
        )
    )
    # queryset = Starship.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return StarshipReadOnlySerializer
        return StarshipSerializer

    def create(self, request, *args, **kwargs):
        #write serializer to handle only ids in the foreign key fields (less complexity)
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        film = write_serializer.save()

        #read_only serializer for a more clear response
        read_serializer = StarshipReadOnlySerializer(film)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        #write serializer to handle only ids in the foreign key fields (less complexity)
        write_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        write_serializer.is_valid(raise_exception=True)
        film = write_serializer.save()

        #read_only serializer for a more clear response
        read_serializer = StarshipReadOnlySerializer(film)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.prefetch_related(
        # Prefetch characters and their related data
        Prefetch(
            "characters",
            queryset=Character.objects.select_related("planet").prefetch_related(
                # Prefetch species and their related planet
                Prefetch(
                    "species",
                    queryset=Species.objects.select_related("planet")
                )
            )
        ),
        # Prefetch planets (top-level relationship to Film)
        "planets",
        # Prefetch starships and their pilots, and the pilots' related data
        Prefetch(
            "starships",
            queryset=Starship.objects.prefetch_related(
                Prefetch(
                    "pilots",
                    queryset=Character.objects.select_related("planet").prefetch_related(
                        Prefetch(
                            "species",
                            queryset=Species.objects.select_related("planet")
                        )
                    )
                )
            )
        ),
        # Prefetch vehicles and their pilots, and the pilots' related data
        Prefetch(
            "vehicles",
            queryset=Vehicle.objects.prefetch_related(
                Prefetch(
                    "pilots",
                    queryset=Character.objects.select_related("planet").prefetch_related(
                        Prefetch(
                            "species",
                            queryset=Species.objects.select_related("planet")
                        )
                    )
                )
            )
        ),
        # Prefetch species and their related planet
        Prefetch(
            "species",
            queryset=Species.objects.select_related("planet")
        )
    )
    # queryset = Film.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['title']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return FilmReadOnlySerializer
        return FilmSerializer

    def create(self, request, *args, **kwargs):
        #write serializer to handle only ids in the foreign key fields (less complexity)
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        film = write_serializer.save()

        #read_only serializer for a more clear response
        read_serializer = FilmReadOnlySerializer(film)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        #write serializer to handle only ids in the foreign key fields (less complexity)
        write_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        write_serializer.is_valid(raise_exception=True)
        film = write_serializer.save()

        #read_only serializer for a more clear response
        read_serializer = FilmReadOnlySerializer(film)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)



