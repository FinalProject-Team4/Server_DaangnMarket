from rest_framework import serializers

from post.models import Post, PostImage


class PostListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username')

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
            'postimage_set',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username')

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
            'postimage_set',
        )


class PostingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'price', 'locate']


class PostImageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ['photo', 'post']