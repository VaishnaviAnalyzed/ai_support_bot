import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

def train_intent_model():
    print("Loading data...")
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'intents.csv')
    df = pd.read_csv(data_path)
    
    # Simple preprocessing
    df['text'] = df['text'].str.lower()
    
    X = df['text']
    y = df['intent']
    
    print("Training model...")
    # Create a pipeline that converts text to features and then trains a classifier
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', LogisticRegression(random_state=42, max_iter=1000)),
    ])
    
    text_clf.fit(X, y)
    
    # Save the model
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'intent_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(text_clf, f)
        
    print(f"Model saved to {model_path}")
    print("Training accuracy:", text_clf.score(X, y))

if __name__ == "__main__":
    train_intent_model()
