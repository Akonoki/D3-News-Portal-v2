import django_filters

from .models import Post, User, Author
from django_filters import FilterSet, CharFilter, RangeFilter, DateFromToRangeFilter


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {'title': ['icontains'],
                  }


class DateFilter(FilterSet):
    time_creation = DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = ['time_creation']


class AuthorFilter(FilterSet):
    username = CharFilter()

    class Meta:
        model = Author
        fields = ['user_relation__username']
