from pathlib import Path
from readme_manager import ReadmeManager

def main():
    # Initialize the ReadmeManager
    # This will automatically load the config and handle the README file
    readme = ReadmeManager()

    # Add main header
    readme.add_header('Research')
    readme.add_text('Below you will find a list of all the research / articles that I have read and found interesting.')

    # Add Articles section
    readme.add_header('Articles', level=2)
    readme.create_table(['Title', 'Summary'])

    # Define your articles
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

    # Add articles to the table
    for article in articles:
        link = readme.create_link(article['title'], article['url'])
        readme.add_table_row([link, article['summary']])

    # Save the changes
    readme.save()

if __name__ == "__main__":
    main()