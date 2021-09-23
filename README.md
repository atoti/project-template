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

### Deploying on Heroku

The application can be deployed very easily on Heroku. Since we use poetry, you will need to add the following build packs using the CLI:

```bash
heroku buildpacks:clear
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
heroku buildpacks:add heroku/python
```

Heroku assigns the port that the application needs to bind to in the `PORT` environment variable.

You can automatically deploy this project to Heroku using this.
If you start a project using this template, remember to change the `repository` value in the `app.json` file to the URL of your repository.
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

With this config done, you can follow the normal deployment procedure for Heroku apps.
A tutorial can be found [here](https://devcenter.heroku.com/articles/getting-started-with-python).
