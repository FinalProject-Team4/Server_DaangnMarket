from rest_framework import serializers

from post.models import Post, PostImage, SearchedWord


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
    id = serializers.IntegerField(
        read_only=True, help_text='게시물 번호')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category', 'price', 'locate', 'showed_locate']
        examples = {
            'id': '1',
            'title': '아이패드 신형',
            'content': '싸게 팝니다',
            'category': 'digital',
            'price': '1000',
            'locate': 435,
            'showed_locate': [
                1234,
                2346
            ],
        }


class PostImageListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.photo.url


# 상품 이미지 업로드
class PostImageUploadSerializer(serializers.ModelSerializer):
    post_id = serializers.CharField(
        source='id', help_text='게시물 번호')
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


# 게시물 검색 저장
class SearchedWordSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user
        w, _ = SearchedWord.objects.get_or_create(user=user, content=validated_data['content'])
        w.count = w.count + 1
        return w

    class Meta:
        model = SearchedWord
        fields = ('content', 'count')
