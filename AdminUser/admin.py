from django.contrib import admin
from .models import Movies, MovieAllocations

# Register your models here.
class MoviesAdminPannel(admin.ModelAdmin):
    # list_display =  ['movie_name', 'movie_description', '']
    search_fields = ['movie_name']
    list_filter = ['movie_langauge', 'movie_release_date']

admin.site.register(Movies,MoviesAdminPannel)
