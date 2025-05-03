from rest_framework.viewsets import ModelViewSet
from dogs.serializers import BreedSerializer, DogSerializer
from dogs.models import Breed, Dog
from django.db.models import OuterRef, Subquery, Avg, Count


class DogViewSet(ModelViewSet):
    """
    ViewSet для модели Dog. Обрабатывает запросы CRUD для собак.

    В режиме 'list' добавляет к каждой собаке средний возраст собак её породы.
    В режиме 'retrieve' добавляет к собаке количество других собак той же породы.

    Атрибуты:
        serializer_class (Serializer): Сериализатор для модели Dog.

    Методы:
        get_queryset(): Возвращает аннотированный QuerySet в зависимости от типа действия.
    """
    serializer_class = DogSerializer

    def get_queryset(self):
        """
        Возвращает QuerySet для модели Dog с дополнительными аннотациями в зависимости от запроса.

        Returns:
            QuerySet: QuerySet объектов Dog с дополнительными данными:
                - при list: средний возраст по породе;
                - при retrieve: количество собак той же породы;
                - в остальных случаях: все записи без аннотаций.
        """
        if self.action == 'list':
            avg_age_subquery = Dog.objects.filter(
                breed=OuterRef('breed')
            ).values('breed').annotate(
                avg_age=Avg('age')
            ).values('avg_age')

            queryset = Dog.objects.annotate(
                average_breed_age=Subquery(avg_age_subquery),
            )
        elif self.action == 'retrieve':
            queryset = Dog.objects.annotate(
                same_breed_count=Count('breed__dogs')
            )
        else:
            queryset = Dog.objects.all()
        return queryset


class BreedViewSet(ModelViewSet):
    """
    ViewSet для модели Breed. Обрабатывает запросы CRUD для пород.

    Атрибуты:
        serializer_class (Serializer): Сериализатор для модели Breed.

    Методы:
        get_queryset(): Возвращает QuerySet пород с аннотацией количества собак.
    """
    serializer_class = BreedSerializer

    def get_queryset(self):
        """
        Возвращает QuerySet для модели Breed с аннотацией количества собак.

        Returns:
            QuerySet: QuerySet объектов Breed с полем dogs_count.
        """
        queryset = Breed.objects.annotate(
            dogs_count=Count('dogs')
        )
        return queryset
