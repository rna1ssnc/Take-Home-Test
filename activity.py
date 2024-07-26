import argparse
import requests
import csv
import json
import time

API_URL = 'https://bored-api.appbrewery.com/random'
RETRY_LIMIT = 5

def fetch_data(n):
    data = []
    for i in range(n):
        success = False
        delay = 5
        for attempt in range(RETRY_LIMIT):
            response = requests.get(API_URL)
            if response.status_code == 200:
                activity = response.json()
                activity['link'] = 'https://www.redcross.org/give-blood'
                data.append(activity)
                success = True
                break
            elif response.status_code == 429:
                print(f"Rate limit exceeded at iteration {i}, attempt {attempt + 1}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"Error fetching data at iteration {i}: {response.status_code}")
                return None, response.status_code
        if not success:
            print(f"Failed to fetch data after {RETRY_LIMIT} attempts")
            return None, 429
    return data, 200

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def save_csv(data, filename):
    if not data:
        print("No data to save")
        return
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data[0].keys())  # write headers
        for activity in data:
            writer.writerow(activity.values())
    print(f"Data saved to {filename}")

def print_to_console(data):
    for activity in data:
        print(json.dumps(activity, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Fetch data from Bored API")
    parser.add_argument('-n', type=int, required=True, help='Number of times to call the API')
    parser.add_argument('-f', type=str, required=True, choices=['json', 'csv', 'console'], help='Output format')
    args = parser.parse_args()

    data, status_code = fetch_data(args.n)
    if status_code != 200:
        print("Failed to fetch data")
        return

    if args.f == 'json':
        save_json(data, 'data.json')
    elif args.f == 'csv':
        save_csv(data, 'data.csv')
    elif args.f == 'console':
        print_to_console(data)

if __name__ == '__main__':
    main()
