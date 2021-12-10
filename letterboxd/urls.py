from django.conf.urls import url
from django.urls import path, include
from letterboxd import views
from rest_framework.routers import DefaultRouter



'''router = DefaultRouter()
router.register(r'signup', views.SignUpView.as_view(), name="signup")
router.register(r'login', views.LoginView.as_view(), name="login")'''
urlpatterns=[
	path('signup/', views.SignUpView.as_view(), name='signup'),
	path('login/', views.LoginView.as_view(), name='login'),
	path('list_film/', views.ListFilmView.as_view(), name='list_film'),
	path('reviews/', views.ReviewView.as_view(), name='reviews'),
	path('userlist/', views.UserListView.as_view(), name='userlist'),
	path('userprofile/', views.UserProfileView.as_view(), name='userprofile'),
	path('addfilm/', views.AddFilmView.as_view(), name='addfilm'),
	path('follow/', views.FollowView.as_view(), name='follow'),
	path('like/', views.LikeView.as_view(), name='like'), 
	path('listfollowing/', views.ListFollowingView.as_view(), name='listfollowing'),
	path('listfollowers/', views.ListFollowersView.as_view(), name='listfollowers')
]