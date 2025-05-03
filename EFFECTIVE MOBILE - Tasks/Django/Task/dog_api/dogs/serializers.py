from rest_framework import serializers
from dogs.models import Breed, Dog


class BreedSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Breed.

    Добавляет поле dogs_count, которое отображает количество собак данной породы.

    Атрибуты:
        dogs_count (int): Количество собак данной породы. Только для чтения.

    Meta:
        model (Breed): Модель, с которой работает сериализатор.
        fields (list): Все поля модели + dogs_count.
    """
    dogs_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Breed
        fields = '__all__'


class DogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Dog.

    Добавляет следующие вычисляемые поля:
        - average_breed_age: Средний возраст собак той же породы (только для list).
        - same_breed_count: Количество собак той же породы (только для retrieve).

    Атрибуты:
        average_breed_age (float): Средний возраст по породе. Только для чтения.
        same_breed_count (int): Количество собак той же породы. Только для чтения.

    Meta:
        model (Dog): Модель, с которой работает сериализатор.
        fields (list): Все поля модели + дополнительные аннотации.
    """
    average_breed_age = serializers.FloatField(read_only=True)
    same_breed_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = '__all__'
