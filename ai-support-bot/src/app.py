from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import sqlite3
import datetime
import os
import secrets
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.inference import ChatbotInference

# Initialize global bot variable
bot = None
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def init_db():
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    db_path = os.path.join(logs_dir, 'chat_logs.db')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_message TEXT,
            intent TEXT,
            bot_response TEXT,
            confidence REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_interaction(user_message, intent, bot_response, confidence):
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    db_path = os.path.join(logs_dir, 'chat_logs.db')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute('INSERT INTO logs (timestamp, user_message, intent, bot_response, confidence) VALUES (?, ?, ?, ?, ?)',
              (timestamp, user_message, intent, bot_response, confidence))
    conn.commit()
    conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global bot
    # Startup: Load the model
    print("Loading models...")
    bot = ChatbotInference()
    print("Models loaded.")
    
    # Initialize DB
    init_db()
    
    yield
    
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, 'index.html'))

@app.get("/admin")
async def read_admin(username: str = Depends(get_current_username)):
    return FileResponse(os.path.join(static_dir, 'admin.html'))

@app.get("/api/admin/stats")
async def get_stats(username: str = Depends(get_current_username)):
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    db_path = os.path.join(logs_dir, 'chat_logs.db')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Total chats
    c.execute("SELECT COUNT(*) FROM logs")
    total_chats = c.fetchone()[0]
    
    # Avg confidence
    c.execute("SELECT AVG(confidence) FROM logs")
    avg_conf_result = c.fetchone()[0]
    avg_conf = avg_conf_result if avg_conf_result is not None else 0.0
    
    # Intent distribution
    c.execute("SELECT intent, COUNT(*) FROM logs GROUP BY intent")
    intents = c.fetchall()
    
    conn.close()
    
    return {
        "total_chats": total_chats,
        "avg_confidence": avg_conf,
        "intents": {i[0]: i[1] for i in intents}
    }

@app.get("/api/admin/logs")
async def get_logs(username: str = Depends(get_current_username)):
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    db_path = os.path.join(logs_dir, 'chat_logs.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

class UserQuery(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(query: UserQuery):
    user_message = query.message
    
    intent = bot.predict_intent(user_message)
    info, score = bot.retrieve_info(user_message)
    
    response_text = ""
    confidence = 0.0
    
    if intent == "Greetings":
        response_text = "Hello! How can I assist you today?"
        confidence = 1.0
    elif intent == "Acknowledgement":
        response_text = "Thank you."
        confidence = 1.0
    elif intent == "Reset Password":
         if info:
             response_text = f"[{intent}] {info['content']}"
             confidence = float(score)
         else:
             response_text = "To reset your password, please check our help section or contact support."
             confidence = 0.5
    else:
        if info:
            response_text = f"[{intent}] {info['content']}"
            confidence = float(score)
        else:
            response_text = "I'm sorry, I couldn't find specific information about that."
            confidence = 0.0

    log_interaction(user_message, intent, response_text, confidence)
    
    return {
        "response": response_text,
        "intent": intent,
        "confidence": confidence
    }
