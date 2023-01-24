from rest_framework import serializers
from posts.models import Post
from users.serializers import UserSerializer


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "created_at", "content", "likes_count"]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["content"]


class FeedSerializer(PostListSerializer):
    user = UserSerializer()

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ["user"]
