from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter

from location.filters import LocationFilter
from location.models import Locate
from post.models import Post

User = get_user_model()


class PostSearchFilter(FilterSet):
    word = CharFilter(
        method='filter_word', required=True, help_text='검색어')
    locate = CharFilter(
        method='filter_locate', help_text='내 동네 설정 e.g. ?locate=1011,6971,2341')

    class Meta:
        model = Post
        fields = ['word', 'locate']

    def filter_word(self, qs, name, value):
        return qs.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )

    def filter_locate(self, qs, name, value):
        locates = [L for L in value.strip().split(',') if L]
        return qs.filter(showed_locates__in=locates)


class PostFilter(FilterSet):
    locate = CharFilter(
        method='range_filter', lookup_expr='exact', help_text='대표 거래 동네')
    category = CharFilter(
        method='filter_category', lookup_expr='exact', help_text='카테고리')
    distance = CharFilter(
        method='range_filter', lookup_expr='exact', help_text='범위')
    username = CharFilter(
        method='filter_user', lookup_expr='exact', help_text='작성자')

    def filter_user(self, qs, name, value):
        user = User.objects.get(username=value)
        return qs.filter(author=user)

    def filter_category(self, qs, name, value):
        categories = [C for C in value.strip().split(',') if C]
        return qs.filter(category__in=categories)

    def range_filter(self, qs, name, value):
        locate_data = {
            'locate': self.data.get('locate'),
            'distance': self.data.get('distance')
        }
        locates = LocationFilter(data=locate_data)
        locates.is_valid()
        user_locations = locates.filter_queryset(Locate.objects.all())
        ret = qs.filter(showed_locates__in=user_locations)
        ret = ret.distinct()
        return ret

    class Meta:
        model = Post
        fields = ['locate', 'category', 'distance']


class PostDetailFilter(FilterSet):
    post_id = NumberFilter(
        field_name='pk', lookup_expr='exact', required=True, help_text='게시글 번호')

    class Meta:
        model = Post
        fields = ['post_id']
