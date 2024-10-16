from scm.github import Github

import os
import argparse
import csv
import logging
from utils.output import Output, RowConfiguration, Row, TriageFile

logging.basicConfig(level=logging.INFO)

CODE_TRIAGE_CONFIG = os.path.expanduser('~/.code-triage')
SCM_CLASS_MAP = {
    'github': Github
}


def triage(owner, scm, output_file='triage2.csv'):
    """
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
    """

    row_config = RowConfiguration()
    output = Output(row_config, output_file)

    """
    csv_writer = csv.writer(csv_file, dialect='excel')
    csv_writer.writerow([
        ROW_NAME_LABEL,
        ROW_OWNER_LABEL,
        ROW_PULL_LABEL,
        ROW_PULL_BRANCH_TAG_LABEL,
        ROW_NOTES_LABEL,
        ROW_EMPTY_LABEL,
        ROW_ARCHIVED_LABEL,
        ROW_FORK_LABEL,
        ROW_DESCRIPTION_LABEL,
        ROW_FORKS_LABEL,
        ROW_OPEN_ISSUES_LABEL,
        ROW_LAST_UPDATED_LABEL,
        ROW_URL_LABEL,
        ROW_CLONE_URL_LABEL,
        ROW_DEFAULT_BRANCH_LABEL,
        ROW_BRANCH_LIST_LABEL,
        ROW_RELEASE_TAGS_LABEL,
        ROW_LATEST_TAG_LABEL
    ])
    """

    # Get all repositories for the user/org
    repos = scm.get_repos(owner)

    logging.info(f"Writing repo metadata to CSV file: {output_file}...")
    """
    for repo in repos:
        branch_list = ','.join([branch.name for branch in repo.branches])
        csv_writer.writerow([repo.name, repo.owner, "", "", "", repo.is_empty, repo.is_archived, repo.is_fork, repo.description, repo.forks_count, repo.open_issues_count, repo.updated_at, repo.url, repo.clone_url, repo.default_branch, branch_list, repo.tag_count, repo.latest_tag])
    """

    for repo in repos:
        row = Row(row_config)
        row.name = repo.name
        row.owner = repo.owner
        row.pull = ""
        row.pull_branch_tag = ""
        row.notes = ""
        row.empty = repo.is_empty
        row.archived = repo.is_archived
        row.fork = repo.is_fork
        row.description = repo.description
        row.forks = repo.forks_count
        row.open_issues = repo.open_issues_count
        row.last_updated = repo.updated_at
        row.url = repo.url
        row.clone_url = repo.clone_url
        row.default_branch = repo.default_branch
        row.branch_list = ','.join([branch.name for branch in repo.branches])
        row.tags = repo.tag_count
        row.latest_tag = repo.latest_tag
        output.add_row(row)

    output.write()

def pull(triage_file, scm, destination_folder):
    row_config = RowConfiguration()
    triage_file = TriageFile(triage_file, row_config)

    # Download repos
    for row in triage_file.get_data():
        if row.pull.casefold() in {'y', 'yes'}:
            logging.info(f"Pulling repo: {row.name}...")

            # Get branch to pull
            branch = row.default_branch
            if row.pull_branch_tag:
                branch = row.pull_branch_tag

            scm.pull_repo(row.owner, row.name, row.clone_url, branch, destination_folder)

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

    # Setup target SCM system
    scm_class = SCM_CLASS_MAP[args.scm]
    scm = scm_class()

    if args.mode in ['triage', 'pull']:
        scm.set_auth_configuration(args)
        scm.authenticate()

    if args.mode == "triage":
        if not args.user:
            logging.error("User (-u/--user) is required for triage mode")
            exit(1)

        triage(args.user, scm, args.output)

    elif args.mode == "pull":
        pull(args.triage_file, scm, args.destination)

