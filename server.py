from flask import Flask, jsonify, request
import requests
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

API_URL = 'https://bored-api.appbrewery.com/random'
RETRY_LIMIT = 5
DELAY = 5

def fetch_data(n):
    data = []
    for i in range(n):
        success = False
        for attempt in range(RETRY_LIMIT):
            response = requests.get(API_URL)
            if response.status_code == 200:
                activity = response.json()
                activity['link'] = 'https://www.redcross.org/give-blood'
                data.append(activity)
                success = True
                break
            elif response.status_code == 429:
                print(f"Rate limit exceeded at iteration {i}, attempt {attempt + 1}. Retrying in {DELAY} seconds...")
                time.sleep(DELAY)
            else:
                print(f"Error fetching data at iteration {i}: {response.status_code}")
                return None, response.status_code
        if not success:
            print(f"Failed to fetch data after {RETRY_LIMIT} attempts")
            return None, 429
    return data, 200

@app.route('/get-activities', methods=['GET'])
def get_activities():
    n = int(request.args.get('n', 10))  # Default to 10 if 'n' is not provided
    data, status_code = fetch_data(n)
    if status_code == 200:
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data"}), status_code

if __name__ == '__main__':
    app.run(debug=True)
