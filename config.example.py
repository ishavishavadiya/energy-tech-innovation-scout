ARXIV_BASE_URL = "http://export.arxiv.org/api/query"

SEARCH_QUERY = (
    "energy AND (machine learning OR optimization OR quantum OR battery OR grid)"
)

MAX_RESULTS = 15          # Fetch more, filter later
DAYS_LOOKBACK = 30        # Only recent papers
TOP_K = 5                 # Final innovations

# LLM
OPENAI_API_KEY = ""
MODEL_NAME = "gpt-4o-mini"
