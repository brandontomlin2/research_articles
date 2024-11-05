from pathlib import Path
from utils import ReadmeManager


def main():
    root_dir = Path(__file__).parent
    readme_path = root_dir / "README.md"

    readme = ReadmeManager(
        filepath=str(readme_path.absolute()),
        preserve_existing=False,
    )

    readme.add_header("Research")
    readme.add_text(
        "Below you will find a list of all the research / articles that I have read and found interesting."
    )
    readme.add_text("If you would like to contribute to this list, please open a PR.")
    readme.add_header("Articles", level=2)
    readme.create_table(["Title", "Summary"])

    articles = [
        {
            "title": "SCIENCEAGENTBENCH: TOWARD RIGOROUS ASSESSMENT OF LANGUAGE AGENTS FOR DATA-DRIVEN SCIENTIFIC DISCOVERY",
            "url": "docs/2410.05080v2.pdf",
            "summary": "",
        },
        {
            "title": "Combining Language Models and Knowledge Graphs for Effective Information Retrieval",
            "url": "docs/Combining_Language_Models_and_Knowledge_Graphs_for_Effective_Information_Retrieval.pdf",
            "summary": "",
        },
        {
            "title": "Transforming Asset Servicing With AI, Oracles, and Blockchains",
            "url": "docs/transforming-asset-servicing.pdf",
            "summary": "",
        },
        {
            "title": "CRISPR-GPT: An LLM Agent for Automated Design of Gene-Editing Experiments",
            "url": "docs/2024.04.25.591003v3.full.pdf",
            "summary": "",
        },
    ]

    for article in articles:
        link = readme.create_link(article["title"], article["url"])
        readme.add_table_row([link, article["summary"]])
    readme.save()


if __name__ == "__main__":
    main()
