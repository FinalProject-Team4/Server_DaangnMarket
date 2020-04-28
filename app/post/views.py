from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from post.filters import PostSearchFilter, PostFilter, PostDetailFilter

from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    GenericAPIView,
    UpdateAPIView
)
from config.c import LargeResultsSetPagination
from post.models import Post, SearchedWord, PostLike, PostImage
from post.serializers import (
    PostCreateSerializer,
    SearchedWordSerializer,
    PostSerializer, PostLikeSerializer
)
from post.swaggers import (
    decorated_post_create_update_api
)

User = get_user_model()


class PostListAPI(ListAPIView):
    """
    게시글 조회

    (+ 거래 동네, + 카테고리)
    ### GET _/post/list/_
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_class = PostFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering = ('-updated',)


class PostDetailAPI(GenericAPIView):
    """
    게시글 상세 정보

    ### GET _/post/detail/_
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_class = PostDetailFilter
    pagination_class = None

    def get(self, request, *args, **kwargs):
        # exceptions
        post = self.filter_queryset(self.queryset)[0]
        post.view_count += 1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostCreateUpdateDestroy(ModelViewSet):
    queryset = Post.objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        게시 정보 조회

        ### GET _/post/_
        """
        return super(PostCreateUpdateDestroy, self).retrieve(request, *args, **kwargs)

    @method_decorator(decorator=decorated_post_create_update_api)
    def create(self, request, *args, **kwargs):
        """
        게시물 생성

        ### POST _/post/_
        """
        return super(PostCreateUpdateDestroy, self).create(request, *args, **kwargs)

    @method_decorator(decorator=decorated_post_create_update_api)
    def partial_update(self, request, *args, **kwargs):
        """
        게시물 수정

        ### PATCH _/post/_
        """
        return super(PostCreateUpdateDestroy, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        게시물 삭제

        ### DELETE _/post/_
        """
        return super(PostCreateUpdateDestroy, self).destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        photos = self.request.data.getlist('photos')
        for photo in photos:
            PostImage.objects.create(post=post, photo=photo)

    def get_object(self):
        qs = self.get_queryset()
        return qs.filter(pk=self.request.data['post_id']).get()


class SearchAPI(ListAPIView):
    """
    게시글 검색

    ### GET _/post/search/_
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_class = PostSearchFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering = ('-updated',)


class PostLikeSave(CreateAPIView):
    """
    좋아요 저장

    ### POST _/post/like/_
    """
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data['post_id']
        post = Post.objects.get(pk=post_id)
        post_like_qs = PostLike.objects.filter(post=post, author=user)
        if post_like_qs.exists():
            post_like_qs.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            like = PostLike.objects.create(post=post, author=user)
            serializer = self.get_serializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostLikeList(ListAPIView):
    """
    좋아요 리스트

    ### GET _/post/like/list/_
    """
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        list = PostLike.objects.filter(author=user)
        return list
