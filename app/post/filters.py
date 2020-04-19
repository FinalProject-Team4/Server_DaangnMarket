from django.db.models import Q
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter

from post.models import Post


class PostSearchFilter(FilterSet):
    word = CharFilter(
        method='filter_word', required=True, help_text='검색어')
    locate = CharFilter(
        field_name='showed_locate', lookup_expr='exact', help_text='내 동네 설정')

    class Meta:
        model = Post
        fields = ['word', 'locate']

    def filter_word(self, qs, name, value):
        return qs.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )


class PostFilter(FilterSet):
    locate = CharFilter(
        field_name='showed_locate', lookup_expr='exact', help_text='거래 동네')
    category = CharFilter(
        field_name='category', lookup_expr='exact', help_text='카테고리')

    class Meta:
        model = Post
        fields = ['locate', 'category']


class PostDetailFilter(FilterSet):
    post_id = NumberFilter(
        field_name='pk', lookup_expr='exact', required=True, help_text='게시글 번호')

    class Meta:
        model = Post
        fields = ['post_id']
