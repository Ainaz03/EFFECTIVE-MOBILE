from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from dogs.serializers import BreedSerializer, DogSerializer
from dogs.models import Breed, Dog
from django.db.models import OuterRef, Subquery, Avg, Count

class DogViewSet(ModelViewSet):
    serializer_class = DogSerializer

    def get_queryset(self):
        avg_age_subquery = Dog.objects.filter(
            breed=OuterRef('breed')
        ).values('breed').annotate(
            avg_age=Avg('age')
        ).values('avg_age')

        queryset = Dog.objects.annotate(
            average_breed_age=Subquery(avg_age_subquery),
            same_breed_count=Count('breed__dogs')
        )
        return queryset

class BreedViewSet(ModelViewSet):
    serializer_class = BreedSerializer

    def get_queryset(self):
        queryset = Breed.objects.annotate(
            dogs_count=Count('dogs')
        )
        return queryset