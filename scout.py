import feedparser
import requests
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import json
import openai
from config import *

openai.api_key = OPENAI_API_KEY


# ---------------------------
# 1. Fetch arXiv papers
# ---------------------------
def fetch_arxiv_papers():
    params = {
        "search_query": SEARCH_QUERY,
        "start": 0,
        "max_results": MAX_RESULTS,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    response = requests.get(ARXIV_BASE_URL, params=params)
    feed = feedparser.parse(response.text)
    return feed.entries


# ---------------------------
# 2. Filter papers
# ---------------------------
from datetime import datetime, timedelta, timezone
from dateutil import parser as date_parser

def filter_recent_papers(entries):
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_LOOKBACK)
    filtered = []

    for entry in entries:
        published = date_parser.parse(entry.published)

        # published is already timezone-aware (UTC)
        if published >= cutoff_date:
            filtered.append({
                "title": entry.title.strip().replace("\n", " "),
                "abstract": entry.summary.strip().replace("\n", " "),
                "authors": [a.name for a in entry.authors],
                "published": published.strftime("%Y-%m-%d"),
                "pdf_link": entry.links[1].href
            })

    return filtered[:TOP_K]


# ---------------------------
# 3. LLM summarization
# ---------------------------
def summarize_batch_with_llm(papers):
    combined_prompt = """
You are an expert energy technology analyst.

For EACH paper below:
- Summarize in 2–3 sentences
- Highlight key innovation
- Mention technologies/methods
- Mention potential energy applications

Return results as a numbered list matching paper order.
"""

    for i, p in enumerate(papers, 1):
        combined_prompt += f"""
Paper {i}
Title: {p['title']}
Abstract: {p['abstract']}
"""

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You analyze research papers."},
            {"role": "user", "content": combined_prompt}
        ],
        temperature=0.4
    )

    summaries = response.choices[0].message.content.strip().split("\n\n")
    return summaries


# ---------------------------
# 4. Build final report
# ---------------------------
def build_report(papers):
    summaries = summarize_batch_with_llm(papers)

    for paper, summary in zip(papers, summaries):
        paper["llm_summary"] = summary

    return papers



# ---------------------------
# 5. Save outputs
# ---------------------------
def save_outputs(report):
    # JSON
    with open("output/report.json", "w") as f:
        json.dump(report, f, indent=2)

    # Markdown
    with open("output/report.md", "w") as f:
        f.write("# 🔋 Energy Tech Innovation Scout – Top 5\n\n")

        for i, p in enumerate(report, 1):
            f.write(f"## {i}. {p['title']}\n")
            f.write(f"**Authors:** {', '.join(p['authors'])}\n\n")
            f.write(f"**Published:** {p['published']}\n\n")
            f.write(f"**PDF:** {p['pdf_link']}\n\n")
            f.write(f"**LLM Insight:**\n{p['llm_summary']}\n\n")
            f.write("---\n\n")


# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    print("🔍 Fetching arXiv papers...")
    entries = fetch_arxiv_papers()

    print("🧹 Filtering recent papers...")
    recent_papers = filter_recent_papers(entries)

    print("🤖 Generating LLM insights...")
    report = build_report(recent_papers)

    print("📄 Saving report...")
    save_outputs(report)

    print("✅ Done! Check the output/ folder.")
