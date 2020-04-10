from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from post.models import Post, PostImage, RecommendWord


# -> PostSerializer
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
            'post_images',
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
            'post_images',
        )


class PostCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category', 'price', 'locate', 'showed_locate']


class PostImageUploadSerializer(serializers.ModelSerializer):
    photos = StringRelatedField(source='post_images', many=True)
    post_id = serializers.CharField(source='id')

    class Meta:
        model = Post
        fields = ('post_id', 'photos')

    def create(self, validated_data):
        post_id = validated_data['post_id']
        photos = validated_data.pop('photos')
        post = Post.objects.get(id=post_id)
        for photo in photos:
            PostImage.objects.create(post=post, **photo)
        return post

    def to_internal_value(self, data):
        ret = {
            'post_id': data.get('post_id'),
            'photos': [{'photo': photo} for photo in data.getlist('photos')]
        }
        return ret


class RecommendWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendWord
        fields = ['content']
