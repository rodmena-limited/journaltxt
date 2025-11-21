"""journaltxt - Build Jekyll blog posts from Journal.TXT single-file format.

Journal.TXT is a simple single-file format for writing journal entries
and blog posts. This package converts Journal.TXT files into individual
Jekyll blog posts with YAML frontmatter.

Example:
    >>> from journaltxt import build_file
    >>> build_file('Vienna.txt', outpath='_posts', name='Vienna')

For command-line usage:
    $ journaltxt -o _posts Vienna.txt
    $ jo -o _posts Vienna.txt  # short alias
"""

from .builder import Builder, build, build_file
from .parser import Parser, ParserError
from .version import __version__, get_banner, get_version

__all__ = [
    "Parser",
    "ParserError",
    "Builder",
    "build",
    "build_file",
    "__version__",
    "get_version",
    "get_banner",
]
