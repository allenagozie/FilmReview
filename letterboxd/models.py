from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class Film(models.Model):
	name = models.CharField(max_length=150)
	year = models.IntegerField()
	genre = models.ManyToManyField(Genre)

	def __str__(self):
		return self.name 

class CustomUser(AbstractUser):
	films_watched = models.ManyToManyField(Film)

	def follow_count(self):
		return self.followers.count()

class Following(models.Model):
	follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE, null=True)
	the_followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followed', on_delete=models.CASCADE, null=True)
	date_followed = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.follower.id} followed {self.the_followed.id}'

	class Meta:
		verbose_name_plural = 'Following Connections'


class Review(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE, null=True)
	film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True)
	review_body = models.TextField(max_length=250)
	review_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user}'s review for {self.film}"

class UserList(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userlist", on_delete=models.CASCADE, null=True)
	film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True)

class AddFilm(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='addingfilm', on_delete=models.CASCADE, null=True)
	film_added = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="filmadded", on_delete=models.CASCADE, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Adding Films"

class Like(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE, null=True)
	film = models.ForeignKey(Film, related_name='likes', on_delete=models.CASCADE, null=True)

class Rating(models.Model):
	rate = models.ForeignKey(Film,validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], on_delete=models.CASCADE)
	film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='filmrating')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ratings', on_delete=models.CASCADE, null=True)
