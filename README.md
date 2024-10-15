# CodeTriage

Code Triage is a tool that can be used by security consultants and their clients for a number of use cases:

- Generating a spreadsheet containing a list of repositories can easily be walked through manually to
    - Mark if the repository should be in scope for review
    - Select what branches or tagged releases should be in scope
- Using the marked up sheet, the repositories can be pulled for offline analysis

# Access Tokens and Authentication

## GitHub

You can generate an access token if you have a GitHub account by following the guide [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

If you're using `Tokens (classic)` the only permission you'll need is `public_repo` under `repo`. If you want to be able to access provide repos you should tick `repo` to select the entire tree.

# Running with Docker

## Installing

- Clone this directory down and `cd` into it
- With docker installed, build the project `docker build . -t codetriage`

## Running

### Bash

Generating the triage spreadsheet for you to review:

`docker run -ti --rm -v ${PWD}:/src codetriage -m triage -a YOUR_ACCESS_TOKEN_OR_LOCATION -u TARGET_ORG_OR_USER`

Pulling the repositories marked in the triage spreadsheet `triage.csv` into a `repos` folder (ensuring it's written into the mounted /src folder):

`docker run -ti --rm -v ${PWD}:/src codetriage -m triage -a YOUR_ACCESS_TOKEN_OR_LOCATION -d /src/repos/ -t triage.csv`

# Running Locally

# Install

- git clone this repository
- Ensure you have poetry installed
- cd into the directory and run `poetry install`

# Running

Generating the triage spreadsheet for you to review:

`poetry run python codetriage.py -m triage -a YOUR_ACCESS_TOKEN_OR_LOCATION -u TARGET_ORG_OR_USER`

Pulling the repositories marked in the triage spreadsheet `triage.csv` into a `repos` folder:

`poetry run python codetriage.py -m triage -a YOUR_ACCESS_TOKEN_OR_LOCATION -d repos/ -t triage.csv`

# Triage Sheet

The triage sheet is designed to give you an overview of a number of repositories for a given user or organisation. The sheet will contain the following columns:

- `Name`: The name of the repository
- `Owner`: The owner of the repository
- `Pull Y/N`: A column to mark if the repository should be pulled
- `Pull Branch/Tag`:
  - A column to mark what branch or tag should be pulled. 
  - If the repository is marked for pull, but this column is empty, the default branch will be pulled
  - \* can be used to pull all branches
- `Notes`: A column for any notes you want to make about the repository
- `Empty`: A column to mark if the repository is empty (where it has been created but nothing has been pushed yet)
- `Archived`: A column to mark if the repository is archived
- `Fork`: A column to mark if the repository is a fork
- `Description`: The description of the repository
- `Forks`: The number of forks the repository has
- `Open Issues`: The number of open issues the repository has (if this information is available)
- `Last Updated`: The date the repository was last updated
- `URL`: The URL to the repository for general browsing
- `Clone URL`: The URL to clone the repository
- `Default Branch`: The default branch of the repository
- `Branch List`: A list of branches in the repository
- `Release Tags`: The number of release tags for the repository
- `Latest Tag`: The latest release tag for the repository

**Note**: Do not edit the `Pull (Y/N)`, `Pull Branch/Tag`, `Default Branch` or `Clone URL` columns as they are used by the tool to determine what to pull.

# Running Tests

To run tests against the code base run the following:

```bash
python -m unittest discover -s tests
```

# TODO List

- [ ] Local configuration file for access tokens and other settings
- [ ] Support for multiple output formats
    - [x] CSV
    - [ ] Excel
- [ ] Functionality for checking the timestamp of each branches commit
- [ ] Functionality for checking each branch of a fork to see the timestamp of last commit and how many commits ahead and behind of target branch
- Support for more SCM platforms
    - [ ] GitLab
    - [ ] BitBucket
    - [ ] Azure DevOps
- [ ] Implement scan mode - run a set of predefined commands at the root of each repository to gather information