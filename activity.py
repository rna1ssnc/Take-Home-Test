import argparse
import requests
import csv
import json
import time

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

def save_as_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved as {filename}")

def save_as_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Data saved as {filename}")

def print_to_console(data):
    for item in data:
        print(json.dumps(item, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Fetch activities from Bored API.")
    parser.add_argument('-n', type=int, required=True, help='Number of times to fetch data')
    parser.add_argument('-f', type=str, required=True, choices=['json', 'csv', 'console'], help='Output format')
    args = parser.parse_args()

    data, status_code = fetch_data(args.n)
    if status_code != 200:
        print(f"Failed to fetch data: Status code {status_code}")
        return

    if args.f == 'json':
        save_as_json(data, 'activities.json')
    elif args.f == 'csv':
        save_as_csv(data, 'activities.csv')
    elif args.f == 'console':
        print_to_console(data)

if __name__ == '__main__':
    main()
