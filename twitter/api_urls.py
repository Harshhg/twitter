from rest_framework.routers import DefaultRouter

from twitter.posts.apis import PostViewSet, FeedViewSet
from twitter.users.apis import AuthViewSet

default_router = DefaultRouter(trailing_slash=False)

default_router.register("auth", AuthViewSet, basename="auth")
default_router.register("post", PostViewSet, basename="posts")
default_router.register("feed", FeedViewSet, basename="feeds")

urlpatterns = default_router.urls


