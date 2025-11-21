"""Parser for Journal.TXT format."""

import re
from datetime import date
from typing import Any

import yaml


class ParserError(Exception):
    """Exception raised for parsing errors."""

    pass


class Parser:
    """Parser for Journal.TXT single-file format.

    Parses journal entries separated by --- delimiters with YAML frontmatter.
    """

    def __init__(self, text: str):
        """Initialize parser with journal text.

        Args:
            text: Journal text in Journal.TXT format
        """
        self.text = text

    def parse(self) -> list[tuple[dict[str, Any], str]]:
        """Parse journal text into entries.

        Returns:
            List of tuples containing (metadata_dict, content_string) for each entry

        Raises:
            ParserError: If required fields are missing or invalid
        """
        # Remove leading first separator --- if present
        text = re.sub(r"^---[ ]*\n?", "", self.text, count=1)

        # Split on separator lines
        blocks = re.split(r"^---[ ]*\n?", text, flags=re.MULTILINE)

        # Group into pairs of (metadata, content)
        items = []
        for i in range(0, len(blocks), 2):
            if i + 1 < len(blocks):
                items.append((blocks[i], blocks[i + 1]))
            elif blocks[i].strip():  # Handle last block without content
                items.append((blocks[i], ""))

        # Process metadata blocks
        last_page_date = None
        parsed_items = []

        for i, (meta_text, content) in enumerate(items):
            # Parse YAML metadata
            try:
                page_meta = yaml.safe_load(meta_text)
                if page_meta is None:
                    page_meta = {}
            except yaml.YAMLError as e:
                raise ParserError(f"Invalid YAML in entry {i + 1}: {e}") from e

            # Extract date components
            year = page_meta.pop("year", None)
            month = page_meta.pop("month", None)
            day = page_meta.pop("day", None)

            # Process year
            if year is None:
                if last_page_date:
                    year = last_page_date.year
                else:
                    raise ParserError(
                        f"Entry {i + 1}: year entry required for first entry"
                    )

            # Process day (required for all entries)
            if day is None:
                raise ParserError(f"Entry {i + 1}: day entry required")

            if isinstance(day, str):
                # Extract numeric day from strings like "Mon 17" or "17"
                nums_day = re.findall(r"\d+", day)
                if nums_day:
                    day = int(nums_day[0])
                else:
                    raise ParserError(f"Entry {i + 1}: invalid day format: {day}")

            # Process month
            if month is None:
                if last_page_date:
                    month = last_page_date.month
                else:
                    raise ParserError(
                        f"Entry {i + 1}: month entry required for first entry"
                    )

            if isinstance(month, str):
                # Parse month name to number
                try:
                    # Try to parse as month name
                    from datetime import datetime

                    month_str = month.strip()
                    # Try full month name or abbreviated
                    for fmt in ["%B", "%b"]:
                        try:
                            dt = datetime.strptime(month_str, fmt)
                            month = dt.month
                            break
                        except ValueError:
                            continue
                    else:
                        # If not a month name, might be a number
                        month = int(month_str)
                except (ValueError, TypeError) as e:
                    raise ParserError(
                        f"Entry {i + 1}: invalid month format: {month}"
                    ) from e

            # Create date object
            try:
                page_date = date(year, month, day)
            except ValueError as e:
                raise ParserError(
                    f"Entry {i + 1}: invalid date ({year}-{month}-{day}): {e}"
                ) from e

            last_page_date = page_date
            page_meta["date"] = page_date

            parsed_items.append((page_meta, content))

        return parsed_items

    @classmethod
    def parse_text(cls, text: str) -> list[tuple[dict[str, Any], str]]:
        """Convenience method to parse text directly.

        Args:
            text: Journal text in Journal.TXT format

        Returns:
            List of tuples containing (metadata_dict, content_string) for each entry
        """
        return cls(text).parse()
