# Before the Work Start

Before you start contributing to the project, you should install `pre-commit`

```bash
pip install pre-commit
```

Then, you should install the pre-commit hooks

```bash
pre-commit install
```

After that, you can start working on the project.


# Installation

To be able to contribute to Malevich Library, you should install the following dependencies:

```bash
pip install -r requirements.dev.txt
```



# Git Flow

We use the following git flow:

- Create a new branch from `main` with the name `feature/<feature-name>` or `fix/<fix-name>`
     1. In case several people work on the same feature, you can create a branch with the name `feature/<feature-name>/<your-name>` to avoid conflicts (e.g. `feature/feature-name/alex`)
- Once you are done with the feature, create a pull request to `dev`
- Once the pull request is approved, merge it to `dev`
- Once the `dev` branch is stable, merge it to `main`
- Once the `main` branch is stable, create a release with the version `vX.Y.Z` and tag it with the same name
- Once a fix is required, create a branch from `main` with the name `hotfix/<hotfix-name>`
- Once the hotfix is done, create a pull request to `main`

## Commit Style

We use the following commit style:
- `add`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `upd`: A code change that neither fixes a bug nor adds a feature
- `misc`: Other changes


# Code Style

We use `ruff` to format the code. You can run the following command to format the code

```bash
ruff check ./
```

# Testing

We use `pytest` to test the code. You can run the following command to run the tests

```bash
pytest
```

# Workflows

We use GitHub Actions to run the following workflows:

- `ruff`: Running Ruff Python formatter

