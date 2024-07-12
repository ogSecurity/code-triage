# CodeTriage


## Access Tokens and Authentication

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