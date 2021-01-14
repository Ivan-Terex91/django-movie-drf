from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Actor, Review
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializes, CreateRatingSerializer, \
    ActorListSerializer, ActorDetailSerializer
from .service import get_client_ip, MovieFilter


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов или одного фильма"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F("ratings__star")) / models.Count(models.F("ratings"))
        )
        return movies

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializes


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга к фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка или одного актёра или режессёра"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer

#  Классы на generic классах
# class MovieListView(generics.ListAPIView):
#     """Вывод списка фильмов"""
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F("ratings__star")) / models.Count(models.F("ratings"))
#         )
#         return movies
#
#
# class MovieDetailView(generics.RetrieveAPIView):
#     """Вывод фильма"""
#
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#
# # class ReviewDestroyView(generics.DestroyAPIView):
# #     """Удаление отзыва"""
# #     queryset = Review.objects.all()
# #     permission_classes = [permissions.IsAdminUser]
#
#
# class ReviewCreateView(generics.CreateAPIView):
#     """Добавление отзыва к фильму"""
#     serializer_class = ReviewCreateSerializes
#
#
# class AddStarRatingView(generics.CreateAPIView):
#     """Добавление рейтинга к фильму"""
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
#
#
# class ActorListView(generics.ListAPIView):
#     """Вывод списка актёров и режессёров"""
#     queryset = Actor.objects.filter()
#     serializer_class = ActorListSerializer
#
#
# class ActorDetailView(generics.RetrieveAPIView):
#     """Вывод информации об актёре или режиссёре"""
#     queryset = Actor.objects.filter()
#     serializer_class = ActorDetailSerializer
