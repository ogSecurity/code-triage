# CodeTriage

Code Triage is a tool that can be used by security consultants and their clients for a number of use cases:

- Generating a spreadsheet containing a list of repostories can easily be walked through manually to
    - Mark if the repository should be in scope for review
    - Select what branches or tagged releases should be in scope
- Using the marked up sheet, the repositories can be pulled for offline analysis

## Access Tokens and Authentication

### GitHub

You can generate an access token if you have a GitHub account by following the guide [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

If you're using `Tokens (classic)` the only permission you'll need is `public_repo` under `repo`. If you want to be able to access provide repos you should tick `repo` to select the entire tree.

## Installing (docker)

- Clone this directory down and `cd` into it
- With docker installed, build the project `docker build . -t codetriage`

## Running (Docker)

### PowerShell

`docker run -ti --rm -v ${PWD}:/src codetriage -m triage -a YOUR_ACCESS_TOKEN -u TARGET_ORG_OR_USER`

## Running Tests

To run tests against the code base run the following:

```bash
python -m unittest discover -s tests
```

# TODO List

- [ ] Local configuration file for access tokens and other settings
- [ ] Support for multiple output formats
    - [ ] CSV
    - [ ] Excel
- Support for more SCM platforms
    - [ ] GitLab
    - [ ] BitBucket
    - [ ] Azure DevOps