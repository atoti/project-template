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
  poetry run mypy --package app --package tests
  ```

- Lint the code:

  ```bash
  poetry run pylint app/ tests/
  ```

- Sort the imports:

  ```bash
  poetry run isort app/ tests/
  ```

- Format the code:

  ```bash
  poetry run black app/ tests/
  ```

### Deploying on Heroku

The application can be deployed easily on Heroku.

Since the dependencies in this project are managed with poetry, the following CLI commands are required to change the buildpacks:

```bash
heroku buildpacks:clear
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
heroku buildpacks:add heroku/python
```

With this config done, the [usual deployment procedure for Heroku apps can be followed](https://devcenter.heroku.com/articles/getting-started-with-python).

#### Heroku button

Click on the button below to automatically deploy this project on Heroku.
To deploy a project started from this template, remember to change the `repository` value in [app.json](app.json).

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
