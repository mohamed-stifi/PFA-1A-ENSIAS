'''
   Qdrant is an open-source vector search engine that is specifically designed for 
efficient similarity search over large collections of high-dimensional vectors. 
It is commonly used for tasks such as nearest neighbor search, similarity search, 
and clustering in applications like recommendation systems, natural language 
processing, image processing, and more.

   Qdrant provides a Python client library that simplifies interacting with Qdrant's 
RESTful API. Using the Qdrant Python client, you can easily perform operations such 
as ingesting data, querying vectors, and managing the vector database.
'''
import pandas as pd
import pickle
from qdrant_client import QdrantClient
from qdrant_client.models import models
from sentence_transformers import SentenceTransformer

# Load data and prepare data
def load_data(data):
    return pd.read_csv(data)

def prepare_data(df, name):
    docx = df[f'{name}_title'].tolist()
    payload = df[[f"{name}_id"]].to_dict("records")
    return docx, payload

def save_vectors(vectors, name):
    with open(f'vectorized_{name}.pickle', 'wb') as f:
        pickle.dump(vectors, f)

def load_vectors(vector_file):
    with open(vector_file, 'rb') as f:
        vectors = pickle.load(f)
    return vectors

name = 'article'

# create a vectorDB client
client = QdrantClient(path=f'{name}_vector_database.db')
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
vectors = model.encode(docx, show_progress_bar= True)
print('model is encode')
save_vectors(vectors, name)

print("is saved")
# stored in vectorDB collection
client.upload_collection(collection_name=f'{name}s_collection',
                        vectors= vectors,
                        ids = None,
                        payload= payload, 
                        batch_size = 1024
                        )

print('upload_collection')
query_vector = model.encode('مدن ومحافظات وبلدان قارة آسيا').tolist()

results = client.search(collection_name=f'{name}s_collection',
                        query_vector= query_vector,
                        limit=5)

print('search')

print(results)