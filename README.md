# GitHub User Activity CLI

A command-line tool that fetches a GitHub user's recent public activity
and displays it in the terminal, using only the Python standard library.

Project page: https://roadmap.sh/projects/github-user-activity

## Requirements

Python 3.12+ (uses nested quotes inside f-strings). No external dependencies.

## Usage

    python3 github-activity.py <username>

Example:

    python3 github-activity.py torvalds

## Sample output

    Output:
    - Pushed 6 commits to torvalds/linux.
    - 1 branch was created in torvalds/ScrollWheel.
    - 2 pull requests were closed in torvalds/GuitarPedal.

## Error handling

- Invalid username -> "User not found."
- Rate limit (HTTP 403) -> "GitHub API rate limit reached."
- Network failure -> "Could not reach GitHub."

## Notes

Activity is fetched from `https://api.github.com/users/<username>/events`
using `urllib` from the standard library, with no third-party HTTP libraries.
