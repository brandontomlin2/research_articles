class ReadmeManager:
    def __init__(self, filepath='README.md'):
        """Initialize the README manager with a filepath.
        
        Args:
            filepath (str): Path to the README.md file
        """
        self.filepath = filepath
        self.content = []
        self._load_content()
    
    @staticmethod
    def create_link(text, url):
        """Create a Markdown link.
        
        Args:
            text (str): The text to display for the link
            url (str): The URL the link points to
            
        Returns:
            str: Formatted Markdown link
        """
        # Escape any pipe characters in the text or URL to prevent table formatting issues
        text = text.replace('|', '\\|')
        url = url.replace('|', '%7C')
        return f'[{text}]({url})'
    
    @staticmethod
    def create_image_link(alt_text, image_url, link_url=None):
        """Create a Markdown image with an optional link wrapper.
        
        Args:
            alt_text (str): Alternative text for the image
            image_url (str): URL of the image
            link_url (str, optional): URL to link the image to
            
        Returns:
            str: Formatted Markdown image with optional link
        """
        # Escape any pipe characters
        alt_text = alt_text.replace('|', '\\|')
        image_url = image_url.replace('|', '%7C')
        image = f'![{alt_text}]({image_url})'
        
        if link_url:
            link_url = link_url.replace('|', '%7C')
            return f'[{image}]({link_url})'
        return image
    
    def _load_content(self):
        """Load existing content from the file if it exists."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read().splitlines()
        except FileNotFoundError:
            self.content = []
    
    def save(self):
        """Save the current content to the README file."""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.content) + '\n')
    
    def add_header(self, text, level=1):
        """Add a header to the README.
        
        Args:
            text (str): Header text
            level (int): Header level (1-6)
        """
        level = max(1, min(6, level))  # Ensure level is between 1 and 6
        self.content.append(f'\n{"#" * level} {text}\n')
    
    def add_text(self, text):
        """Add text content to the README.
        
        Args:
            text (str): Text content to add
        """
        self.content.append(f'{text}\n')
    
    def create_table(self, headers):
        """Create a new table with the specified headers.
        
        Args:
            headers (list): List of column headers
        """
        # Add header row
        header_row = '| ' + ' | '.join(headers) + ' |'
        # Add separator row with alignment
        separator_row = '| ' + ' | '.join(['---'] * len(headers)) + ' |'
        
        self.content.extend(['', header_row, separator_row])
    
    def add_table_row(self, values):
        """Add a row to the last table in the README.
        
        Args:
            values (list): List of values for the row
        """
        row = '| ' + ' | '.join(str(value) for value in values) + ' |'
        self.content.append(row)
    
    def find_table_indices(self):
        """Find the start and end indices of all tables in the content.
        
        Returns:
            list: List of tuples containing (start_index, end_index) for each table
        """
        tables = []
        start_idx = None
        
        for i, line in enumerate(self.content):
            if line.startswith('|') and i + 1 < len(self.content) and '---' in self.content[i + 1]:
                start_idx = i
            elif start_idx is not None and (not line.startswith('|') or i == len(self.content) - 1):
                end_idx = i if not line.startswith('|') else i + 1
                tables.append((start_idx, end_idx))
                start_idx = None
                
        return tables
    
    def add_column(self, header, values=None):
        """Add a new column to the last table in the README.
        
        Args:
            header (str): Header for the new column
            values (list, optional): Values for the new column. If None, fills with empty strings.
        """
        tables = self.find_table_indices()
        if not tables:
            raise ValueError("No tables found in the README")
        
        start_idx, end_idx = tables[-1]
        rows = self.content[start_idx:end_idx]
        
        # Update header row
        header_parts = rows[0].split('|')
        header_parts.insert(-1, f' {header} ')
        self.content[start_idx] = '|'.join(header_parts)
        
        # Update separator row
        separator_parts = rows[1].split('|')
        separator_parts.insert(-1, ' --- ')
        self.content[start_idx + 1] = '|'.join(separator_parts)
        
        # Update data rows
        if values is None:
            values = [''] * (len(rows) - 2)
        
        for i, value in enumerate(values, start=2):
            if start_idx + i < end_idx:
                row_parts = self.content[start_idx + i].split('|')
                row_parts.insert(-1, f' {value} ')
                self.content[start_idx + i] = '|'.join(row_parts)

# Example usage:
if __name__ == "__main__":
    # Create a new README manager
    readme = ReadmeManager('README.md')
    
    # Add a main header
    readme.add_header('Research')
    
    # Add some description
    readme.add_text('Below you will find a list of all the research / articles that I have read and found interesting.')
    
    # Add a subheader
    readme.add_header('Articles', level=2)
    
    # Create a table with links
    readme.create_table(['Title', 'Summary'])
    
    # Create some links and add rows
    docs_link = readme.create_link('SCIENCEAGENTBENCH:TOWARD RIGOROUS ASSESSMENT OF LANGUAGE AGENTS FOR DATA-DRIVEN SCIENTIFIC DISCOVERY', 
                                   'docs/2410.05080v2.pdf')
    readme.add_table_row(['SCIENCEAGENTBENCH:TOWARD RIGOROUS ASSESSMENT OF LANGUAGE AGENTS FOR DATA-DRIVEN SCIENTIFIC DISCOVERY',  docs_link])
    
    
    # Add a row with multiple links in one cell
    # docs_links = (
    #     readme.create_link('Setup', 'https://docs.example.com/setup') + ' | ' +
    #     readme.create_link('Guide', 'https://docs.example.com/guide')
    # )
    # readme.add_table_row(['Documentation', 'In Progress', docs_links, ''])
    
    # Save the changes
    readme.save()