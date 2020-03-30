from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.utils.datastructures import MultiValueDict
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.gis.db.models.functions import Distance

from django.contrib.gis.measure import D
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, JSONParser

from location.models import Locate
from post.models import Post, RecommendWord
from post.serializers import PostImageCreateSerializer, PostListSerializer, PostDetailSerializer, PostingSerializer, \
    RecommendWordSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404


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


class ApiPostCreate(CreateAPIView):
    """
    post 생성

    ---
    ## /post/create/
    ## 내용
        - title: 게시글 제목
        - content: 게시글 내용
        - category: 판매 상품 카테고리 분류
        - price: 판매 가격
        - locate: 게시글 게시 지역
    """
    serializer_class = PostingSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        user = User.objects.get(username='admin')
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPostCreateLocate(CreateAPIView):
    serializer_class = PostingSerializer

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


# post image upload
class ApiPostImageUpload(CreateAPIView):
    """
    post 이미지 업로드

    ---
    ## /post/image/upload/
    ## 내용
        - post_id: 게시글 id
        - photos: 사진 이미지들
    """
    serializer_class = PostImageCreateSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def create(self, request, *args, **kwargs):
        post = request.data.get('post_id')
        photos = request.data.getlist('photos')
        photo_result = []
        for photo in photos:
            data = {'post': post,
                    'photo': photo,
                    }
            serializer = PostImageCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                photo_result.append(serializer.data.get('photo'))
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        result = {'photos': photo_result}
        return Response(result, status=status.HTTP_201_CREATED)


class ApiSearch(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        word = self.request.query_params.get('word')
        txt_list = word.split()
        for txt in txt_list:
            w = RecommendWord.objects.get_or_create(content=txt)
            w.count = w.count + 1
            w.save()
        post_list = Post.objects.filter(
            Q(title__icontains=word) |
            Q(content__icontains=word)
        ).distinct().order_by('-created')
        return post_list


class ApiRecommendWord(ListAPIView):
    serializer_class = RecommendWordSerializer

    def get_queryset(self):
        words = RecommendWord.objects.all().order_by('count')[:10]
        return words
