# atoti Project Template

This template can be used to start atoti projects where the goal is to go into production rather than prototyping in a notebook.

On top of the `atoti` package, it comes with:

- Dependency management with [Poetry](https://python-poetry.org/)
- Testing with [pytest](https://docs.pytest.org/)
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
  poetry run python -m project
  ```

- Run the tests:

  ```bash
  poetry run pytest
  ```

- Format the code:

  ```bash
  poetry run black project/ tests/
  ```

- Sort the imports:

  ```bash
  poetry run isort project/ tests/
  ```

- Lint the code:

  ```bash
  poetry run pylint project/ tests/
  ```
