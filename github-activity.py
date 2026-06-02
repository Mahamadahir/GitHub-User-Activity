#!/usr/bin/env python3

"""
GitHub User Activity CLI.

Fetches recent public activity for a GitHub user and displays it in the terminal.
"""

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://api.github.com/users/{username}/events"
REQUEST_TIMEOUT = 10


def parse_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Github Activity CLI - Fetches and display recent activty for a user"
        )
    parser.add_argument(
        'username',
        help='Github username to fetch activity for'
    )
    return parser.parse_args()

def fetch_activity(username):
    """Fetch recent public GitHub activity for username."""
    
    url = API_URL.format(username = username)

    request = Request(
        url,
        headers={
            "User-Agent": "github-activity-cli"
        }
    )

    with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        response_body = response.read().decode("utf-8")

    return json.loads(response_body)

def summarise_events(events):
    # dict with tuple as key 
    summary = {}

    for event in events:
        event_type = event.get("type")
        repo_name = event.get("repo", {}).get("name", "unknown repositry")
        detail = get_event_detail(event)

        key = (event_type, repo_name, detail)
        summary[key] = summary.get(key, 0) + 1 

    return summary


def get_event_detail(event):
    event_type = event.get("type")
    payload = event.get("payload", {})

    if event_type == "CreateEvent":
        return payload.get("ref_type")
    
    if event_type in ("IssuesEvent", "PullRequestEvent"):
        return payload.get("action")
    
    return None

#TODO
def format_summary_item(event_type, repo_name, detail, count):

    if event_type == "PushEvent":
        return f"- Pushed {count} {"commits" if count > 1 else "commit"} to {repo_name}."

    if event_type == "IssuesEvent":
        return f"- {count} {"issues" if count > 1 else "issue"} {detail} in {repo_name}."

    if event_type == "CreateEvent":
        return f"- {count} {"branches were" if count > 1 else "branch was"} created in {repo_name}."
    
    if event_type == "PullRequestEvent":
        return f"- {f"{count} pull requests were" if count > 1 else "A pull request was"} {detail} in {repo_name}."
    
    if event_type == "WatchEvent": 
        return f"- Starred {repo_name}."
    
    if event_type == "ForkEvent":
        return f"- Forked {repo_name}."
    
    return f"- {event_type} occurred {f'{count} times' if count > 1 else 'once'} in {repo_name}."

#TODO
def display_activity(summary):

    print("Output:")
    
    if not summary:
        print("No recent public activity found")

    else :
        
        for key, value in summary.items():
            print(format_summary_item(key[0], key[1], key[2], value))        
    

#TODO
def handle_http_error(error):
    """Convert GitHub HTTP errors into friendly CLI messages."""

    if error.code == 404:
        return "User not found. Check the username and try again."
    if error.code == 403:
        return "GitHub API rate limit reached. Try again later."
    return f"GitHub API returned an error ({error.code})."

#TODO
def main():
    """Run the CLI."""

    args = parse_args()

    try:
        events = fetch_activity(args.username)
    
    except HTTPError as error:
        sys.exit(handle_http_error(error))
    except URLError as error:
        sys.exit(f"Could not reach GitHub: {error.reason}")
    except json.JSONDecodeError:
        sys.exit("GitHub returned an unexpected response.")

    summary = summarise_events(events)
    display_activity(summary)

if __name__ == "__main__":
    main()