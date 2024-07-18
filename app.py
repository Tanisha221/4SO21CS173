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
@app.route('/numbers/<string:number_type>', methods=['GET'])
def get_numbers(number_type):
    if number_type not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number type"}), 400

    with lock:
        previous_state = stored_numbers.copy()

    fetched_numbers = fetch_numbers(number_type)
    unique_numbers = list(set(fetched_numbers))

    with lock:
        for number in unique_numbers:
            if number not in stored_numbers:
                if len(stored_numbers) >= window_size:
                    stored_numbers.pop(0)
                stored_numbers.append(number)

        current_state = stored_numbers.copy()
        avg = calculate_average(stored_numbers)

    return jsonify({
        "windowPrevState": previous_state,
        "windowCurrState": current_state,
        "numbers": unique_numbers,
        "avg": round(avg, 2)
    })

if __name__ == '__main__':
    app.run(port=9876)


