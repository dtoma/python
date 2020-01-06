from invoke import task


@task
def fmt(c):
    c.run("black ./python/ ./tests/")


@task
def test(c):
    c.run("python -m unittest")


@task
def clear_poetry_cache(c):
    """https://github.com/python-poetry/poetry/issues/728"""
    c.run("poetry cache:clear --all pypi")


@task
def lint(c):
    c.run("mypy ./python/ ./tests/")
