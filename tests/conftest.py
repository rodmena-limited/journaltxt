"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def data_dir() -> Path:
    """Return path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def journal_txt(data_dir: Path) -> str:
    """Load journal.txt test data."""
    return (data_dir / "journal.txt").read_text(encoding="utf-8")


@pytest.fixture
def vienna_txt(data_dir: Path) -> str:
    """Load vienna.txt test data."""
    return (data_dir / "vienna.txt").read_text(encoding="utf-8")


@pytest.fixture
def tmp_output(tmp_path: Path) -> Path:
    """Create temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir
