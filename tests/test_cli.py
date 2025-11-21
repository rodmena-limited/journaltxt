"""Tests for CLI module."""


import pytest

from journaltxt.cli import create_parser, jo_main, main


def test_create_parser():
    """Test parser creation."""
    parser = create_parser()

    assert parser.prog == "journaltxt"
    assert parser.description is not None


def test_parser_defaults():
    """Test parser default values."""
    parser = create_parser()
    args = parser.parse_args([])

    assert args.files == ["journal.txt"]
    assert args.verbose is False
    assert args.outpath == "."
    assert args.name is None
    assert args.date is True


def test_parser_verbose():
    """Test -v/--verbose flag."""
    parser = create_parser()

    args = parser.parse_args(["-v"])
    assert args.verbose is True

    args = parser.parse_args(["--verbose"])
    assert args.verbose is True


def test_parser_output():
    """Test -o/--output option."""
    parser = create_parser()

    args = parser.parse_args(["-o", "_posts"])
    assert args.outpath == "_posts"

    args = parser.parse_args(["--output", "output"])
    assert args.outpath == "output"


def test_parser_name():
    """Test -n/--name option."""
    parser = create_parser()

    args = parser.parse_args(["-n", "Vienna"])
    assert args.name == "Vienna"

    args = parser.parse_args(["--name", "Berlin"])
    assert args.name == "Berlin"


def test_parser_date_flags():
    """Test --date/--no-date flags."""
    parser = create_parser()

    args = parser.parse_args(["--date"])
    assert args.date is True

    args = parser.parse_args(["--no-date"])
    assert args.date is False


def test_parser_files():
    """Test positional file arguments."""
    parser = create_parser()

    args = parser.parse_args(["vienna.txt"])
    assert args.files == ["vienna.txt"]

    args = parser.parse_args(["file1.txt", "file2.txt", "file3.txt"])
    assert args.files == ["file1.txt", "file2.txt", "file3.txt"]


def test_main_basic(data_dir, tmp_output):
    """Test main function with basic arguments."""
    journal_path = str(data_dir / "journal.txt")

    result = main(["-o", str(tmp_output), journal_path])

    assert result == 0
    assert len(list(tmp_output.glob("*.md"))) == 5


def test_main_vienna(data_dir, tmp_output):
    """Test main function with Vienna.txt."""
    vienna_path = str(data_dir / "vienna.txt")

    result = main(["-o", str(tmp_output), "-n", "Vienna", "--no-date", vienna_path])

    assert result == 0
    assert len(list(tmp_output.glob("*.md"))) == 3


def test_main_multiple_files(data_dir, tmp_output):
    """Test main function with multiple files."""
    journal_path = str(data_dir / "journal.txt")
    vienna_path = str(data_dir / "vienna.txt")

    result = main(["-o", str(tmp_output), journal_path, vienna_path])

    assert result == 0
    # 5 from journal + 3 from vienna = 8 total
    assert len(list(tmp_output.glob("*.md"))) == 8


def test_main_file_not_found(tmp_output):
    """Test main function with non-existent file."""
    result = main(["-o", str(tmp_output), "nonexistent.txt"])

    assert result == 1


def test_main_verbose(data_dir, tmp_output, capsys):
    """Test main function with verbose flag."""
    journal_path = str(data_dir / "journal.txt")

    result = main(["-v", "-o", str(tmp_output), journal_path])

    assert result == 0

    captured = capsys.readouterr()
    assert ":: Config :::" in captured.out
    assert ":: Files :::" in captured.out


def test_main_default_journal_txt(tmp_path, monkeypatch):
    """Test main function defaults to journal.txt."""
    # Create a temporary journal.txt in the temp directory
    journal_file = tmp_path / "journal.txt"
    journal_file.write_text(
        """---
year: 2017
month: 7
day: 19
---
Content.
"""
    )

    # Change to temp directory
    monkeypatch.chdir(tmp_path)

    result = main([])

    assert result == 0
    assert (tmp_path / "2017-07-19-journal.md").exists()


def test_jo_main(data_dir, tmp_output):
    """Test jo_main alias function."""
    journal_path = str(data_dir / "journal.txt")

    result = jo_main(["-o", str(tmp_output), journal_path])

    assert result == 0
    assert len(list(tmp_output.glob("*.md"))) == 5


def test_main_creates_output_dir(data_dir, tmp_path):
    """Test that main creates output directory if it doesn't exist."""
    journal_path = str(data_dir / "journal.txt")
    output_dir = tmp_path / "new" / "output" / "dir"

    result = main(["-o", str(output_dir), journal_path])

    assert result == 0
    assert output_dir.exists()
    assert len(list(output_dir.glob("*.md"))) == 5


def test_main_with_all_options(data_dir, tmp_output):
    """Test main with all options combined."""
    vienna_path = str(data_dir / "vienna.txt")

    result = main(
        [
            "-v",
            "-o",
            str(tmp_output),
            "-n",
            "Vienna",
            "--no-date",
            vienna_path,
        ]
    )

    assert result == 0
    files = list(tmp_output.glob("*.md"))
    assert len(files) == 3

    # Check that files have correct names
    assert (tmp_output / "2017-07-17-vienna.md").exists()


def test_parser_version(capsys):
    """Test --version flag."""
    parser = create_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--version"])

    assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "journaltxt" in captured.out


def test_main_error_handling_verbose(tmp_output):
    """Test error handling in verbose mode."""
    # Pass a directory instead of a file to trigger an error
    # In verbose mode, exceptions are re-raised
    with pytest.raises(IsADirectoryError):
        main(["-v", "-o", str(tmp_output), str(tmp_output)])


def test_main_empty_args_missing_file(tmp_path, monkeypatch):
    """Test main with no args when journal.txt doesn't exist."""
    # Change to temp directory with no journal.txt
    monkeypatch.chdir(tmp_path)

    result = main([])

    # Should fail because journal.txt doesn't exist
    assert result == 1
