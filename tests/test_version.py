"""Tests for version module."""

import re

from journaltxt import __version__, get_banner, get_version


def test_version_format():
    """Test that version follows semantic versioning."""
    assert re.match(r"^\d+\.\d+\.\d+$", __version__)


def test_get_version():
    """Test get_version() returns version string."""
    version = get_version()
    assert version == __version__
    assert isinstance(version, str)


def test_get_banner():
    """Test get_banner() returns formatted banner."""
    banner = get_banner()
    assert "journaltxt" in banner
    assert __version__ in banner
    assert "Python" in banner
