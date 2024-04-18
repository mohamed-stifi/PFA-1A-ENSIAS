import pandas as pd
import pickle
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
