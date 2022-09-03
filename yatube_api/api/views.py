from rest_framework import viewsets, filters

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Post, Group
from .serializers import (FollowSerializer,
                          PostSerializer,
                          GroupSerializer,
                          CommentSerializer)
from .permissions import IsAuthorOrReadOnly
from .viewsets import ListCreateViewSet


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """
    Viewset for requests to api/v1/posts endpoints.
    Allows editing only to post authors.
    Supports limit-offset pagination.
    """

    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for requests to api/v1/groups endpoints.
    Only allows for GET-requests.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for requests to api/v1/{post_id}/comments endpoints.
    Allows editing only to comment authors.
    """

    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(ListCreateViewSet):
    """
    Viewset for requests to api/v1/follow endpoints.
    Supports search by username of followed users.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username', )

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
