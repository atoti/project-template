# atoti Project Template

This template can be used to start atoti projects where the goal is to go into production rather than prototyping in a notebook.

On top of the `atoti` package, it comes with:

- Settings management with [pydantic](https://pydantic-docs.helpmanual.io/usage/settings/)
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

  ```bash
  poetry install
  ```

### Commands

- Start the session:

  ```bash
  poetry run python -m app
  ```

- Run the tests:

  ```bash
  poetry run pytest
  ```

- Check the types:

  ```bash
  poetry run typecheck
  ```

- Sort the imports:

  ```bash
  poetry run sort-imports --fix
  ```

- Format the code:

  ```bash
  poetry run format --fix
  ```

- Lint the code:

  ```bash
  poetry run lint
  ```

## Variants

This repository has the following long-lived branches showcasing different aspects:

- [`atoti-plus`](https://github.com/atoti/project-template/tree/atoti-plus) for upgrading to Atoti+.
- [`deploy-to-heroku`](https://github.com/atoti/project-template/tree/deploy-to-heroku) for a one-click deploy to Heroku.
