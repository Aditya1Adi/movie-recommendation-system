from django.contrib import admin

# Register your models here.

from .models import Movies


class MovieAdmin(admin.ModelAdmin):
    fields = ['imdb_id', 'genres', 'original_title', 'overview', 'watched','poster_path']
    list_display = ('original_title', 'genres', 'release_date', 'watched','poster_path')
    search_fields = ['original_title', 'overview']


admin.site.register(Movies, MovieAdmin)
