from github import Github, Auth
from github.GithubException import GithubException


import pygit2
import os
import argparse
import csv
import logging

logging.basicConfig(level=logging.INFO)

def triage(owner, output_file='triage.csv', access_token='access_token'):
    auth = Auth.Token(access_token)
    g = Github(auth=auth)

    # Get all repositories for the owner
    repos = g.get_user(owner).get_repos()

    # If output file exists prompt for overwrite
    if os.path.exists(output_file):
        overwrite = input(f"File {output_file} already exists. Overwrite? (Y/N): ")
        if overwrite not in ['Y', 'y', 'Yes', 'yes']:
            logging.info("Exiting...")
            return

    # Build CSV file with repo metadata
    try:
        csv_file = open(output_file, mode='w', newline='')
    except PermissionError:
        logging.error(f"Permission denied to write to file: {output_file} - is it open?")
        return

    csv_writer = csv.writer(csv_file, dialect='excel')

    # TODO Move Pull (Y/N) and Pull Branch after "Name"
    # TODO Add Note after main
    csv_writer.writerow(['Name', 'Owner', 'Empty', 'Archived', 'Fork', 'Description', 'Forks', 'Open Issues', 'Last Updated', 'URL', 'Default Branch', 'Branch list', 'Release Tags', 'Latest Tag', 'Pull (Y/N)', 'Pull Branch'])

    count = 1
    for repo in repos:
        logging.info(f"Processing repo: {repo.name}... {count}/{repos.totalCount}")

        # Get all branches for the repo
        logging.info(f"Getting branches for repo: {repo.name}...")
        branches = repo.get_branches()
        branch_list = ','.join([branch.name for branch in branches])

        # Get any tag information
        tag_count, latest_tag = release_tags(repo)

        # Write repo metadata to CSV file
        logging.info(f"Writing repo metadata to CSV file: {output_file}...")
        csv_writer.writerow([repo.name, repo.owner.login, is_repo_empty(repo), repo.archived, repo.fork, repo.description, repo.forks_count, repo.open_issues_count, repo.updated_at, repo.html_url, repo.default_branch, branch_list, tag_count, latest_tag, "", ""])

        count += 1
    csv_file.close()

def release_tags(repo):
    count = 0
    latest_tag = "N/A"
    try:
        tags = repo.get_tags()
        count = tags.totalCount
        if count > 0:
            latest_tag = tags[0].name
    except GithubException as e:
        logging.error(f"An error getting tags for {repo.name}: {e}")
        return count, latest_tag
    return count, latest_tag

def is_repo_empty(repo):
    try:
        # Check if the repository size is zero
        if repo.size == 0:
            return True
        # Check if the repository has any branches
        branches = repo.get_branches()
        if branches.totalCount == 0:
            return True
        # If the repository has branches, check if it has any commits
        if repo.get_commits().totalCount == 0:
            return True
        return False
    except GithubException as e:
        print(f"An error occurred: {e}")
        return False


def pull(csv_file, access_token, destination_folder):
    auth = Auth.Token(access_token)
    g = Github(auth=auth)

    # Read CSV file
    with open(csv_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)

    # Download repos
    for i, row in enumerate(rows):
        if row['Pull (Y/N)'] in ['Y', 'y', 'Yes', 'yes']:
            logging.info(f"Pulling repo: {row['Name']}...")

            # Get repo
            repo = g.get_repo(f"{row['Owner']}/{row['Name']}")

            # Get branch to pull
            branch = row['Default Branch']
            if row['Pull Branch']:
                branch = row['Pull Branch']

            # TODO if * in branch list, pull all branches

            # TODO if pull branch doesn't exist but was given check tag name and tag id and pull that if it exists

            # Clone repo
            try:
                pygit2.clone_repository(repo.clone_url, f"{destination_folder}/{row['Name']}", checkout_branch=branch)
            except ValueError as e:
                logging.error(f"An error occurred cloning {row['Name']}: {e}, skipping")
                continue

            logging.info(f"Repo {row['Name']} pulled to {destination_folder}")

# TODO functionality for checking the timestamp of each branches commit
# TODO functionality for checking each branch of a fork to see the timestamp of last commit and how many commits ahead and behind of target branch

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help='Mode: triage - create CSV containing repo information, pull - download all repos (use -t for triage sheet where you can specify what to pull)', choices=['triage', 'pull'], required=True)
    parser.add_argument('-u', '--user', help='User (or organisation), required for triage mode')
    parser.add_argument('-o', '--output', help='Output file', default='triage.csv')
    parser.add_argument('-t', '--triage-file', help='Triage file with repo information', default='triage.csv')
    parser.add_argument('-a', '--access-token', help='Access token', required=True)
    parser.add_argument('-d', '--destination', help='Destination folder for pull', default='repos')
    args = parser.parse_args()

    if args.mode == "triage":
        if not args.user:
            logging.error("User (-u/--user) is required for triage mode")
        else:
            triage(args.user, args.output, args.access_token)

    elif args.mode == "pull":
        pull(args.triage_file, args.access_token, args.destination)

