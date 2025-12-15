import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class ChatbotInference:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.models_dir = os.path.join(self.base_dir, '..', 'models')
        
        # Load Intent Model
        with open(os.path.join(self.models_dir, 'intent_model.pkl'), 'rb') as f:
            self.intent_model = pickle.load(f)
            
        # Load Vector DB
        self.kb_embeddings = np.load(os.path.join(self.models_dir, 'kb_embeddings.npy'))
        with open(os.path.join(self.models_dir, 'kb_data.pkl'), 'rb') as f:
            self.kb_data = pickle.load(f)
            
        # Load Sentence Transformer (must match the one used for building DB)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def predict_intent(self, text):
        return self.intent_model.predict([text.lower()])[0]
    
    def retrieve_info(self, query):
        query_vec = self.embedding_model.encode([query])
        similarities = cosine_similarity(query_vec, self.kb_embeddings)[0]
        
        # Get top 1 result for now
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score < 0.2: # arbitrary threshold
            return None, best_score
            
        return self.kb_data[best_idx], best_score

    def get_response(self, user_query):
        intent = self.predict_intent(user_query)
        print(f"Detected Intent: {intent}")
        
        if intent == "Greetings":
            return "Hello! How can I assist you today?"
        
        if intent == "Reset Password":
             # We can still look up specific details if needed, or provide a generic response if the retrieval is low confidence
             # For a RAG system, we usually try to valid retrieval even for known intents to be specific.
             pass
             
        # Retrieval Step
        info, score = self.retrieve_info(user_query)
        
        if info:
            return f"[{intent}] Here is what I found: {info['content']} (Confidence: {score:.2f})"
        else:
            return "I'm sorry, I couldn't find specific information about that in my knowledge base."

if __name__ == "__main__":
    bot = ChatbotInference()
    
    test_queries = [
        "Hello",
        "How do I get a refund?",
        "How long does shipping take?",
        "What is the battery life?",
        "I forgot my password"
    ]
    
    for q in test_queries:
        print(f"\nQuery: {q}")
        print(f"Response: {bot.get_response(q)}")
