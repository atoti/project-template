# atoti Project Template

This template can be used to start atoti projects where the goal is to go into production rather than prototyping in a notebook.

On top of the `atoti` package, it comes with:

- Dependency management with [Poetry](https://python-poetry.org/)
- Testing with [pytest](https://docs.pytest.org/)
- Type checking with [mypy](http://mypy-lang.org/)
- Formatting with [Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/)
- Linting with [Pylint](https://www.pylint.org/)
- Continuous testing with [GitHub Actions](https://github.com/features/actions)

## Usage

### Installation

- [Install `poetry`](https://python-poetry.org/docs/#installation)
- Install the dependencies:

  ```console
  poetry install
  ```

### Commands

- Start the session:

  ```console
  poetry run python -m app
  ```

- Run the tests:

  ```console
  poetry run pytest
  ```

- Check the types:

  ```console
  poetry run mypy --package app --package tests --show-error-codes
  ```

- Sort the imports:

  ```console
  poetry run isort app/ tests/
  ```

- Format the code:

  ```console
  poetry run black app/ tests/
  ```

- Lint the code:

  ```console
  poetry run pylint app/ tests/
  ```

## Variants

This repository has the following long-lived branches showcasing different aspects:

- [`deploy-to-heroku`](https://github.com/atoti/project-template/tree/deploy-to-heroku) for a one-click deploy to Heroku.
