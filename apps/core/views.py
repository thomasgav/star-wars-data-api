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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sync()
        return Response({"detail": "Star Wars data synced successfully"}, status=status.HTTP_200_OK)


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.prefetch_related('characters', 'starships__pilots')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
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


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = StandardResultsSetPagination


class StarshipViewSet(viewsets.ModelViewSet):
    queryset = Starship.objects.prefetch_related("pilots")
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
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
