import os
import sys

import requests

if __name__ == "__main__":
    repository = os.environ["GITHUB_REPOSITORY"]
    pull_request_number = os.environ["PR_NUMBER"].split("/")[-1]
    # Construct the URL to fetch pull request information using the GitHub API
    url = f"https://api.github.com/repos/{repository}/pulls/{pull_request_number}"

    # Add any necessary authentication headers if your repository requires them

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f'Bearer {os.environ["GITHUB_TOKEN"]}',
    }

    # Send a GET request to retrieve information about the pull request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pull_request_info = response.json()
        commits_url = f"https://api.github.com/repos/{repository}/pulls/{pull_request_number}/commits"  # Send a GET request to retrieve the list of commits for the pull request

        response = requests.get(commits_url, headers=headers)

        if response.status_code == 200:
            commits = response.json()
            changelog = []
            version = "1.0.0"  # Initial version
            # Process the list of commits
            for commit in commits:
                sha = commit["sha"]

                message = commit["commit"]["message"]
                changelog.append(f"{sha[:7]}: {message}")

            # Write the changelog to a file
            with open("CHANGELOG.md", "w") as changelog_file:
                changelog_file.write("# Changelog\n\n")
                for item in changelog:
                    changelog_file.write(f"- {item}\n")

    else:
        sys.exit(1)
