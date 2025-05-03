from django.contrib import admin

from dogs.models import Breed, Dog

admin.site.register(Breed)
admin.site.register(Dog)