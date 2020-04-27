from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from django_filters.rest_framework import DjangoFilterBackend
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
    decorated_post_create_api
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


class ApiPostUpdate(UpdateAPIView):
    serializer_class = PostSerializer

    def update(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        state = request.data.get('state')
        post = Post.objects.get(pk=post_id)
        post.state = state
        post.save()
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPostListOther(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id', 0)
        post = Post.objects.get(pk=post_id)
        list = Post.objects.filter(author=post.author)
        return list


class ApiPostListUser(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        username = self.request.query_params.get('username', 0)
        user = User.objects.get(username=username)
        list = Post.objects.filter(author=user)
        return list


@method_decorator(name='post', decorator=decorated_post_create_api)
class PostCreateAPI(CreateAPIView):
    """
    게시글 생성

    ### POST _/post/create/_
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        photos = self.request.data.getlist('photos')
        for photo in photos:
            PostImage.objects.create(post=post, photo=photo)


# TODO: post edit

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


class SearchSaveAPI(CreateAPIView):
    """
    게시글 검색 저장

    ### POST _/post/search/save/_
    """
    queryset = SearchedWord.objects.all()
    serializer_class = SearchedWordSerializer
    permission_classes = [IsAuthenticated]


class PostLikeSave(CreateAPIView):
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
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        list = PostLike.objects.filter(author=user)
        return list
