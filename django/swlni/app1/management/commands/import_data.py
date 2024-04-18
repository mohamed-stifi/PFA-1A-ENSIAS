# import_data.py

import csv
from django.core.management.base import BaseCommand
from app1.models import Topic, Article

class Command(BaseCommand):
    help = '''Import data from CSV files
            to run :
                python manage.py import_data ../topic_table.csv ../article_table.csv
    '''

    def add_arguments(self, parser):
        parser.add_argument('topic_csv', type=str, help='C:\\Users\\lenovo\\Desktop\\PFA\\topic_table.csv')
        parser.add_argument('article_csv', type=str, help='C:\\Users\\lenovo\\Desktop\\PFA\\article_table.csv')

    def handle(self, *args, **kwargs):
        topic_csv = kwargs['topic_csv']
        article_csv = kwargs['article_csv']

        # Import Topics
        with open(topic_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                topic_id = int(row['topic_id'])
                topic_title = row['topic_title']
                Topic.objects.create(topic_id=topic_id, topic_title=topic_title)

        self.stdout.write(self.style.SUCCESS('Topics imported successfully.'))

        # Import Articles
        with open(article_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                article_id = int(row['article_id'])
                article_title = row['article_title']
                topic_id = int(row['topic_id'])
                topic = Topic.objects.get(topic_id=topic_id)
                Article.objects.create(article_id=article_id, article_title=article_title, topic=topic)

        self.stdout.write(self.style.SUCCESS('Articles imported successfully.'))
