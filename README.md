# Atoti Project Template

This template can be used to start Atoti projects where the goal is to [go into production rather than prototyping in a notebook](https://docs.atoti.io/latest/deployment/going_from_a_notebook_to_an_app.html).

On top of the `atoti` package, it comes with:

- Dependency management with [Poetry](https://python-poetry.org)
- Config management with [Pydantic Settings](https://docs.pydantic.dev/2.6/concepts/pydantic_settings)
- Testing with [pytest](https://docs.pytest.org)
- Type checking with [mypy](http://mypy-lang.org)
- Formatting and linting with [Ruff](https://docs.astral.sh/ruff)
- Continuous testing with [GitHub Actions](https://github.com/features/actions)

## Usage

### Installation

- [Install `poetry`](https://python-poetry.org/docs/#installation)
- Install the dependencies:

  ```bash
  poetry install
  ```

### Commands

To start the app:

```bash
poetry run python -m main
```

Other useful commands can be found in [`test.yml`](.github/workflows/test.yml).

## Variants

This repository has the following long-lived branches showcasing different aspects:

- [`deploy-to-aws`](https://github.com/atoti/project-template/tree/deploy-to-aws) for deploying on AWS ECS.
- [`deploy-to-heroku`](https://github.com/atoti/project-template/tree/deploy-to-heroku) for a one-click deploy to Heroku.
