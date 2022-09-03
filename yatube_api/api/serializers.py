from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow
from .custom_fields import Base64ImageField


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer class for Post objects.
    Uses Base64ImageField custom field for image serializing.
    """

    author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer class for Comment objects.
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer class for Comment objects.
    """

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer class for Follow objects.
    Uses UniqueTogetherValidator to disallow
    creating a copy of already existing Follow.
    Following field is also validated to disallow following oneself.
    """

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Вы уже подписаны на этого автора!'
            )
        ]

    def validate_following(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return value
