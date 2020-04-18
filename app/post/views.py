from django.db.models import Q
from django.shortcuts import render
from django.utils.datastructures import MultiValueDict
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

from location.models import Locate
from members.models import User
from post.models import Post, SearchedWord
from post.serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer, PostImageUploadSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404, GenericAPIView

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
        # exceptions
        try:
            category = self.request.query_params.get('category')
            locate_id = self.request.query_params.get('locate')
            locate = Locate.objects.get(id=locate_id)
        except:
            raise ValidationError(status=status.HTTP_400_BAD_REQUEST)
        objs = Post.objects.filter(category=category, showed_locate=locate).order_by('-created')
        return objs


# @@ 문서 정리
class ApiPostDetail(RetrieveAPIView):
    """
    게시글 상세 정보

    ### GET /post/detail/
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
    게시물 검색

    ### GET /post/search/
    """
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        '''
        user가 갖고 있는 'selected_locations_verified' 에서
        'activated' 되어 있는 'locate'을 중심으로 'distance'값 안에 있는
        모든 'locate'들이 갖고 있는 Post들 출력
        '''

        ret = []

        user = self.request.user
        if user.is_anonymous:
            user = None

        # 검색어 저장
        word = self.request.query_params.get('word')
        txt_list = word.split()

        for txt in txt_list:
            w, _ = SearchedWord.objects.get_or_create(user=user, content=txt)
            w.count = w.count + 1
            w.save()

        # 유저가 갖고 있는 로케이션
        for loc in user.selected_locations_verified.all():
            if loc.activated:
                user_select_location = loc
                distance = str(user_select_location.distance)
                pnt = user_select_location.locate.latlng

                # 유저가 갖고 있는 로케이션의 범위네 로케이션들
                locates = Locate.objects.filter(
                    latlng__distance_lt=(pnt, D(m=distance)),
                ).annotate(distance=Distance(pnt, 'latlng')).order_by('distance')

                # 단어 검색
                for L in locates:
                    post_list = L.posts.filter(
                        Q(title__icontains=word) |
                        Q(content__icontains=word)
                    ).distinct()
                    ret += post_list

        return ret
