import json
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

def build_vector_db():
    print("Loading Knowledge Base...")
    kb_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base.json')
    with open(kb_path, 'r') as f:
        kb_data = json.load(f)
        
    texts = [item['content'] for item in kb_data]
    
    print("Loading Sentence Transformer model...")
    # using a small, fast model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Generating embeddings...")
    embeddings = model.encode(texts)
    
    # Save embeddings and data
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    embeddings_path = os.path.join(models_dir, 'kb_embeddings.npy')
    data_path = os.path.join(models_dir, 'kb_data.pkl')
    
    np.save(embeddings_path, embeddings)
    with open(data_path, 'wb') as f:
        pickle.dump(kb_data, f)
        
    print(f"Embeddings saved to {embeddings_path}")
    print(f"KB Data saved to {data_path}")

if __name__ == "__main__":
    build_vector_db()
