import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet, CharFilter

from post.models import Post


class PostWithLocateFilter(FilterSet):
    word = django_filters.CharFilter(
        method='filter_word')
    locate = CharFilter(
        field_name='showed_locate__id', lookup_expr='exact')

    class Meta:
        model = Post
        fields = ['word', 'locate']

    def filter_word(self, qs, name, value):
        return qs.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )
