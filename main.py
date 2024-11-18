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
            "source": "https://arxiv.org/pdf/2410.05080v2.pdf",
        },
        {
            "title": "Combining Language Models and Knowledge Graphs for Effective Information Retrieval",
            "url": "docs/Combining_Language_Models_and_Knowledge_Graphs_for_Effective_Information_Retrieval.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2407.06564v1",
        },
        {
            "title": "Transforming Asset Servicing With AI, Oracles, and Blockchains",
            "url": "docs/transforming-asset-servicing.pdf",
            "summary": "",
            "source": "https://pages.chain.link/hubfs/e/transforming-asset-servicing.pdf",
        },
        {
            "title": "CRISPR-GPT: An LLM Agent for Automated Design of Gene-Editing Experiments",
            "url": "docs/2024.04.25.591003v3.full.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2404.18021",
        },
        {
            "title": "Impact of Code Transformation on Detection of Smart Contract Vulnerabilities",
            "url": "docs/2410.21685.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2410.21685.pdf",
        },
        {
            "title": "Attention Is All You Need for LLM-based Code Vulnerability Localization",
            "url": "docs/2410.15288v1.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2410.15288v1.pdf",
        },
        {
            "title": "Leveraging Fine-Tuned Language Models for Efficient and Accurate Smart Contract Auditing",
            "url": "docs/2410.13918v1.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2410.13918v1.pdf",
        },
        {
            "title": "LLM-SmartAudit: Advanced Smart Contract Vulnerability Detection",
            "url": "docs/2410.09381v1.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2410.09381v1.pdf",
        },
        {
            "title": "CountChain: A Decentralized Oracle Network for Counting Systems",
            "url": "docs/2409.11592v1.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2409.11592v1.pdf",
        },
        {
            "title": "Semantic Interoperability on Blockchain by Generating Smart Contracts Based on Knowledge Graphs",
            "url": "docs/2409.12171v1.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2409.12171v1.pdf",
        },
        {
            "title": "Detect Llama - Finding Vulnerabilities in Smart Contracts using Large Language Models",
            "url": "docs/2407.08969v1.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2407.08969v1.pdf",
        },
        {
            "title": "Vulnerability Detection in Smart Contracts: A Comprehensive Survey",
            "url": "docs/2407.07922v1.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2407.07922v1.pdf",
        },
        {
            "title": "Gorilla: Large Language Model Connected withMassive APIs",
            "url": "docs/2305.15334v1.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2305.15334v1.pdf",
        },
        {
            "title": "MAD: Move AI Decompiler to Improve Transparency and Auditability on Non-Open-Source Blockchain Smart Contract",
            "url": "docs/2410.15275.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2410.15275",
        },
        {
            "title": "Financial Statement Analysis with Large Language Models",
            "url": "docs/BFI_WP_2024-65.pdf",
            "summary": "",
            "source": "https://bfi.uchicago.edu/wp-content/uploads/2024/05/BFI_WP_2024-65.pdf",
        },
        {
            "title": "Artificial Intelligence, Scientific Discovery, and Product Innovation*",
            "url": "docs/AI_innovation.pdf",
            "summary": "",
            "source": "https://aidantr.github.io/files/AI_innovation.pdf",
        },
        {
            "title": "LONGMEMEVAL: BENCHMARKING CHAT ASSISTANTS ON LONG-TERM INTERACTIVE MEMORY",
            "url": "docs/AI_science.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2410.10813",
        },
        {
            "title": "LIGHTWEIGHT NEURAL APP CONTROL",
            "url": "docs/2410.17883.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2410.17883",
        },
        {
            "title": "miniCTX: Neural Theorem Proving with (Long-)Contexts",
            "url": "docs/2408.03350.pdf",
            "summary": "",
            "source": "https://www.arxiv.org/pdf/2408.03350",
        },
        {
            "title": "The Moral Case for Using Language Model Agents for Recommendation",
            "url": "docs/2410.12123.pdf",
            "summary": "",
            "source": "https://arxiv.org/abs/2410.12123", 
        },
        {
            "title": "Towards Edge General Intelligence via LargeLanguage Models: Opportunities and Challenges",
            "url": "docs/2410.18125v1.pdf",
            "summary": "",
            "source": "https://arxiv.org/pdf/2410.18125", 
        }
    ]

    for article in articles:
        doc_link = readme.create_link(article["title"], article["source"])

        readme.add_table_row([
            doc_link,
            article["summary"]
            ])

    readme.save()


if __name__ == "__main__":
    main()
