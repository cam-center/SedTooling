import nox
from nox_poetry import Session, session

nox.options.sessions = ["test", "coverage", "lint"]
locations = "src", "tests"


@session(python=["3.8", "3.9", "3.10", "3.11"])
def test(s: Session):
    s.install(".", "pytest", "pytest-cov", "pytest-timeout")
    s.env["COVERAGE_FILE"] = f".coverage.{s.python}"
    s.run("python", "-m", "pytest", "--cov", "sed_converter")


@session(venv_backend="none")
def coverage(s: Session):
    s.run("coverage", "combine")
    s.run("coverage", "html")
    s.run("coverage", "xml", "--fail-under=100")


@session(venv_backend="none")
def fmt(s: Session) -> None:
    s.run("ruff", "check", ".", "--select", "I", "--fix")
    s.run("black", ".")


@session(venv_backend="none")
def lint(s: Session) -> None:
    s.run("black", "--check", ".")
    s.run("ruff", "check", ".")


@nox.session(venv_backend="none")
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.run("mypy", *args)
