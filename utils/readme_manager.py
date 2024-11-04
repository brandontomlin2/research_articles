import os
import logging
from pathlib import Path
from typing import List, Optional
from .config_manager import ConfigManager


class ReadmeManager:
    """A class to manage README.md files with support for headers, tables, and links."""

    def __init__(self, filepath: Optional[str] = None, preserve_existing: bool = False):
        """Initialize the README manager.

        Args:
            filepath: Path to the README.md file (optional, uses config if not provided)
            preserve_existing: If True, keeps existing content. If False, starts fresh
        """
        # Initialize configuration
        self.config = ConfigManager()
        self.logger = self._setup_logging()

        # Initialize filepath from args or config
        self.filepath = Path(
            filepath or self.config.get("file_settings", "default_file")
        )
        self.content: List[str] = []

        try:
            self._initialize_file(preserve_existing)
        except Exception as e:
            self.logger.error(f"Failed to initialize README manager: {str(e)}")
            raise

    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger("ReadmeManager")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                self.config.get(
                    "logging",
                    "format",
                    fallback="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                )
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            level = self.config.get("logging", "level", fallback="INFO")
            logger.setLevel(getattr(logging, level))
        return logger

    def _initialize_file(self, preserve_existing: bool) -> None:
        """Initialize the file, either preserving or deleting existing content."""
        if not preserve_existing and self.filepath.exists():
            if self.config.getboolean("file_settings", "backup_enabled", fallback=True):
                self._create_backup()

            try:
                self.filepath.unlink()
                self.logger.info(f"Deleted existing file: {self.filepath}")
            except Exception as e:
                self.logger.error(f"Error deleting {self.filepath}: {str(e)}")
                raise

        if preserve_existing:
            self._load_content()

    def _create_backup(self) -> None:
        """Create a backup of the existing file if backup is enabled."""
        try:
            backup_dir = Path(
                self.config.get(
                    "file_settings", "backup_directory", fallback=".backups"
                )
            )
            backup_dir.mkdir(parents=True, exist_ok=True)

            # Create timestamped backup
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"README_{timestamp}.md.bak"

            # Copy file to backup location
            import shutil

            shutil.copy2(self.filepath, backup_path)
            self.logger.info(f"Created backup at {backup_path}")

        except Exception as e:
            self.logger.warning(f"Failed to create backup: {str(e)}")

    def _load_content(self) -> None:
        """Load existing content from the file if it exists."""
        try:
            if self.filepath.exists():
                self.content = self.filepath.read_text(encoding="utf-8").splitlines()
        except Exception as e:
            self.logger.error(f"Error loading content: {str(e)}")
            raise

    def save(self) -> None:
        """Save the current content to the README file."""
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            self.filepath.write_text("\n".join(self.content) + "\n", encoding="utf-8")
            self.logger.info(f"Successfully saved content to {self.filepath}")
        except Exception as e:
            self.logger.error(f"Error saving content: {str(e)}")
            raise

    @staticmethod
    def create_link(text: str, url: str) -> str:
        """Create a Markdown link.

        Args:
            text: The text to display for the link
            url: The URL the link points to

        Returns:
            Formatted Markdown link
        """
        text = text.replace("|", "\\|").strip()
        url = url.replace("|", "%7C").strip()
        return f"[{text}]({url})"

    @staticmethod
    def create_image_link(
        alt_text: str, image_url: str, link_url: Optional[str] = None
    ) -> str:
        """Create a Markdown image with an optional link wrapper.

        Args:
            alt_text: Alternative text for the image
            image_url: URL of the image
            link_url: Optional URL to link the image to

        Returns:
            Formatted Markdown image with optional link
        """
        alt_text = alt_text.replace("|", "\\|").strip()
        image_url = image_url.replace("|", "%7C").strip()
        image = f"![{alt_text}]({image_url})"

        if link_url:
            link_url = link_url.replace("|", "%7C").strip()
            return f"[{image}]({link_url})"
        return image

    def add_header(self, text: str, level: int = 1) -> None:
        """Add a header to the README.

        Args:
            text: Header text
            level: Header level (1-6)
        """
        level = max(1, min(6, level))
        self.content.append(f'\n{"#" * level} {text.strip()}\n')
        self.logger.debug(f"Added level {level} header: {text}")

    def add_text(self, text: str) -> None:
        """Add text content to the README.

        Args:
            text: Text content to add
        """
        self.content.append(f"{text}\n")

    def create_table(self, headers: List[str]) -> None:
        """Create a new table with the specified headers.

        Args:
            headers: List of column headers

        Raises:
            ValueError: If headers list is empty
        """
        if not headers:
            raise ValueError("Headers list cannot be empty")

        # Strip whitespace from headers
        headers = [h.strip() for h in headers]
        header_row = "| " + " | ".join(headers) + " |"
        separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"

        self.content.extend(["", header_row, separator_row])
        self.logger.debug(f"Created table with headers: {headers}")

    def add_table_row(self, values: List[str]) -> None:
        """Add a row to the last table in the README.

        Args:
            values: List of values for the row

        Raises:
            ValueError: If values list is empty
        """
        if not values:
            raise ValueError("Values list cannot be empty")

        # Convert all values to strings and strip whitespace
        values = [str(v).strip() for v in values]
        row = "| " + " | ".join(values) + " |"
        self.content.append(row)

    def find_table_indices(self) -> List[tuple]:
        """Find the start and end indices of all tables in the content.

        Returns:
            List of tuples containing (start_index, end_index) for each table
        """
        tables = []
        start_idx = None

        for i, line in enumerate(self.content):
            if (
                line.startswith("|")
                and i + 1 < len(self.content)
                and "---" in self.content[i + 1]
            ):
                start_idx = i
            elif start_idx is not None and (
                not line.startswith("|") or i == len(self.content) - 1
            ):
                end_idx = i if not line.startswith("|") else i + 1
                tables.append((start_idx, end_idx))
                start_idx = None

        return tables

    def add_column(self, header: str, values: Optional[List[str]] = None) -> None:
        """Add a new column to the last table in the README.

        Args:
            header: Header for the new column
            values: Optional list of values for the new column

        Raises:
            ValueError: If no tables exist in the README
        """
        tables = self.find_table_indices()
        if not tables:
            raise ValueError("No tables found in the README")

        start_idx, end_idx = tables[-1]
        rows = self.content[start_idx:end_idx]

        # Update header row
        header_parts = rows[0].split("|")
        header_parts.insert(-1, f" {header.strip()} ")
        self.content[start_idx] = "|".join(header_parts)

        # Update separator row
        separator_parts = rows[1].split("|")
        separator_parts.insert(-1, " --- ")
        self.content[start_idx + 1] = "|".join(separator_parts)

        # Update data rows
        if values is None:
            values = [""] * (len(rows) - 2)

        for i, value in enumerate(values, start=2):
            if start_idx + i < end_idx:
                row_parts = self.content[start_idx + i].split("|")
                row_parts.insert(-1, f" {str(value).strip()} ")
                self.content[start_idx + i] = "|".join(row_parts)
