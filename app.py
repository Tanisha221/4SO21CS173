from flask import Flask, jsonify
import requests
import threading

app = Flask(__name__)
window_size = 10
stored_numbers = []
lock = threading.Lock()

def fetch_numbers(number_type):
    url = f"http://localhost:9876/numbers/e"
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return []
    return []

def calculate_average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0.0

