from django.db import models

# Create your models here.
class Topic(models.Model):
    topic_id = models.IntegerField(primary_key=True)
    topic_title = models.CharField(max_length=100)

    def __str__(self):
        return self.topic_title

class Article(models.Model):
    article_id = models.IntegerField(primary_key=True)
    article_title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.article_title