import django_filters
from django_filters.filters import CharFilter
from .models import Article, Topic

class TopicFilter(django_filters.FilterSet):
    topic_title = CharFilter(field_name='topic_title', lookup_expr='icontains')

    class Meta:
        model = Topic
        fields = []


class ArticleFilter(django_filters.FilterSet):
    article_title = CharFilter(field_name='article_title', lookup_expr='icontains')

    class Meta:
        model = Article
        fields = []