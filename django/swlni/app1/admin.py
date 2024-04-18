from django.contrib import admin
from .models import Topic, Article
# Register your models here.


admin.site.register(Topic)
admin.site.register(Article)
'''
In summary, while both methods accomplish the same task, the @admin.register() 
decorator provides a more modern and structured approach to registering models 
with the Django admin interface, allowing for better organization and customization.


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['topic_id', 'topic_title']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['article_id', 'article_title', 'topic']'''