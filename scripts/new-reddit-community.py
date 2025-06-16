import praw
import os
from datetime import datetime
import json
import pytz

print("Scanning for new subreddits...")

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent=os.environ.get("REDDIT_USER_AGENT")
)

utc_now = datetime.utcnow().strftime('%Y-%m-%d')
result_dir = "results"
os.makedirs(result_dir, exist_ok=True)

found = {}

for submission in reddit.subreddit("all").new(limit=1000):
    sub_name = submission.subreddit.display_name
    created = submission.created_utc
    if sub_name not in found:
        found[sub_name] = created

result_path = f"{result_dir}/{utc_now}.json"
with open(result_path, "w") as f:
    json.dump(found, f, indent=2)

print(f"Saved {len(found)} unique subreddits to {result_path}")
import praw
import os
from datetime import datetime
import json
import pytz

print("Scanning for new subreddits...")

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent=os.environ.get("REDDIT_USER_AGENT")
)

utc_now = datetime.utcnow().strftime('%Y-%m-%d')
result_dir = "results"
os.makedirs(result_dir, exist_ok=True)

found = {}

for submission in reddit.subreddit("all").new(limit=1000):
    sub_name = submission.subreddit.display_name
    created = submission.created_utc
    if sub_name not in found:
        found[sub_name] = created

result_path = f"{result_dir}/{utc_now}.json"
with open(result_path, "w") as f:
    json.dump(found, f, indent=2)

print(f"Saved {len(found)} unique subreddits to {result_path}")
