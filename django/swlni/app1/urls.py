from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name = 'home'),
    path("topic/<str:topic_id>", views.read_articles_of_topic, name = 'articles'),
    path("recommend/", views.recommend_view, name = 'recommend'),
]