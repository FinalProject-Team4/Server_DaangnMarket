from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, JSONParser

from location.models import Locate
from post.models import Post
from post.serializers import PostImageCreateSerializer, PostListSerializer, PostDetailSerializer, PostingSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404


class ApiPostList(ListAPIView):
    '''
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
    '''
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.all().order_by('-created')


class ApiPostListWithGPS(ListAPIView):
    '''
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
    '''
    serializer_class = PostListSerializer

    def get_queryset(self):
        try:
            locate_id = self.request.query_params.get('locate')
            print('locate_id : ', locate_id)
            locate = Locate.objects.get(id=locate_id)
            print('locate_id : ', locate_id)
        except:
            raise ValidationError(['HTTP_400_BAD_REQUEST'])

        objs = Post.objects.filter(locate=locate).order_by('-created')
        return objs


class ApiPostListWithCate(ListAPIView):
    '''
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
    '''
    serializer_class = PostListSerializer

    def get_queryset(self):
        try:
            category = self.request.query_params.get('category')
        except:
            raise ValidationError(status=status.HTTP_400_BAD_REQUEST)
        objs = Post.objects.filter(category=category).order_by('-created')
        return objs


# post detail
class ApiPostDetail(RetrieveAPIView):
    serializer_class = PostDetailSerializer

    def get_object(self):
        pk = self.request.query_params.get('post_id', None)
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj = get_object_or_404(Post, pk=pk)
        obj.view_count = obj.view_count + 1
        obj.save()
        return obj


# posting
class ApiPostCreate(CreateAPIView):
    serializer_class = PostingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = User.objects.get(username='admin')
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post edit


# post image upload
class ApiPostImageUpload(CreateAPIView):
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
