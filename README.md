# Atoti Project Template

This template can be used to start Atoti projects where the goal is to [go into production rather than prototyping in a notebook](https://docs.atoti.io/latest/deployment/going_from_a_notebook_to_an_app.html).

On top of the `atoti` package, it comes with:

- Dependency management with [Poetry](https://python-poetry.org)
- Settings management with [Pydantic](https://docs.pydantic.dev/latest/usage/settings)
- Testing with [pytest](https://docs.pytest.org)
- Type checking with [mypy](http://mypy-lang.org)
- Formatting with [Black](https://black.readthedocs.io)
- Linting with [Ruff](https://beta.ruff.rs)
- Continuous testing with [GitHub Actions](https://github.com/features/actions)

## Usage

### Installation

- [Install `poetry`](https://python-poetry.org/docs/#installation)
- Install the dependencies:

  ```bash
  poetry install
  ```

### Commands

To get a list of the commands that can be executed to interact with the project, run:

```bash
poetry run app --help
```

A few examples:

- Start the app:

  ```bash
  poetry run app start
  ```

- Launch the tests:

  ```bash
  poetry run app test
  ```

- Reformat the code:

  ```bash
  poetry run app format
  ```

## Variants

This repository has the following long-lived branches showcasing different aspects:

- [`deploy-to-aws`](https://github.com/atoti/project-template/tree/deploy-to-aws) for deploying on AWS ECS.
- [`deploy-to-heroku`](https://github.com/atoti/project-template/tree/deploy-to-heroku) for a one-click deploy to Heroku.
