import os
import subprocess
import sys

import requests

# Get the necessary information from the GitHub Actions environment


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

# Check if the request was successful (status code 200)
if response.status_code == 200:
    pull_request_info = response.json()
    source_branch = pull_request_info["head"]["ref"]
    # Configure Git user details
    subprocess.run(
        ["git", "config", "--global", "user.email", "actions@github.com"]
    )
    subprocess.run(
        ["git", "config", "--global", "user.name", "GitHub Actions"]
    )
    subprocess.run(
        [
            "git",
            "config",
            "--global",
            "--add",
            "safe.directory",
            "/home/runner/work/test_actions/test_actions",
        ]
    )

    # Construct the URL to fetch pull request commits using the GitHub API

    commits_url = f"https://api.github.com/repos/{repository}/pulls/{pull_request_number}/commits"
    # Send a GET request to retrieve the list of commits for the pull request

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
            # If the commit message contains 'BREAKING CHANGE', increment the major version
            if "BREAKING CHANGE" in message:
                version_parts = version.split(".")
                version_parts[0] = str(int(version_parts[0]) + 1)
                version_parts[1] = "0"
                version_parts[2] = "0"
                version = ".".join(version_parts)
            # If the commit message contains 'feat', increment the minor version
            elif "feat" in message:
                version_parts = version.split(".")
                version_parts[1] = str(int(version_parts[1]) + 1)
                version_parts[2] = "0"
                version = ".".join(version_parts)
            # If the commit message contains 'fix', increment the patch version
            elif "fix" in message:
                version_parts = version.split(".")
                version_parts[2] = str(int(version_parts[2]) + 1)
                version = ".".join(version_parts)

        # Write the changelog to a file
        with open("CHANGELOG.md", "w") as changelog_file:
            changelog_file.write("# Changelog\n\n")
            for item in changelog:
                changelog_file.write(f"- {item}\n")

        # Commit and push the changelog file to the source branch
        subprocess.run(["git", "checkout", source_branch])
        subprocess.run(["git", "add", "CHANGELOG.md"])
        subprocess.run(["git", "commit", "-m", "'Update changelog'"])
        subprocess.run(["git", "push", "origin", source_branch])
    else:
        print(f"Failed to retrieve commits: {response.status_code}")
        sys.exit(1)
else:
    print(
        f"Failed to retrieve pull request information: {response.status_code}"
    )
    sys.exit(1)
