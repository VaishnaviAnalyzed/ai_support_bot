import requests
import time
import sys

def test_api():
    url = "http://127.0.0.1:8000/api/chat"
    
    # Wait for server to start
    print("Waiting for server...")
    time.sleep(5)
    
    test_cases = [
        {"message": "Hello"},
        {"message": "How do I return an item?"},
        {"message": "Does the laptop have 5G?"}
    ]
    
    for tc in test_cases:
        try:
            print(f"\nSending: {tc['message']}")
            response = requests.post(url, json=tc)
            if response.status_code == 200:
                print("Response:", response.json())
            else:
                print("Error:", response.status_code, response.text)
        except Exception as e:
            print("Request failed:", e)

if __name__ == "__main__":
    test_api()
