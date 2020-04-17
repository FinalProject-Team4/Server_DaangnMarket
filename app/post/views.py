from django.db.models import Q
from django.shortcuts import render
from django.utils.datastructures import MultiValueDict
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.gis.db.models.functions import Distance

from django.contrib.gis.measure import D
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

from location.models import Locate
from members.models import User
from post.models import Post
from post.serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer, PostImageUploadSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404

from post.swaggers import decorated_post_image_upload_api, decorated_post_create_api


class ApiPostList(ListAPIView):
    """
    post 목록 조회

    ---
    ## /post/list/
    ## 내용
        - username: 작성자
        - title: 게시글 제목
        - content: 게시글 내용
        - category: 상품 분류
        - view_count: 조회수
        - updated: 수정일
        - postimage_set: 게시글에 있는 사진
            - photo: 사진 파일 url
            - post: 사진이 속해있는 게시판
    """
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.all().order_by('-created')


class ApiPostListWithGPS(ListAPIView):
    """
    특정 지역의  post 목록 조회

    ---
    ## /post/list/gps/
    ## Parameters
        - locate: 동 id
    ## 내용
        - username: 작성자
        - title: 게시글 제목
        - content: 게시글 내용
        - category: 상품 분류
        - view_count: 조회수
        - updated: 수정일
        - postimage_set: 게시글에 있는 사진
            - photo: 사진 파일 url
            - post: 사진이 속해있는 게시판
    """
    serializer_class = PostListSerializer

    def get_queryset(self):
        try:
            locate_id = self.request.query_params.get('locate')
            print('locate_id : ', locate_id)
            locate = Locate.objects.get(id=locate_id)
            print('locate_id : ', locate_id)
        except:
            raise ValidationError(['HTTP_400_BAD_REQUEST'])

        objs = Post.objects.filter(showed_locate=locate).order_by('-created')
        return objs


class ApiPostListWithCate(ListAPIView):
    """
    특정 카테고리의 Post 목록

    ---
    ## /post/list/category/
    ## Parameters
     - category: 분류 이름(ex ditital)
    ## 내용
        - username: 작성자
        - title: 게시글 제목
        - content: 게시글 내용
        - category: 상품 분류
        - view_count: 조회수
        - updated: 수정일
        - postimage_set: 게시글에 있는 사진
            - photo: 사진 파일 url
            - post: 사진이 속해있는 게시판
    """
    serializer_class = PostListSerializer

    def get_queryset(self):
        try:
            category = self.request.query_params.get('category')
            locate_id = self.request.query_params.get('locate')
            locate = Locate.objects.get(id=locate_id)
        except:
            raise ValidationError(status=status.HTTP_400_BAD_REQUEST)
        objs = Post.objects.filter(category=category, showed_locate=locate).order_by('-created')
        return objs


# post detail
class ApiPostDetail(RetrieveAPIView):
    """
    post

    ---
    ## /post/detail/
    ## Parameters
        - post_id: 상세정보를 볼 post id값
    ## 내용
        - username: 작성자
        - title: 게시글 제목
        - content: 게시글 내용
        - category: 상품 분류
        - view_count: 조회수
        - updated: 수정일
        - postimage_set: 게시글에 있는 사진
            - photo: 사진 파일 url
            - post: 사진이 속해있는 게시판
    """
    serializer_class = PostDetailSerializer

    def get_object(self):
        pk = self.request.query_params.get('post_id', None)
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj = get_object_or_404(Post, pk=pk)
        obj.view_count = obj.view_count + 1
        obj.save()
        return obj


@method_decorator(name='post', decorator=decorated_post_create_api)
class ApiPostCreate(CreateAPIView):
    """
    게시글 생성

    POST /post/create/
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


# post edit

@method_decorator(name='post', decorator=decorated_post_image_upload_api)
class ApiPostImageUpload(CreateAPIView):
    """
    상품 이미지 업로드

    ### POST /post/image/upload/
    """
    queryset = Post.objects.all()
    serializer_class = PostImageUploadSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

# class ApiSearch(ListAPIView):
#     serializer_class = PostListSerializer
#
#     def get_queryset(self):
#         word = self.request.query_params.get('word')
#         txt_list = word.split()
#         for txt in txt_list:
#             w = RecommendWord.objects.get_or_create(content=txt)
#             w.count = w.count + 1
#             w.save()
#         post_list = Post.objects.filter(
#             Q(title__icontains=word) |
#             Q(content__icontains=word)
#         ).distinct().order_by('-created')
#         return post_list


# class ApiRecommendWord(ListAPIView):
#     serializer_class = RecommendWordSerializer
#
#     def get_queryset(self):
#         words = RecommendWord.objects.all().order_by('count')[:10]
#         return words
