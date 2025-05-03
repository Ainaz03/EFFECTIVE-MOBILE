from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Breed(models.Model):
    SIZE_TYPES = (
        ('Tiny', 'Tiny'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    )

    name = models.CharField(max_length=250)
    size = models.CharField(max_length=10, choices=SIZE_TYPES)

    friendliness = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    trainability = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    shedding_amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    exercise_needs = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.name

class Dog(models.Model):
    name = models.CharField(max_length=250)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=50)
    color = models.CharField(max_length=250)
    favorite_food = models.CharField(max_length=250)
    favorite_toy = models.CharField(max_length=250)

    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='dogs')

    def __str__(self):
        return self.name