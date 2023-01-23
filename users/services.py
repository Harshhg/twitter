from django.contrib.auth import authenticate
from rest_framework import exceptions
from users.models import User


def create_user_account(**kwargs):
    user = User.objects.create_user(**kwargs)
    return user


def get_and_authenticate_user(email, password):
    user = authenticate(email=email, password=password)
    if user is None:
        raise exceptions.NotAuthenticated("Invalid username/password. Please try again!")
    if not user.is_verified():
        raise exceptions.AuthenticationFailed("Email is not verified !")
    return user
