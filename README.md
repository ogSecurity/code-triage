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
- Support for more SCM platforms
    - [ ] GitLab
    - [ ] BitBucket
    - [ ] Azure DevOps