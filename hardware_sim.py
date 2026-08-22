import requests
import time
import random
import os

API_URL =os.getenv("RENDER_API_URL")

print("Starting fake ESP32 Hardware Stream...")
battery = 100

while True:
    payload = {
        "device_id": "HELMET_ESP32_01",
        "ir_status": random.choice([True, False, False]), 
        "battery_percent": battery
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers={"X-Hardware-Key": "dev-secret-key-123"})
        print(f"Sent: {payload} | Status: {response.status_code}")
    except Exception as e:
        print("API is offline.")
        
    battery = max(0, battery - 1)
    time.sleep(2) 
