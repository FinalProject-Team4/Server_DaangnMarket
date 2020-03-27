from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.datastructures import MultiValueDict
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.gis.db.models.functions import Distance

from django.contrib.gis.measure import D
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, JSONParser

from location.models import Locate
from post.models import Post
from post.serializers import PostImageCreateSerializer, PostListSerializer, PostDetailSerializer, PostingSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404


# post 목록
class ApiPostList(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.all().order_by('-created')


# 위치
class ApiPostListWithGPS(ListAPIView):
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


# 카테고리
class ApiPostListWithCate(ListAPIView):
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





