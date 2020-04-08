from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import models

from post.models import Post, PostImage, RecommendWord


class PostListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username')
    address = serializers.CharField(source='locate.dong')

    class Meta:
        model = Post
        depth = 1
        fields = (
            'id',
            'username',
            'title',
            'content',
            'category',
            'view_count',
            'updated',
            'address',
            'price',
            'state',
            'postimage_set',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username')
    address = serializers.CharField(source='locate.dong')

    class Meta:
        model = Post
        depth = 1
        fields = (
            'id',
            'username',
            'title',
            'content',
            'category',
            'view_count',
            'updated',
            'address',
            'price',
            'state',
            'postimage_set',
        )


class PostingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category', 'price', 'locate', 'showed_locate']


class PostImageListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        instances = [
            PostImage(**attrs) for attrs in validated_data
        ]
        PostImage.objects.bulk_create(instances)
        return PostImage.objects.all()


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['photo', 'post']
        list_serializer_class = PostImageListSerializer


class RecommendWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendWord
        fields = ['content']
