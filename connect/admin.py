from django.contrib import admin

from .models import GenreField,Request,SectorField,InitialMatchingRequest

admin.site.register(GenreField)
admin.site.register(Request)
admin.site.register(SectorField)
admin.site.register(InitialMatchingRequest)