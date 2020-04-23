from django.db.models import Q
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter

from post.models import Post


class PostSearchFilter(FilterSet):
    word = CharFilter(
        method='filter_word', required=True, help_text='검색어')
    dong_id = CharFilter(
        method='filter_locate', help_text='내 동네 설정 e.g. ?locate=1011,6971,2341')

    class Meta:
        model = Post
        fields = ['word', 'dong_id']

    def filter_word(self, qs, name, value):
        return qs.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )

    def filter_locate(self, qs, name, value):
        locates = [L for L in value.strip().split(',') if L]
        return qs.filter(showed_locate__in=locates)


class PostFilter(FilterSet):
    dong_id = CharFilter(
        field_name='showed_locate', lookup_expr='exact', help_text='거래 동네')
    category = CharFilter(
        field_name='category', lookup_expr='exact', help_text='카테고리')

    class Meta:
        model = Post
        fields = ['dong_id', 'category']


class PostDetailFilter(FilterSet):
    post_id = NumberFilter(
        field_name='pk', lookup_expr='exact', required=True, help_text='게시글 번호')

    class Meta:
        model = Post
        fields = ['post_id']
