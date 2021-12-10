from rest_framework import serializers 
from .models import CustomUser, Film, Genre, Review, UserList, Following
from rest_framework.validators import UniqueValidator


class CustomUserSerializer(serializers.ModelSerializer):

	email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all(), message='user already exists')])
	password =serializers.CharField(min_length=10, write_only=True)

	def create(self, validated_data):
		password = validated_data.pop('password')
		user = CustomUser.objects.create(**validated_data)
		user.set_password(password)
		user.save()
		return user

	class Meta:
		model = CustomUser
		fields = ['first_name', 'last_name', 'email', 'username',  'password']


class FilmSerializer(serializers.ModelSerializer):

	class Meta:
		model = Film
		fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

	class Meta:
		model = Genre 
		fields = ['name']


class ReviewSerializer(serializers.ModelSerializer):

	class Meta:
		model = Review
		fields = '__all__'

class UserListSerializer(serializers.ModelSerializer):

	class Meta:
		model = CustomUser
		exclude = ('password',)


class UserProfileSerializer(serializers.ModelSerializer):
	reviews = ReviewSerializer(many=True)
	films_watched = FilmSerializer(many=True)

	class Meta:
		model = CustomUser
		fields = ['username', 'first_name', 'last_name', 'email', 'reviews', 'films_watched']

