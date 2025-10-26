#!/usr/bin/env python3
"""
Quick test script to check if the backend is working
"""
import requests
import json

def test_backend():
    try:
        # Test basic endpoint
        response = requests.get("http://localhost:8000/")
        print(f"✅ Basic endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test gamification endpoints
        try:
            response = requests.get("http://localhost:8000/gamification/user-stats/testuser")
            print(f"✅ Gamification endpoint: {response.status_code}")
        except Exception as e:
            print(f"❌ Gamification endpoint error: {e}")
            
        # Test chat endpoints
        try:
            response = requests.get("http://localhost:8000/chat/history/testroom")
            print(f"✅ Chat endpoint: {response.status_code}")
        except Exception as e:
            print(f"❌ Chat endpoint error: {e}")
            
    except Exception as e:
        print(f"❌ Backend not running: {e}")
        print("Make sure to run: python -m uvicorn app.main:app --reload")

if __name__ == "__main__":
    test_backend()
