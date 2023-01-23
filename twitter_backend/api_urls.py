from rest_framework.routers import DefaultRouter
from users.apis import AuthViewSet

default_router = DefaultRouter(trailing_slash=False)
default_router.register("auth", AuthViewSet, basename="auth")

urlpatterns = default_router.urls


