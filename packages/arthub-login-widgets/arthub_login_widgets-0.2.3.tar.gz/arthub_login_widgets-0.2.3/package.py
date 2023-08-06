"""Contains information and properties pertaining to Rez package."""
name = "arthub_login_widgets"
authors = ["Joey Ding"]
uuid = "f295388e-ad31-40da-8daa-6d0e9e7bac7b"
description = "A Qt Widget for login ArtHub."
homepage = "https://git.woa.com/lightbox/internal/arthub_login_widgets"
tools = []
build_requires = []
private_build_requires = [
    "rez_builder-0",
    "setuptools_scm-1.15",
]
requires = [
    "python-2.7..3.10",
    "arthub_api-1",
    "lightbox_ui-0",
    "platformdirs-2.0",
]
# Internal variable used by `rezolve_me` for dev environment.
# Overrides `requires`. Uncomment this only if needed.
dev_requires = requires + ["pytest-4.6", "pytest_cov-2.10", "pytest_qt-3.2", "pyqt5-5.15", "pytest_mock-1.10"]
variants = []

_TEST_COMMAND = "pytest --pyargs arthub_login_widgets  --cov arthub_login_widgets"
tests = {
    "python-2.7": {
        "command": _TEST_COMMAND,
        "requires": ["pytest-4.6", "python-2.7", "pyside-1.2", "pytest_qt-3.2", "pytest_mock-1.10", "pytest_cov-2.10"],
    },
    "python-3.7": {
        "command": _TEST_COMMAND,
        "requires": ["pytest-4.6", "python-3.7", "pyqt5-5.15", "pytest_qt-3.2", "pytest_mock-1.10", "pytest_cov-2.10"],
    },
    "python-3.9": {
        "command": _TEST_COMMAND,
        "requires": ["pytest-4.6", "python-3.9", "pyqt5-5.15", "pytest_qt-3.2", "pytest_mock-1.10", "pytest_cov-2.10"],
    },
    "houdini-19.5": {
        "command": _TEST_COMMAND,
        "requires": ["pytest-4.6", "houdini-19.5", "pytest_qt-3.2", "pytest_mock-1.10", "pytest_cov-2.10"],
    },
    "mari-5": {
        "command": _TEST_COMMAND,
        "requires": ["pytest-4.6", "mari-5", "pytest_qt-3.2", "pytest_mock-1.10", "pytest_cov-2.10"],
    },
}


def commands():
    """Set up package."""
    env.PYTHONPATH.prepend("{this.root}/site-packages")  # noqa: F821
