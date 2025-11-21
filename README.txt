journaltxt - Build Jekyll Blog Posts from Journal.TXT
=====================================================

journaltxt is a Python tool that converts single-file journal entries in the
Journal.TXT format into individual Jekyll blog posts with YAML frontmatter.

Write your journal entries in a simple, human-readable format, and automatically
generate a complete blog with properly formatted posts for Jekyll static site
generators.


Features
--------

* Simple single-file format for journal/blog entries
* Automatic conversion to Jekyll posts (YYYY-MM-DD-title.md format)
* YAML frontmatter generation with metadata
* Flexible date formats (full dates, abbreviated months, day-of-week)
* Inherits year and month for subsequent entries
* Command-line interface with intuitive options
* Both 'journaltxt' and 'jo' (short alias) commands
* Preserves custom metadata fields
* Creates output directories automatically
* Full test coverage with pytest
* Type hints for better IDE support
* Format and lint with ruff


Installation
------------

Install from PyPI:

    pip install journaltxt

Or install from source:

    git clone https://github.com/journaltxt/journaltxt
    cd journaltxt/python-rewrite/journaltxt
    pip install -e .


Quick Start
-----------

1. Create a journal.txt file:

    ---
    year:  2017
    month: July
    day:   Mon 17
    ---

    Jumping on tram #1 in front of the Staatsoper (state opera house).
    Circling the Ringstrasse for a great tour with a public transport ticket.

    ---
    day:   Tue 18
    ---

    Visiting the imperial palace Schönbrunn - the former summer residence
    of the Habsburg family.

    ---
    day:   Wed 19
    ---

    Visiting the Sigmund Freud Museum. Too much culture - need a beer!

2. Convert to Jekyll posts:

    journaltxt -o _posts journal.txt

3. Your posts are ready in the _posts directory!


Journal.TXT Format
------------------

The Journal.TXT format uses YAML frontmatter delimited by "---" to separate
entries. Each entry consists of:

1. Metadata block (YAML format)
2. Content (Markdown or plain text)

Example:

    ---
    year:  2017
    month: July
    day:   Mon 17
    ---
    Your journal entry content here.
    ---
    day:   Tue 18
    ---
    Next entry content.

The first entry must include year, month, and day. Subsequent entries can
omit year and month (they inherit from the previous entry).


Date Format Options
-------------------

Year:
    - Numeric: year: 2017

Month:
    - Full name: month: July
    - Abbreviated: month: Jul
    - Numeric: month: 7

Day:
    - With day-of-week: day: Mon 17
    - Numeric only: day: 17


Command-Line Usage
------------------

Basic usage:

    journaltxt [OPTIONS] [FILES...]

If no files are specified, defaults to "journal.txt" in the current directory.

Options:

    -o, --output PATH
        Output directory for generated posts (default: current directory)

    -n, --name NAME
        Journal name for post titles (default: filename without .txt)

    --date / --no-date
        Include/exclude date in post titles (default: --date)

    -v, --verbose
        Show debug messages and configuration

    --version
        Show version and exit

    -h, --help
        Show help message and exit

Short alias:

    jo [OPTIONS] [FILES...]


Examples
--------

Convert Vienna.txt to posts in _posts directory:

    journaltxt -o _posts Vienna.txt

Use short alias:

    jo -o _posts Vienna.txt

Process multiple files:

    journaltxt -o _posts Vienna.txt Berlin.txt Paris.txt

Customize journal name:

    journaltxt -o _posts -n "Travel Diary" vienna.txt

Disable date in titles:

    journaltxt -o _posts --no-date journal.txt

Default behavior (processes journal.txt):

    journaltxt
    jo

Verbose output for debugging:

    journaltxt -v -o _posts Vienna.txt


Output Format
-------------

Each journal entry is converted to a Jekyll post with:

Filename:
    YYYY-MM-DD-name.md
    Example: 2017-07-17-vienna.md

Content:
    ---
    # Journal.TXT entry 1/3 - auto-built on 2024-11-21 by journaltxt/1.0.0
    date: 2017-07-17
    title: Vienna - Day 1 - Mon, 17 Jul
    ---

    Your journal content here.

The YAML frontmatter includes:
- Auto-build comment with timestamp
- date: Entry date as YAML date object
- title: Auto-generated title (customizable)
- Any custom metadata from your original entry


Custom Metadata
---------------

Add any custom YAML fields to your entries, and they'll be preserved in the
output:

    ---
    year: 2017
    month: July
    day: Mon 17
    author: John Doe
    tags: [travel, vienna, europe]
    location: Vienna, Austria
    weather: sunny
    ---

    Your content here.

All custom fields (author, tags, location, weather) will appear in the
generated Jekyll post's frontmatter.


Python API
----------

You can also use journaltxt as a Python library:

    from journaltxt import build_file, build, Parser

    # Build from a file
    build_file('Vienna.txt', outpath='_posts', name='Vienna')

    # Build from text
    text = '''---
    year: 2017
    month: 7
    day: 19
    ---
    Content here.
    '''
    build(text, outpath='_posts')

    # Parse only (without building)
    items = Parser.parse_text(text)
    for metadata, content in items:
        print(f"Date: {metadata['date']}")
        print(f"Content: {content}")


Development
-----------

Install development dependencies:

    pip install -e ".[dev]"

Run tests:

    pytest

Run tests with coverage:

    pytest --cov=journaltxt --cov-report=html

Format code with ruff:

    ruff format .

Lint code:

    ruff check .

Fix linting issues automatically:

    ruff check --fix .


Project Structure
-----------------

    journaltxt/
    ├── src/journaltxt/
    │   ├── __init__.py      # Public API
    │   ├── version.py       # Version information
    │   ├── parser.py        # Journal.TXT parser
    │   ├── builder.py       # Jekyll post builder
    │   └── cli.py           # Command-line interface
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py      # Pytest fixtures
    │   ├── data/            # Test data files
    │   ├── test_version.py
    │   ├── test_parser.py   # Parser tests
    │   ├── test_builder.py  # Builder tests
    │   └── test_cli.py      # CLI tests
    ├── pyproject.toml       # Project configuration
    └── README.txt           # This file


Requirements
------------

- Python 3.10 or higher
- PyYAML >= 6.0


Similar Projects
----------------

This is a Python port of the original Ruby journaltxt gem:
https://github.com/journaltxt/journaltxt

The Journal.TXT format and specification:
https://journaltxt.github.io


License
-------

Copyright 2024 Farshid Ashouri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Contributing
------------

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

Please ensure:
- All tests pass (pytest)
- Code is formatted (ruff format)
- No linting errors (ruff check)
- Add tests for new features


Support
-------

- Issues: https://github.com/journaltxt/journaltxt/issues
- Discussions: https://github.com/journaltxt/journaltxt/discussions
- Email: farsheed.ashouri@gmail.com


Authors
-------

- Farshid Ashouri <farsheed.ashouri@gmail.com>

Based on the original Ruby implementation by Gerald Bauer and contributors.


Changelog
---------

Version 1.0.0 (2024-11-21)
- Initial Python implementation
- Full feature parity with Ruby version
- Comprehensive test suite
- Type hints and modern Python features
- Ruff formatting and linting
- PyPI packaging
