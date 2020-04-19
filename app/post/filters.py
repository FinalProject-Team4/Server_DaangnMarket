import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet, CharFilter

from post.models import Post


class PostWithLocateFilter(FilterSet):
    word = django_filters.CharFilter(
        method='filter_word', required=True, help_text='검색어')
    locate = CharFilter(
        field_name='showed_locate__id', lookup_expr='exact', help_text='내 동네 설정')

    class Meta:
        model = Post
        fields = ['word', 'locate']

    def filter_word(self, qs, name, value):
        return qs.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )
