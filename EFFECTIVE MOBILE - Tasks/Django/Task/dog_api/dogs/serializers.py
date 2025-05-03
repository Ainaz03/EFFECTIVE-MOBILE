from rest_framework import serializers

from dogs.models import Breed, Dog

class BreedSerializer(serializers.ModelSerializer):
    dogs_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Breed
        fields = '__all__'

class DogSerializer(serializers.ModelSerializer):
    average_breed_age = serializers.FloatField(read_only=True)
    same_breed_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = '__all__'