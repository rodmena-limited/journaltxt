"""Tests for builder module."""

from datetime import date

import yaml

from journaltxt.builder import Builder, build, build_file


def test_builder_defaults():
    """Test Builder default configuration."""
    builder = Builder()

    assert builder.opts["outpath"] == "."
    assert builder.opts["date"] is True
    assert builder.opts["verbose"] is False
    assert builder.opts["name"] == "Journal"


def test_builder_custom_opts():
    """Test Builder with custom options."""
    builder = Builder(outpath="_posts", name="Vienna", date=False, verbose=True)

    assert builder.opts["outpath"] == "_posts"
    assert builder.opts["name"] == "Vienna"
    assert builder.opts["date"] is False
    assert builder.opts["verbose"] is True


def test_build_basic(tmp_output):
    """Test basic build functionality."""
    text = """---
year: 2017
month: 7
day: 19
---
Test content.
"""
    build(text, outpath=str(tmp_output), name="Test")

    # Check output file was created
    expected_file = tmp_output / "2017-07-19-test.md"
    assert expected_file.exists()

    # Read and verify content
    content = expected_file.read_text(encoding="utf-8")
    assert "---" in content
    assert "Test content." in content
    assert "title:" in content


def test_build_title_with_date(tmp_output):
    """Test that title includes date when date=True."""
    text = """---
year: 2017
month: 7
day: Mon 17
---
Content.
"""
    build(text, outpath=str(tmp_output), name="Vienna", date=True)

    expected_file = tmp_output / "2017-07-17-vienna.md"
    content = expected_file.read_text(encoding="utf-8")

    # Parse YAML frontmatter
    yaml_content = content.split("---")[1]
    meta = yaml.safe_load(yaml_content)

    assert meta["title"] == "Vienna - Day 1 - Mon, 17 Jul"


def test_build_title_without_date(tmp_output):
    """Test that title excludes date when date=False."""
    text = """---
year: 2017
month: 7
day: 17
---
Content.
"""
    build(text, outpath=str(tmp_output), name="Vienna", date=False)

    expected_file = tmp_output / "2017-07-17-vienna.md"
    content = expected_file.read_text(encoding="utf-8")

    # Parse YAML frontmatter
    yaml_content = content.split("---")[1]
    meta = yaml.safe_load(yaml_content)

    assert meta["title"] == "Vienna - Day 1"


def test_build_journal_name(tmp_output):
    """Test that 'Journal' name is not added to title."""
    text = """---
year: 2017
month: 7
day: 19
---
Content.
"""
    build(text, outpath=str(tmp_output), name="Journal")

    expected_file = tmp_output / "2017-07-19-journal.md"
    content = expected_file.read_text(encoding="utf-8")

    yaml_content = content.split("---")[1]
    meta = yaml.safe_load(yaml_content)

    # Title should not include "Journal -"
    assert not meta["title"].startswith("Journal -")
    assert meta["title"].startswith("Day 1")


def test_build_multiple_entries(tmp_output):
    """Test building multiple entries."""
    text = """---
year: 2017
month: 7
day: 19
---
First entry.
---
day: 20
---
Second entry.
---
day: 21
---
Third entry.
"""
    build(text, outpath=str(tmp_output), name="Test")

    # Check all files were created
    assert (tmp_output / "2017-07-19-test.md").exists()
    assert (tmp_output / "2017-07-20-test.md").exists()
    assert (tmp_output / "2017-07-21-test.md").exists()

    # Verify day numbers in titles
    for day, expected_day_num in [(19, 1), (20, 2), (21, 3)]:
        filepath = tmp_output / f"2017-07-{day}-test.md"
        content = filepath.read_text(encoding="utf-8")
        yaml_content = content.split("---")[1]
        meta = yaml.safe_load(yaml_content)
        assert f"Day {expected_day_num}" in meta["title"]


def test_build_preserves_metadata(tmp_output):
    """Test that custom metadata is preserved in output."""
    text = """---
year: 2017
month: 7
day: 19
author: John Doe
tags: [travel, blog]
custom: value
---
Content.
"""
    build(text, outpath=str(tmp_output))

    expected_file = tmp_output / "2017-07-19-journal.md"
    content = expected_file.read_text(encoding="utf-8")

    yaml_content = content.split("---")[1]
    meta = yaml.safe_load(yaml_content)

    assert meta["author"] == "John Doe"
    assert meta["tags"] == ["travel", "blog"]
    assert meta["custom"] == "value"


def test_build_file_basic(data_dir, tmp_output):
    """Test build_file with journal.txt."""
    journal_path = data_dir / "journal.txt"
    build_file(journal_path, outpath=str(tmp_output))

    # Should create 5 files (journal.txt has 5 entries)
    files = list(tmp_output.glob("*.md"))
    assert len(files) == 5


def test_build_file_vienna(data_dir, tmp_output):
    """Test build_file with vienna.txt."""
    vienna_path = data_dir / "vienna.txt"
    build_file(vienna_path, outpath=str(tmp_output), name="Vienna", date=False)

    # Should create 3 files
    files = list(tmp_output.glob("*.md"))
    assert len(files) == 3

    # Check filenames
    assert (tmp_output / "2017-07-17-vienna.md").exists()
    assert (tmp_output / "2017-07-18-vienna.md").exists()
    assert (tmp_output / "2017-07-19-vienna.md").exists()


def test_build_file_derives_name_from_filename(data_dir, tmp_output):
    """Test that build_file uses filename as default name."""
    vienna_path = data_dir / "vienna.txt"
    build_file(vienna_path, outpath=str(tmp_output))

    # Files should be named vienna (lowercase)
    assert (tmp_output / "2017-07-17-vienna.md").exists()


def test_build_creates_output_directory(tmp_path):
    """Test that build creates output directory if it doesn't exist."""
    text = """---
year: 2017
month: 7
day: 19
---
Content.
"""
    output_dir = tmp_path / "nested" / "output" / "dir"
    build(text, outpath=str(output_dir))

    assert output_dir.exists()
    assert (output_dir / "2017-07-19-journal.md").exists()


def test_build_yaml_comment(tmp_output):
    """Test that YAML frontmatter includes auto-build comment."""
    text = """---
year: 2017
month: 7
day: 19
---
Content.
"""
    build(text, outpath=str(tmp_output))

    expected_file = tmp_output / "2017-07-19-journal.md"
    content = expected_file.read_text(encoding="utf-8")

    # Check for comment in YAML
    assert "Journal.TXT entry 1/1" in content
    assert "auto-built on" in content
    assert "journaltxt/" in content


def test_build_content_separation(tmp_output):
    """Test that content is properly separated from YAML."""
    text = """---
year: 2017
month: 7
day: 19
---
Line 1
Line 2

Paragraph 2
"""
    build(text, outpath=str(tmp_output))

    expected_file = tmp_output / "2017-07-19-journal.md"
    content = expected_file.read_text(encoding="utf-8")

    # Content should come after the second ---
    parts = content.split("---")
    assert len(parts) >= 3
    actual_content = parts[2].strip()
    assert actual_content.startswith("Line 1")


def test_builder_class_build_file(data_dir, tmp_output):
    """Test Builder class build_file method."""
    builder = Builder(outpath=str(tmp_output), name="TestJournal")
    journal_path = data_dir / "journal.txt"

    builder.build_file(journal_path)

    files = list(tmp_output.glob("*.md"))
    assert len(files) == 5


def test_builder_class_build(tmp_output):
    """Test Builder class build method."""
    builder = Builder(outpath=str(tmp_output))
    text = """---
year: 2017
month: 7
day: 19
---
Content.
"""
    builder.build(text)

    assert (tmp_output / "2017-07-19-journal.md").exists()


def test_build_date_in_yaml(tmp_output):
    """Test that date is included in YAML frontmatter."""
    text = """---
year: 2017
month: 7
day: 19
---
Content.
"""
    build(text, outpath=str(tmp_output))

    expected_file = tmp_output / "2017-07-19-journal.md"
    content = expected_file.read_text(encoding="utf-8")

    yaml_content = content.split("---")[1]
    meta = yaml.safe_load(yaml_content)

    assert "date" in meta
    assert meta["date"] == date(2017, 7, 19)
