"""Tests for parser module."""

from datetime import date

import pytest

from journaltxt.parser import Parser, ParserError


def test_parser_basic():
    """Test basic parsing functionality."""
    text = """---
year: 2017
month: July
day: 19
---
First entry content.
---
day: 20
---
Second entry content.
"""
    items = Parser.parse_text(text)

    assert len(items) == 2

    # Check first entry
    meta1, content1 = items[0]
    assert meta1["date"] == date(2017, 7, 19)
    assert content1 == "First entry content.\n"

    # Check second entry
    meta2, content2 = items[1]
    assert meta2["date"] == date(2017, 7, 20)
    assert content2 == "Second entry content.\n"


def test_parser_with_day_format():
    """Test parsing with formatted day (e.g., 'Mon 17')."""
    text = """---
year: 2017
month: July
day: Mon 17
---
Content here.
"""
    items = Parser.parse_text(text)

    assert len(items) == 1
    meta, content = items[0]
    assert meta["date"] == date(2017, 7, 17)


def test_parser_month_name():
    """Test parsing with month names."""
    text = """---
year: 2017
month: July
day: 15
---
Content.
"""
    items = Parser.parse_text(text)

    meta, _ = items[0]
    assert meta["date"] == date(2017, 7, 15)


def test_parser_abbreviated_month():
    """Test parsing with abbreviated month names."""
    text = """---
year: 2017
month: Jul
day: 15
---
Content.
"""
    items = Parser.parse_text(text)

    meta, _ = items[0]
    assert meta["date"] == date(2017, 7, 15)


def test_parser_inherits_year_month():
    """Test that subsequent entries inherit year and month."""
    text = """---
year: 2017
month: 7
day: 19
---
First.
---
day: 20
---
Second.
---
day: 21
---
Third.
"""
    items = Parser.parse_text(text)

    assert len(items) == 3
    assert items[0][0]["date"] == date(2017, 7, 19)
    assert items[1][0]["date"] == date(2017, 7, 20)
    assert items[2][0]["date"] == date(2017, 7, 21)


def test_parser_preserves_metadata():
    """Test that custom metadata is preserved."""
    text = """---
year: 2017
month: 7
day: 19
custom_field: custom_value
tags: [tag1, tag2]
---
Content.
"""
    items = Parser.parse_text(text)

    meta, _ = items[0]
    assert meta["custom_field"] == "custom_value"
    assert meta["tags"] == ["tag1", "tag2"]
    assert meta["date"] == date(2017, 7, 19)


def test_parser_missing_year_first_entry():
    """Test that missing year in first entry raises error."""
    text = """---
month: 7
day: 19
---
Content.
"""
    with pytest.raises(ParserError, match="year entry required"):
        Parser.parse_text(text)


def test_parser_missing_month_first_entry():
    """Test that missing month in first entry raises error."""
    text = """---
year: 2017
day: 19
---
Content.
"""
    with pytest.raises(ParserError, match="month entry required"):
        Parser.parse_text(text)


def test_parser_missing_day():
    """Test that missing day raises error."""
    text = """---
year: 2017
month: 7
---
Content.
"""
    with pytest.raises(ParserError, match="day entry required"):
        Parser.parse_text(text)


def test_parser_invalid_day_format():
    """Test that invalid day format raises error."""
    text = """---
year: 2017
month: 7
day: Invalid
---
Content.
"""
    with pytest.raises(ParserError, match="invalid day format"):
        Parser.parse_text(text)


def test_parser_invalid_date():
    """Test that invalid date raises error."""
    text = """---
year: 2017
month: 2
day: 30
---
Content.
"""
    with pytest.raises(ParserError, match="invalid date"):
        Parser.parse_text(text)


def test_parser_journal_txt(journal_txt):
    """Test parsing journal.txt fixture."""
    items = Parser.parse_text(journal_txt)

    assert len(items) == 5
    assert items[0][0]["date"] == date(2017, 7, 19)
    assert items[1][0]["date"] == date(2017, 7, 20)
    assert items[2][0]["date"] == date(2017, 7, 21)
    assert items[3][0]["date"] == date(2017, 7, 22)
    assert items[4][0]["date"] == date(2017, 7, 23)


def test_parser_vienna_txt(vienna_txt):
    """Test parsing vienna.txt fixture."""
    items = Parser.parse_text(vienna_txt)

    assert len(items) == 3
    assert items[0][0]["date"] == date(2017, 7, 17)
    assert items[1][0]["date"] == date(2017, 7, 18)
    assert items[2][0]["date"] == date(2017, 7, 19)


def test_parser_class_method():
    """Test Parser class instantiation and parse method."""
    text = """---
year: 2017
month: 7
day: 19
---
Content.
"""
    parser = Parser(text)
    items = parser.parse()

    assert len(items) == 1
    assert items[0][0]["date"] == date(2017, 7, 19)


def test_parser_empty_metadata():
    """Test parsing with minimal metadata."""
    text = """---
year: 2017
month: 7
day: 19
---
Content.
---
day: 20
---
More content.
"""
    items = Parser.parse_text(text)

    assert len(items) == 2
    assert "date" in items[0][0]
    assert "date" in items[1][0]


def test_parser_multiline_content():
    """Test parsing with multiline content."""
    text = """---
year: 2017
month: 7
day: 19
---
Line 1
Line 2
Line 3

Paragraph 2
"""
    items = Parser.parse_text(text)

    meta, content = items[0]
    assert "Line 1" in content
    assert "Line 2" in content
    assert "Line 3" in content
    assert "Paragraph 2" in content


def test_parser_invalid_yaml():
    """Test that invalid YAML raises error."""
    text = """---
year: 2017
month: 7
day: [invalid yaml structure
---
Content.
"""
    with pytest.raises(ParserError, match="Invalid YAML"):
        Parser.parse_text(text)
