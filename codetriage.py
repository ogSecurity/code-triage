from utils.config import CodeTriageConfiguration
from scm.github_public import GithubPublic

import pygit2
import os
import argparse
import csv
import logging

logging.basicConfig(level=logging.INFO)

CODE_TRIAGE_CONFIG = os.path.expanduser('~/.code-triage')
SCM_CLASS_MAP = {
    'github': GithubPublic
}


def triage(owner, scm, output_file='triage2.csv'):
    # If output file exists prompt for overwrite
    if os.path.exists(output_file):
        overwrite = input(f"File {output_file} already exists. Overwrite? (Y/N): ")
        if overwrite.casefold() not in {'y', 'yes'}:
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
    csv_writer.writerow(['Name', 'Owner', 'Pull (Y/N)', 'Pull Branch', 'Notes', 'Empty', 'Archived', 'Fork', 'Description', 'Forks', 'Open Issues', 'Last Updated', 'URL', 'Clone URL', 'Default Branch', 'Branch list', 'Release Tags', 'Latest Tag'])

    # Get all repositories for the user/org
    repos = scm.get_repos(owner)

    logging.info(f"Writing repo metadata to CSV file: {output_file}...")
    for repo in repos:
        branch_list = ','.join([branch.name for branch in repo.branches])
        csv_writer.writerow([repo.name, repo.owner, "", "", "", repo.is_empty, repo.is_archived, repo.is_fork, repo.description, repo.forks_count, repo.open_issues_count, repo.updated_at, repo.url, repo.clone_url, repo.default_branch, branch_list, repo.tag_count, repo.latest_tag])

    csv_file.close()

def pull(csv_file, scm, destination_folder):
    # Read CSV file
    with open(csv_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)

    # Download repos
    for i, row in enumerate(rows):
        if row['Pull (Y/N)'].casefold() in {'y', 'yes'}:
            logging.info(f"Pulling repo: {row['Name']}...")

            # Get branch to pull
            branch = row['Default Branch']
            if row['Pull Branch']:
                branch = row['Pull Branch']

            scm.pull_repo(row['Owner'], row['Name'], row['Clone URL'], branch, destination_folder)

# TODO functionality for checking the timestamp of each branches commit
# TODO functionality for checking each branch of a fork to see the timestamp of last commit and how many commits ahead and behind of target branch

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help='Mode: triage - create CSV containing repo information, pull - download all repos (use -t for triage sheet where you can specify what to pull)', choices=['triage', 'pull'], required=True)
    parser.add_argument('-u', '--user', help='User (or organisation), required for triage mode')
    parser.add_argument('-o', '--output', help='Output file', default='triage.csv')
    parser.add_argument('-t', '--triage-file', help='Triage file with repo information', default='triage.csv')
    parser.add_argument('-s', '--scm', help='Source control system - only Github is supported at this time', choices=['github'], default='github')
    parser.add_argument('-a', '--access-token', help='Access token - either as a file or the token itself')
    parser.add_argument('-p', '--prompt', help='Prompt for access tokens or credential material', action='store_true')
    parser.add_argument('-d', '--destination', help='Destination folder for pull', default='repos')
    args = parser.parse_args()

    if args.mode in ['triage', 'pull']:
        scm_class = SCM_CLASS_MAP[args.scm]
        scm = scm_class()
        scm.set_auth_configuration(args)
        scm.authenticate()

    if args.mode == "triage":
        if not args.user:
            logging.error("User (-u/--user) is required for triage mode")
            exit(1)

        triage(args.user, scm, args.output)

    elif args.mode == "pull":
        pull(args.triage_file, scm, args.destination)

