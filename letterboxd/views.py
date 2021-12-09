from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from letterboxd.serializers import CustomUserSerializer, FilmSerializer, ReviewSerializer, UserListSerializer, UserProfileSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import permissions
from .models import CustomUser, Film, Review, UserList, AddFilm, Following, Like
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import render

from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_204_NO_CONTENT,
	HTTP_404_NOT_FOUND,
	HTTP_201_CREATED, 
	HTTP_200_OK,
	)
class SignUpView(APIView):
	permission_classes = [AllowAny,]

	def post(self, request):
		serializer = CustomUserSerializer(data=request.data, context={'request':request})
		if serializer.is_valid():
			user = serializer.save()
			if user:
				token = Token.objects.create(user=user)
				response = serializer.data
				response['token'] = token.key 

				return Response(data=response, status=HTTP_201_CREATED)
		return Response(serializer.errors, HTTP_400_BAD_REQUEST)

class LoginView(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):
		username = request.data.get("username")
		password = request.data.get("password")

		if username is None or password is None:
			return Response("Provide username and password", HTTP_400_BAD_REQUEST)

		user = authenticate(username=username, password=password)
		if not user:
			return Response(
				"Invalid credentials", HTTP_404_NOT_FOUND
				)
		token, _ = Token.objects.get_or_create(user=user)
		response = CustomUserSerializer(user).data
		response['token'] = token.key
		return Response(response, HTTP_200_OK)


class ListFilmView(APIView):
	#serializer_classes = FilmSerializer

	def get(self, request):
		film_list = Film.objects.all()
		serializer = FilmSerializer(film_list, many=True)
		return Response(serializer.data, HTTP_200_OK)

class ReviewView(APIView):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

	def post(self, request):
		if request.method == 'POST':
			review = request.data.get('review_body')
			Review.objects.create(review_body=review, user=request.user)
			return Response('good job')

	def get(self, request):
		reviews = Review.objects.all()
		print(reviews)
		serializer = ReviewSerializer(reviews, many=True)
		print(serializer.data)
		return Response(serializer.data, HTTP_200_OK)

class UserListView(APIView):
	queryset = CustomUser.objects.all()
	serializer_class = UserListSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

	def get(self, request):
		userlist =  CustomUser.objects.all()
		serializer = CustomUserSerializer(userlist, many=True)
		return Response(serializer.data, HTTP_200_OK)

class UserProfileView(APIView):
	serializer_class = UserProfileSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

	def get(self, request):
		if request.data.get("username"):
			user = CustomUser.objects.get(username=request.data["username"])
		else:
			user = request.user
		serializer = UserProfileSerializer(user)
		return Response(serializer.data, HTTP_200_OK)

class AddFilmView(APIView):
	permission_classes= [IsAuthenticated, ]

	def post(self, request):
		film = Film.objects.get(name=request.data["name"])
		request.user.films_watched.add(film)
	
		return Response(HTTP_200_OK)

class FollowView(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request):
		follower = request.user
		followed_username = request.data.get('username')

		try:
			the_followed = CustomUser.objects.get(username=followed_username)
			if follower == the_followed:
				return Response('you cannot follow yourself')
			
			for f in the_followed.followed.all():
				if f.follower == follower:
					return Response('already following user')

		except CustomUser.DoesNotExist:
			return Response('user does not exist')
		Following.objects.create(follower=follower, the_followed=the_followed)
		return Response( f"you are now following {followed_username}",HTTP_200_OK)


class UnFollowView(APIView):
	permission_classes = [IsAuthenticated, ]

	def delete(self, request):
		unfollower = request.user 
		unfollowed = request.data.get('username')

		if unfollower == unfollowed:
			return Response("you can't unfollow yourself")

		try:
			connection = Following.objects.get(follower=follower, following=following)
			connection.delete()
			return Response(HTTP_204_NO_CONTENT)
		except:
			return Response('Not Following User')

class LikeView(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request):
		film = Film.objects.get(name=request.data["name"])
		new_like, created = Like.objects.get_or_create(user=request.user, film=film)
		if not created:
			return Response("already liked")
		else:
			return Response("liked", HTTP_200_OK)