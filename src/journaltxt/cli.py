"""Command-line interface for journaltxt."""

import argparse
import sys
from pathlib import Path

from .builder import build_file
from .version import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for journaltxt CLI.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="journaltxt",
        description="Build Jekyll blog posts from Journal.TXT single-file format",
        epilog=(
            "Example: journaltxt -o _posts Vienna.txt\n"
            "See https://journaltxt.github.io for more information"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "files",
        nargs="*",
        default=["journal.txt"],
        metavar="FILE",
        help="Journal.TXT files to process (default: journal.txt)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show debug messages",
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="outpath",
        default=".",
        metavar="PATH",
        help="Output directory path (default: .)",
    )

    parser.add_argument(
        "-n",
        "--name",
        metavar="NAME",
        help="Journal name (default: derived from filename)",
    )

    parser.add_argument(
        "--date",
        dest="date",
        action="store_true",
        default=True,
        help="Add date to page title (default: true)",
    )

    parser.add_argument(
        "--no-date",
        dest="date",
        action="store_false",
        help="Do not add date to page title",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"journaltxt {__version__}",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for journaltxt CLI.

    Args:
        argv: Command-line arguments (default: sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Build configuration from args
    config = {}

    if args.verbose:
        config["verbose"] = True
        print(":: Config :::")
        print(config)
        print(":: Files :::")
        print(args.files)

    if args.outpath != ".":
        config["outpath"] = args.outpath

    if args.name:
        config["name"] = args.name

    config["date"] = args.date

    # Process each file
    try:
        for filepath in args.files:
            path = Path(filepath)
            if not path.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                return 1

            build_file(path, **config)

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            raise
        return 1


def jo_main(argv: list[str] | None = None) -> int:
    """Entry point for 'jo' command (alias for journaltxt).

    Args:
        argv: Command-line arguments (default: sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    return main(argv)


if __name__ == "__main__":
    sys.exit(main())
