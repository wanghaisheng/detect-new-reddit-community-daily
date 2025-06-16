import praw
import time
import os
from datetime import datetime, timedelta
import pytz

# --- Reddit API credentials ---
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='NewSubTracker/0.1 by YOUR_USERNAME'
)

# --- Set up timezone and time window ---
utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
one_day_ago = utc_now - timedelta(days=1)

# --- Track seen subreddits ---
seen_subreddits = set()
new_subreddits = []

# --- Create results directory if it doesn't exist ---
os.makedirs("results", exist_ok=True)

# --- Filename as today's date ---
filename = f"results/{utc_now.strftime('%Y-%m-%d')}.txt"

# --- Scan new posts from r/all ---
print("Scanning for new subreddits...\n")

for submission in reddit.subreddit("all").new(limit=1000):
    subreddit = submission.subreddit

    if subreddit.display_name in seen_subreddits:
        continue

    seen_subreddits.add(subreddit.display_name)

    created_time = datetime.utcfromtimestamp(subreddit.created_utc).replace(tzinfo=pytz.UTC)

    if created_time > one_day_ago:
        line = f"r/{subreddit.display_name} | Created: {created_time.strftime('%Y-%m-%d %H:%M:%S')} UTC"
        print(line)
        new_subreddits.append(line)

# --- Save to file ---
if new_subreddits:
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(new_subreddits))
    print(f"\nSaved {len(new_subreddits)} new subreddits to {filename}")
else:
    print("No new subreddits found in the last 24 hours.")
