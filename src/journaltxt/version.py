"""Version information for journaltxt."""

__version__ = "1.0.1"

MAJOR = 1
MINOR = 0
PATCH = 1


def get_version() -> str:
    """Get the current version string."""
    return __version__


def get_banner() -> str:
    """Get version banner with Python information."""
    import platform
    import sys

    return (
        f"journaltxt/{__version__} on Python {sys.version.split()[0]} "
        f"({platform.python_implementation()}) [{platform.platform()}]"
    )
