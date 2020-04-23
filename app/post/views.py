from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDict
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from rest_framework.filters import OrderingFilter

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

from location.models import Locate
from post.filters import PostSearchFilter, PostFilter, PostDetailFilter
from post.models import Post, SearchedWord, PostLike
from post.serializers import (
    PostCreateSerializer,
    PostImageUploadSerializer,
    SearchedWordSerializer,
    PostSerializer, PostLikeSerializer)
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    GenericAPIView, UpdateAPIView)

from post.swaggers import (
    decorated_post_image_upload_api,
    decorated_post_create_api)

User = get_user_model()


class ApiPostList(ListAPIView):
    """
    게시글 조회

    (+ 거래 동네, + 카테고리)
    ### GET _/post/list/gps/_
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
        serializer = self.serializer_class(post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPostListOther(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id', 0)
        post = Post.objects.get(pk=post_id)
        list = Post.objects.filter(author=post.author)
        return list


@method_decorator(name='post', decorator=decorated_post_create_api)
class ApiPostCreate(CreateAPIView):
    """
    게시글 생성

    ### POST /post/create/
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ApiPostCreateLocate(CreateAPIView):
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        locate_id = request.data.get('locate')
        distance = request.data.get('distance', 1000)
        data = request.data.copy()

        try:
            dong = Locate.objects.get(id=locate_id)
        except Locate.DoesNotExist:
            print('Locate.DoesNotExist')
            raise ValidationError(['There are no dong_id'])

        pnt = dong.latlng
        locates = Locate.objects.filter(
            latlng__distance_lt=(pnt, D(m=distance)),
        ).annotate(distance=Distance(pnt, 'latlng')).order_by('distance')
        showed_locate = []
        for locate in locates:
            showed_locate.append(f'{locate.id}')
        data.update(MultiValueDict({'showed_locate': showed_locate}))

        serializer = self.get_serializer(data=data)
        user = User.objects.get(username='admin')
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: post edit

@method_decorator(name='post', decorator=decorated_post_image_upload_api)
class PostImageUploadAPI(CreateAPIView):
    """
    상품 이미지 업로드

    ### POST /post/image/upload/
    """
    queryset = Post.objects.all()
    serializer_class = PostImageUploadSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)


class SearchAPI(ListAPIView):
    """
    게시글 검색

    ### GET /post/search/
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_class = PostSearchFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering = ('-updated',)


class SearchSaveAPI(CreateAPIView):
    """
    게시글 검색 저장

    ### POST /post/search/save/
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


