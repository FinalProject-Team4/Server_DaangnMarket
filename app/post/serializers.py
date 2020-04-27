from rest_framework import serializers

from location.filters import LocationFilter
from location.models import Locate
from post.models import Post, PostImage, SearchedWord, PostLike


class PostSerializer(serializers.ModelSerializer):
    photos = serializers.StringRelatedField(
        source='post_images', read_only=True, many=True, help_text='상품 사진')

    class Meta:
        model = Post
        depth = 1
        fields = (
            'id',
            'username',
            'title',
            'content',
            'address',
            'category',
            'view_count',
            'updated',
            'likes',
            'price',
            'state',
            'photos',
        )
        read_only_fields = ('id', 'username', 'likes', 'updated', 'view_count', 'address')


class PostCreateSerializer(PostSerializer):
    distance = serializers.CharField(
        write_only=True, help_text='동네 범위')

    def validate(self, attrs):
        user = self.context.get('request').user
        activated = user.user_selected_locations.filter(activated=True).get()
        locate_data = {
            'locate': activated.locate,
            'distance': attrs.pop('distance')
        }
        locates = LocationFilter(data=locate_data)
        locates.is_valid()
        attrs['showed_locates'] = locates.filter_queryset(Locate.objects.all())
        attrs['address'] = activated.locate.address
        return attrs

    class Meta(PostSerializer.Meta):
        model = Post
        fields = PostSerializer.Meta.fields + ('distance',)


class PostImageListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.photo.url


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
    post = PostSerializer(read_only=True)

    class Meta:
        model = PostLike
        depth = 1
        fields = (
            'author',
            'post',
        )
