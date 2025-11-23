from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views


urlpatterns = [
    path('user/register/', views.UserRegistrationApiView.as_view(), name='register'),
    path('user/login/', views.UserLoginApiView.as_view(), name='login'),
    path('user/logout/', views.UserLogoutView.as_view(), name='logout'),
    path('user/active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('', views.activate, name = 'activate'),
    path('follow/', views.FollowerView.as_view(), name='follow-user'),
    path('followers/', views.FollowerView.as_view(), name='get-followers'),
    path('followers/manage/', views.FollowerView.as_view(), name='manage-followers'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', views.CustomResetPasswordRequestToken.as_view(), name='password-reset'),
    path('password/reset/confirm/', views.CustomResetPasswordConfirm.as_view(), name='password-reset-confirm'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('people-you-may-know/', views.PeopleYouMayKnowView.as_view(), name='people-you-may-know'),
]



