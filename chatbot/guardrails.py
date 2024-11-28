# guardrails.py

SENSITIVE_TOPICS = ["sexual", "violence", "politics", "healthcare", "legal"]

def is_sensitive_query(query):
    """
    Check if the query contains sensitive content.
    """
    return any(topic in query.lower() for topic in SENSITIVE_TOPICS)
