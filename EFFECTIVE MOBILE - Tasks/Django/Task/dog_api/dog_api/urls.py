from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from dogs.models import Breed, Dog
from dogs.views import BreedViewSet, DogViewSet

router = DefaultRouter()
router.register(r'api/dogs', DogViewSet, basename=Dog)
router.register(r'api/breeds', BreedViewSet, basename=Breed)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]