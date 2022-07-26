
from django.urls import path
from account.views import UserRegistrationView, UserLoginView, CheckWeather, LogoutView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name="register"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('weather/',CheckWeather.as_view(),name="weather"),
    path('logout/', LogoutView.as_view(), name='logout'),
]