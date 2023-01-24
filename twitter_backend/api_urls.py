from rest_framework.routers import DefaultRouter

from posts.apis import PostViewSet
from users.apis import AuthViewSet

default_router = DefaultRouter(trailing_slash=False)

default_router.register("auth", AuthViewSet, basename="auth")
default_router.register("post", PostViewSet, basename="posts")

urlpatterns = default_router.urls


