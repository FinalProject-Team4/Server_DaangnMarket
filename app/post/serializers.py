from rest_framework import serializers

from post.models import Post, PostImage


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
            'postimage_set',
        )


class PostingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'price', 'locate', 'showed_locate']


class PostImageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ['photo', 'post']