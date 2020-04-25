from rest_framework import serializers

from location.filters import LocationFilter
from location.models import Locate
from post.models import Post, PostImage, SearchedWord, PostLike


class PostSerializer(serializers.ModelSerializer):
    photos = serializers.StringRelatedField(
        source='post_images', read_only=True,  many=True, help_text='상품 사진')
    showed_locates = serializers.PrimaryKeyRelatedField(
        read_only=True,  many=True, help_text='포스트 될 동네 ID'
    )

    class Meta:
        model = Post
        depth = 1
        fields = (
            'id',
            'username',
            'title',
            'content',
            'category',
            'address',
            'view_count',
            'updated',
            'price',
            'showed_locates',
            'state',
            'photos',
        )
        read_only_fields = ('id', 'username', 'updated', 'view_count')


class PostCreateSerializer(PostSerializer):
    dong_id = serializers.CharField(
        write_only=True, help_text='내 동네 동 ID 값')
    distance = serializers.CharField(
        write_only=True, help_text='동네 범위')

    def validate(self, attrs):
        locate_data = {
            'dong_id': attrs.pop('dong_id'),
            'distance': attrs.pop('distance')
        }
        locates = LocationFilter(data=locate_data)
        locates.is_valid()
        attrs['showed_locates'] = locates.filter_queryset(Locate.objects.all())
        return attrs

    class Meta(PostSerializer.Meta):
        model = Post
        fields = PostSerializer.Meta.fields + ('dong_id', 'distance')


class PostImageListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.photo.url


# 상품 이미지 업로드
class PostImageUploadSerializer(serializers.ModelSerializer):
    post_id = serializers.CharField(
        source='id', help_text='게시글 번호')
    photos = PostImageListingField(
        source='post_images', queryset=PostImage.objects.all(), many=True, help_text='상품 이미지 URIs')

    class Meta:
        model = Post
        fields = ('post_id', 'photos',)
        examples = {
            'post_id': '2',
            'photos': [
                'https://img_server.com/post_images/post_2/anna.jpeg',
                'https://img_server.com/post_images/post_3/elsa.jpeg',
            ]
        }

    def to_internal_value(self, data):
        ret = {
            'post_id': data.get('post_id'),
            'photos': [{'photo': photo} for photo in data.getlist('photos')]
        }
        return ret


# 게시글 검색 저장
class SearchedWordSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user
        w, _ = SearchedWord.objects.get_or_create(user=user, content=validated_data['content'])
        w.count = w.count + 1
        return w

    class Meta:
        model = SearchedWord
        fields = ('content', 'count')


class PostLikeSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')

    class Meta:
        model = PostLike
        depth = 1
        fields = (
            'author',
            'post',
        )
