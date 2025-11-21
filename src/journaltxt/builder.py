"""Builder for converting Journal.TXT entries to Jekyll posts."""

from datetime import datetime
from pathlib import Path

import yaml

from .parser import Parser
from .version import __version__


class Builder:
    """Builds Jekyll posts from Journal.TXT entries."""

    DEFAULTS = {
        "outpath": ".",
        "date": True,  # include date in (auto-)title
        "verbose": False,
        "name": "Journal",
    }

    def __init__(self, **opts):
        """Initialize builder with options.

        Args:
            outpath: Output directory path (default: '.')
            name: Journal name (default: 'Journal')
            date: Include date in page title (default: True)
            verbose: Show debug messages (default: False)
        """
        self.opts = {**self.DEFAULTS, **opts}

    def build_file(self, path: str | Path, **opts) -> None:
        """Build Jekyll posts from a Journal.TXT file.

        Args:
            path: Path to Journal.TXT file
            **opts: Additional options to override defaults
        """
        path = Path(path)

        # Read file with UTF-8 encoding, removing BOM if present
        with open(path, encoding="utf-8-sig") as f:
            text = f.read()

        # Get basename without .txt extension for default name
        basename = path.stem

        # Use basename as name if not user-supplied
        build_opts = {**self.opts, **opts}
        if "name" not in opts:
            build_opts["name"] = basename

        self.build(text, **build_opts)

    def build(self, text: str, **opts) -> None:
        """Build Jekyll posts from Journal.TXT text.

        Args:
            text: Journal.TXT formatted text
            **opts: Build options (outpath, name, date, verbose)
        """
        build_opts = {**self.opts, **opts}

        outpath = Path(build_opts["outpath"])
        name = build_opts["name"]
        add_date = build_opts["date"]
        verbose = build_opts["verbose"]

        if verbose:
            print(":: Opts :::")
            print(build_opts)

        # Parse entries
        items = Parser.parse_text(text)

        # Add page titles to metadata
        for i, (page_meta, _) in enumerate(items):
            page_date = page_meta["date"]

            page_title = ""
            if name.lower() != "journal":
                # Don't add "default/generic" journal to title
                page_title = f"{name} - "

            page_title += f"Day {i + 1}"

            if add_date:
                # Format: "Mon, 17 Jul"
                page_title += f" - {page_date.strftime('%a, %-d %b')}"

            page_meta["title"] = page_title

        # Write entries to files
        for i, (page_meta, page_content) in enumerate(items):
            page_date = page_meta["date"]
            page_title = page_meta["title"]

            # Build output path: YYYY-MM-DD-name.md
            filename = f"{page_date}-{name.lower()}.md"
            filepath = outpath / filename

            # Create output directory if it doesn't exist
            filepath.parent.mkdir(parents=True, exist_ok=True)

            print(f"Writing entry {i + 1}/{len(items)} >{page_title}< to {filepath}...")

            # Create comment for YAML header
            comment = (
                f"Journal.TXT entry {i + 1}/{len(items)} - "
                f"auto-built on {datetime.now()} by journaltxt/{__version__}"
            )

            # Convert metadata to YAML
            yaml_text = yaml.dump(
                page_meta,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

            # Add comment to YAML header
            yaml_text = f"# {comment}\n{yaml_text}"

            # Write Jekyll post with YAML frontmatter
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(yaml_text)
                f.write("---\n\n")
                f.write(page_content)


def build_file(path: str | Path, **opts) -> None:
    """Convenience function to build from a file.

    Args:
        path: Path to Journal.TXT file
        **opts: Build options
    """
    builder = Builder(**opts)
    builder.build_file(path, **opts)


def build(text: str, **opts) -> None:
    """Convenience function to build from text.

    Args:
        text: Journal.TXT formatted text
        **opts: Build options
    """
    builder = Builder(**opts)
    builder.build(text, **opts)
