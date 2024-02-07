import os
import sys

import requests

# Get the necessary information from the GitHub Actions environment
repository = os.environ["GITHUB_REPOSITORY"]
pull_request_number = os.environ["PR_NUMBER"].split("/")[-1]

print("HELLO WORLD")

# Construct the URL to fetch pull request information using the GitHub API
url = f"https://api.github.com/repos/{repository}/pulls/{pull_request_number}/commits"


# Add any necessary authentication headers if your repository requires them
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f'Bearer {os.environ["GITHUB_TOKEN"]}',
}

print(url)
print(headers)

# Send a GET request to retrieve the list of commits for the pull request
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    commits = response.json()
    # Process the list of commits
    for commit in commits:
        print(commit["sha"], commit["commit"]["message"])
else:
    print(f"Failed to retrieve commits: {response.status_code}")
    sys.exit(1)
