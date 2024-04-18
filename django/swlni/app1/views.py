from django.shortcuts import render
from .models import Topic, Article
from .filters import TopicFilter, ArticleFilter
from django.core.paginator import Paginator
from .forms import RecommendrdForm
import pickle
import pandas as pd

# from qdrant_client import QdrantClient
# from qdrant_client.models import models
# from sentence_transformers import SentenceTransformer

# from .utils import load_data, load_vectors, prepare_data
# Create your views here.

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

articles = '../article_table.csv'
topics = '../topic_table.csv'

df_articles = pd.read_csv(articles)
df_topics = pd.read_csv(topics)

articles_title = df_articles['article_title'].tolist()
topics_title = df_topics['topic_title'].tolist()

articles_id = [str(i) for i in df_articles['article_id'].tolist()]
topics_id = [str(i) for i in df_topics['topic_id'].tolist()]

model_id = "sentence-transformers/distiluse-base-multilingual-cased-v2"
dim = 512

device = "cpu" #"cuda:0" # 

model = SentenceTransformer(model_id, device=device)

## Load
with open("../articles_faiss_index.pickle", "rb") as handle:
    articles_faiss_index = pickle.load(handle)

with open("../topics_faiss_index.pickle", "rb") as handle:
    topics_faiss_index = pickle.load(handle)

'''name = 'topic'

# create a vectorDB client
client = QdrantClient(":memory:")
client.recreate_collection(collection_name=f'{name}s_collection',
                           vectors_config=models.VectorParams(
                               size = 384, distance= models.Distance.COSINE
                           ))

# vectorized our data: create word embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# column = f'{name}_title'
data = f'../{name}_table.csv'
df = load_data(data)
docx, payload = prepare_data(df, name)

vectors = load_vectors(f'vectorized_{name}.pickle')

# stored in vectorDB collection
client.upload_collection(collection_name=f'{name}s_collection',
                        vectors= vectors,
                        payload= payload,
                        ids = None, 
                        batch_size = 256
                        )'''

def index_view(request):
    topics = Topic.objects.all()
    search_filter_topic = TopicFilter(request.GET, queryset= topics)
    search_term = request.GET.get('topic_title', '')

    topics = search_filter_topic.qs
    paginator = Paginator(topics, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'title' : "topics", 'topics': topics, 
               'search_filter_topic': search_filter_topic,
               'page_obj': page_obj,
               'search_term':search_term,
               }
    
    return render(request, "index.html", context)


def read_articles_of_topic(request, topic_id):
    # Retrieve the topic object based on the provided topic_id
    topic_articles = Article.objects.filter(topic_id=topic_id)
    
    paginator = Paginator(topic_articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'title':"articles",
               'articles': topic_articles, 
               # 'search_filter_article': search_filter_article,
               'page_obj': page_obj}

    # Render the articles related to the topic
    return render(request, 'articles_of_topic.html', context)

def recommend_view(request):
    if request.method == 'POST':
        form = RecommendrdForm(data= request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            # vectorized the search term
            # 'مدن ومحافظات وبلدان قارة آسيا'
            search_term_embed = model.encode([search_term])

            faiss.normalize_L2(search_term_embed)

            n_results = 1

            articles_results = articles_faiss_index.search(search_term_embed, n_results)
            topics_results = topics_faiss_index.search(search_term_embed, n_results)

            articles_r = [{
                'article_title':articles_title[articles_results[1][0][i]-1],
                'score': articles_results[0][0][i] 
                } for i in range(n_results)]
            topics_r = [{
                'topic_title':topics_title[topics_results[1][0][i]-1] ,
                'score': topics_results[0][0][i]
                } for i in range(n_results)]

            context = {
                'articles_results': articles_results, 'form':form, 'search_term':search_term,
                'topics_results':topics_results,'articles_r':articles_r, 'topics_r':topics_r
            }
            return render(request, 'recommended.html', context)
    else :
        form = RecommendrdForm()

    context = {"form":form}
    # Render the articles related to the topic
    return render(request, 'recommended.html', context)