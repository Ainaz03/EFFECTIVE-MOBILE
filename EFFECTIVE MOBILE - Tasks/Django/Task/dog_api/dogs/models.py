from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Breed(models.Model):
    """
    Модель породы собаки.

    Атрибуты:
        name (str): Название породы.
        size (str): Размер породы (Tiny, Small, Medium, Large).
        friendliness (int): Уровень дружелюбия от 1 до 5.
        trainability (int): Уровень обучаемости от 1 до 5.
        shedding_amount (int): Уровень линьки от 1 до 5.
        exercise_needs (int): Уровень потребности в физической активности от 1 до 5.
    """
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
        """
        Возвращает строковое представление объекта.

        Returns:
            str: Название породы.
        """
        return self.name


class Dog(models.Model):
    """
    Модель собаки.

    Атрибуты:
        name (str): Имя собаки.
        age (int): Возраст собаки.
        gender (str): Пол собаки.
        color (str): Цвет шерсти.
        favorite_food (str): Любимая еда.
        favorite_toy (str): Любимая игрушка.
        breed (Breed): Внешний ключ на породу.
    """
    name = models.CharField(max_length=250)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=50)
    color = models.CharField(max_length=250)
    favorite_food = models.CharField(max_length=250)
    favorite_toy = models.CharField(max_length=250)

    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='dogs')

    def __str__(self):
        """
        Возвращает строковое представление объекта.

        Returns:
            str: Имя собаки.
        """
        return self.name
