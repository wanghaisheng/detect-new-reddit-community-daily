import os
import requests
import csv
import time
from datetime import datetime
from requests_toolbelt import user_agent
from requests import Session

# Get config from environment variables (set in GitHub Action workflow)
user_agent_name = os.getenv('USER_AGENT_NAME', 'github-action-bot')
script_name = os.getenv('SCRIPT_NAME', 'subreddit-tracker')
script_vers = os.getenv('SCRIPT_VERSION', '0.0.1')
times_run = int(os.getenv('PAGES_TO_CRAWL', '3'))  # default 3 pages

my_script = f"{script_name}/{script_vers}"

s = Session()
s.headers = {
    'User-Agent': user_agent(user_agent_name, my_script)
}

header = ['display_name']
results = []

after_token = None

for i in range(times_run):
    url = 'https://www.reddit.com/subreddits/new.json?limit=100'
    if after_token:
        url += f'&after={after_token}'

    response = s.get(url)
    if response.status_code != 200:
        print(f"Request failed with status {response.status_code}. Retrying...")
        time.sleep(2)
        continue

    data = response.json()
    subs = data.get('data', {}).get('children', [])
    after_token = data.get('data', {}).get('after', None)

    if not subs:
        print("No more subreddits found.")
        break

    for sub in subs:
        entry = {field: sub['data'].get(field, '') for field in header}
        results.append(entry)

    print(f"Page {i+1} crawled, after_token: {after_token}")

    if not after_token:
        print("Reached the end of the list.")
        break

    time.sleep(1)  # polite delay

date_str = datetime.utcnow().strftime('%Y-%m-%d')
filename = f'results/new_subreddits_{date_str}.tsv'

# Ensure results folder exists
os.makedirs('results', exist_ok=True)

with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header, delimiter='\t')
    writer.writeheader()
    writer.writerows(results)

print(f"Saved {len(results)} subreddits to {filename}")
