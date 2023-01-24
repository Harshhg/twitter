from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post
from posts.serializers import PostListSerializer, PostCreateSerializer
from posts.services import like_post, unlike_post


class PostViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_archived=False)
        if self.action == "list":
            queryset = queryset.filter(user=self.request.user)
        if self.action == "like":
            queryset = queryset.exclude(user=self.request.user)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        response = self.get_paginated_response(serializer.data)
        return Response(response.data)

    def create(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"success": True}, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=True)
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        like_post(request.user, post)
        return Response({"success": True})

    @action(methods=["POST"], detail=True)
    def unlike(self, request, *args, **kwargs):
        post = self.get_object()
        unlike_post(request.user, post)
        return Response({"success": True})
