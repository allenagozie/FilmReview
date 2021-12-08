from django.contrib import admin
from .models import CustomUser, Film, Genre, Review


class CustomeUserAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'username', 'email', 'get_films_watched']

	def get_films_watched(self, obj):
		return '\n'.join([f.name for f in obj.films_watched.all()])

class FilmAdmin(admin.ModelAdmin):
	list_display = ['name', 'year', 'get_genre']

	def get_genre(self, obj):
		return '\n'.join([g.name for g in obj.genre.all()])

admin.site.register(CustomUser, CustomeUserAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Genre)
admin.site.register(Review)