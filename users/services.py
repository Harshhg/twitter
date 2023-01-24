from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import exceptions

from common.services import send_email
from users.models import User, EmailToken
from django.conf import settings
from django.core.mail import send_mail


def generate_token():
    token_length = settings.USER_EMAIL_VERIFICATION.get("TOKEN_LENGTH")
    token = get_random_string(length=token_length)
    return token


def send_verification_email(user, email_token):
    subject = 'Verify Your Email !'
    verification_link = f"https://app.com?email={user.email}&token={email_token.token}"
    message = f"Hey! {user.full_name}, Please click on the below link to verify your email - \n\n {verification_link}"
    send_email(subject, message, to_email=[user.email])


def create_user_account(**kwargs):
    user = User.objects.create_user(**kwargs)
    email_token = EmailToken.objects.create(email=user.email, token=generate_token())

    # todo: make it async
    send_verification_email(user, email_token)
    return user


def get_and_authenticate_user(email, password):
    user = authenticate(email=email, password=password)
    if user is None:
        raise exceptions.NotAuthenticated("Invalid username/password. Please try again!")
    if not user.is_verified():
        raise exceptions.AuthenticationFailed("Email is not verified !")
    return user


def verify_email(email, token):
    email_token = EmailToken.objects.filter(email=email, token=token, is_verified=False).first()
    if not email_token:
        raise exceptions.ValidationError("Invalid email or token !")

    User.objects.filter(email=email).update(verified_on=timezone.now())
    email_token.is_verified = True
    email_token.save()
