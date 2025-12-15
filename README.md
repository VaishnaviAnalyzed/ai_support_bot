# 🤖 AI-Powered Customer Support Chatbot (RAG Architecture)

This is a full-stack, end-to-end Machine Learning project delivering a smart customer support chatbot website. It is built on a **Retrieval-Augmented Generation (RAG)** architecture to provide **high-accuracy, context-grounded answers**, effectively eliminating the "hallucinations" common in simple generative models.

## 🌟 Features & Functionality

* **RAG Core:** The chatbot dynamically retrieves the most relevant information from a structured Knowledge Base (KB) before generating a response. This ensures fidelity to company policies and FAQs.
* **Intent Classification:** Uses a trained model to classify simple intents (e.g., Greetings, Thank You, Reset Password) for instant, non-RAG responses, improving speed.
* **Full-Stack Solution:** Includes a responsive web interface (Frontend) and a robust model-serving API (Backend).
* **MLOps Ready:** Includes an **Admin Dashboard** for live logging of conversations, intent predictions, and model confidence scores for continuous improvement.

## 🚀 Technical Stack

| Category | Component | Key Libraries/Tools |
| :--- | :--- | :--- |
| **Machine Learning** | RAG Pipeline, Vectorization | **Sentence-BERT** (`sentence-transformers`), NumPy / **FAISS** (Vector Store) |
| **Model Serving** | Backend API | **FastAPI** (Recommended for speed) or Flask |
| **Data & Classification** | Intent Routing | **Scikit-learn** or DistilBERT (Hugging Face) |
| **Deployment** | Containerization, Hosting | **Docker**, Heroku / AWS EC2 |
| **Frontend** | User Interface | HTML, CSS, JavaScript (Fetch API) |

## 🗺️ Project Architecture (RAG Flow)

The system is designed with a multi-stage inference process:

1.  **User Query** enters the system.
2.  **Intent Classifier** routes the query.
3.  **Complex Query Path:** Query is converted to a vector embedding.
4.  **Retrieval:** Vector is compared against the pre-indexed **Knowledge Base Vectors**. Top K relevant chunks are retrieved.
5.  **Response:** The retrieved text is returned as the final, grounded answer.

## ⚙️ Setup and Installation

### Prerequisites

* Python 3.8+
* Docker (for containerization and local deployment)
