import os
import logging
from typing import List, Tuple, Optional
from pathlib import Path

class ReadmeManager:
    """A class to manage README.md files with support for headers, tables, and links."""
    
    def __init__(self, filepath: str = 'README.md', preserve_existing: bool = False):
        """Initialize the README manager.
        
        Args:
            filepath: Path to the README.md file
            preserve_existing: If True, keeps existing content. If False, starts fresh.
            
        Raises:
            PermissionError: If file operations fail due to permissions
            OSError: If file operations fail for other reasons
        """
        self.logger = self._setup_logging()
        self.filepath = Path(filepath)
        self.content: List[str] = []
        
        try:
            self._initialize_file(preserve_existing)
        except Exception as e:
            self.logger.error(f"Failed to initialize README manager: {str(e)}")
            raise
    
    @staticmethod
    def _setup_logging() -> logging.Logger:
        """Set up logging configuration.
        
        Returns:
            logging.Logger: Configured logger instance
        """
        logger = logging.getLogger('ReadmeManager')
        if not logger.handlers:  # Avoid adding handlers multiple times
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _initialize_file(self, preserve_existing: bool) -> None:
        """Initialize the file, either preserving or deleting existing content.
        
        Args:
            preserve_existing: If True, keeps existing content. If False, starts fresh.
        """
        if not preserve_existing and self.filepath.exists():
            try:
                self.filepath.unlink()
                self.logger.info(f"Deleted existing file: {self.filepath}")
            except PermissionError as e:
                self.logger.error(f"Permission error deleting {self.filepath}: {str(e)}")
                raise
            except Exception as e:
                self.logger.error(f"Error deleting {self.filepath}: {str(e)}")
                raise

        if preserve_existing:
            self._load_content()

    def _load_content(self) -> None:
        """Load existing content from the file if it exists."""
        try:
            if self.filepath.exists():
                self.content = self.filepath.read_text(encoding='utf-8').splitlines()
        except Exception as e:
            self.logger.error(f"Error loading content: {str(e)}")
            raise

    def save(self) -> None:
        """Save the current content to the README file."""
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            self.filepath.write_text('\n'.join(self.content) + '\n', encoding='utf-8')
            self.logger.info(f"Successfully saved content to {self.filepath}")
        except Exception as e:
            self.logger.error(f"Error saving content: {str(e)}")
            raise

    @staticmethod
    def create_link(text: str, url: str) -> str:
        """Create a Markdown link with proper escaping.
        
        Args:
            text: The text to display for the link
            url: The URL the link points to
            
        Returns:
            Formatted Markdown link
        """
        text = text.replace('|', '\\|').strip()
        url = url.replace('|', '%7C').strip()
        return f'[{text}]({url})'

    @staticmethod
    def create_image_link(alt_text: str, image_url: str, link_url: Optional[str] = None) -> str:
        """Create a Markdown image with an optional link wrapper.
        
        Args:
            alt_text: Alternative text for the image
            image_url: URL of the image
            link_url: Optional URL to link the image to
            
        Returns:
            Formatted Markdown image with optional link
        """
        alt_text = alt_text.replace('|', '\\|').strip()
        image_url = image_url.replace('|', '%7C').strip()
        image = f'![{alt_text}]({image_url})'
        
        if link_url:
            link_url = link_url.replace('|', '%7C').strip()
            return f'[{image}]({link_url})'
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
        self.content.append(f'{text}\n')

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
        header_row = '| ' + ' | '.join(headers) + ' |'
        separator_row = '| ' + ' | '.join(['---'] * len(headers)) + ' |'
        
        self.content.extend(['', header_row, separator_row])
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
        row = '| ' + ' | '.join(values) + ' |'
        self.content.append(row)

def main():
    """Main function to demonstrate usage of ReadmeManager."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        readme = ReadmeManager(
            filepath='README.md',
            preserve_existing=False
        )

        readme.add_header('Research')
        readme.add_text('Below you will find a list of research / articles that I have read and found interesting.')
        readme.add_text('If you would like to contribute to this list, please open a PR.')

        readme.add_header('Articles', level=2)
        readme.create_table(['Title', 'Summary'])

        # Define articles
        articles = [
            {
                'title': 'SCIENCEAGENTBENCH: TOWARD RIGOROUS ASSESSMENT OF LANGUAGE AGENTS FOR DATA-DRIVEN SCIENTIFIC DISCOVERY',
                'url': 'docs/2410.05080v2.pdf',
                'summary': ''
            },
            {
                'title': 'Combining Language Models and Knowledge Graphs for Effective Information Retrieval',
                'url': 'docs/Combining_Language_Models_and_Knowledge_Graphs_for_Effective_Information_Retrieval.pdf',
                'summary': ''
            },
            {
                'title': 'Transforming Asset Servicing With AI, Oracles, and Blockchains',
                'url': 'docs/transforming-asset-servicing-with-ai-oracles-and-blockchains.pdf',
                'summary': ''
            }
        ]

        # Add articles to table
        for article in articles:
            link = readme.create_link(article['title'], article['url'])
            readme.add_table_row([link, article['summary']])

        # Save the changes
        readme.save()
        logger.info("Successfully created README.md")

    except Exception as e:
        logger.error(f"Error creating README: {str(e)}")
        raise

if __name__ == "__main__":
    main()