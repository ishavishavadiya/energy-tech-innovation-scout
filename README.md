# 🔋 Energy Tech Innovation Scout (arXiv + LLM)

This project is a Python-based research scouting tool designed to identify **recent innovations in the Energy Technology domain**. It automatically retrieves newly published research papers from the **arXiv API**, filters them based on relevance and recency, and uses a **Large Language Model (LLM)** to generate concise, innovation-focused summaries.

The final output is a structured report highlighting the **top 5 most recent energy-tech innovations**, provided in both **Markdown** and **JSON** formats.

---

## 🚀 Key Features

- Queries the **arXiv API** for recent Energy Tech–related research papers
- Parses **Atom XML** responses using `feedparser`
- Filters papers based on:
  - Publication date (recent papers only)
  - Keyword relevance in abstracts
- Uses an **LLM** to generate concise insights highlighting:
  - Key innovations
  - Technologies or methods used
  - Potential energy-related applications
- Produces a **Top-5 innovation report**
- Batched LLM requests to remain **rate-limit safe**

---

## 🧠 Technologies Used

- **Python 3.9+**
- **arXiv API** (Atom XML format)
- `feedparser` – XML parsing
- `requests` – API requests
- `python-dateutil` – timezone-safe date handling
- `openai` – LLM integration  
  *(The LLM provider can be swapped with Gemini or Claude with minimal changes)*

---

## 📁 Project Structure

```text
energy_tech_scout/
├── scout.py
├── config.py
├── requirements.txt
├── README.md
└── output/
    ├── report.md
    └── report.json


---

⚙️ Setup Instructions
1️⃣ Prerequisites

Python 3.9 or higher

Internet connection

An API key for an LLM provider (e.g., OpenAI)

---

2️⃣ Install Dependencies

(Optional but recommended: use a virtual environment)

python3 -m venv venv
source venv/bin/activate


Install required packages:

pip install -r requirements.txt

---

3️⃣ Configure API Key

Edit config.py and add your API key:

OPENAI_API_KEY = "YOUR_API_KEY"

You may also customize:

SEARCH_QUERY

DAYS_LOOKBACK

TOP_K

---

▶️ How to Run the Project

From the project root directory, run:

python3 scout.py

---

📄 Output

After execution, results are saved in the output/ folder:

report.md – Human-readable innovation report

report.json – Machine-readable structured output

Each entry includes:

Paper title

Authors

Publication date

PDF link

LLM-generated innovation summary

---

⚠️ Assumptions & Design Decisions

arXiv is used as the primary research source

Only recently published papers (configurable time window) are considered

Keyword-based filtering is used for relevance

LLM summaries are generated using a single batched request to avoid API rate limits

Internet access is required for both arXiv and LLM API calls

API usage limits depend on the chosen LLM provider