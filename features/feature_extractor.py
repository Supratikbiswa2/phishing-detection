import re
from urllib.parse import urlparse

SENSITIVE_WORDS = [
    "login", "secure", "account", "update", "verify",
    "bank", "signin", "password", "confirm"
]

def extract_features(url):
    parsed = urlparse(url)

    features = {}

    features["url_length"] = len(url)
    features["valid_url"] = 1 if parsed.scheme and parsed.netloc else 0
    features["at_symbol"] = 1 if "@" in url else 0

    # IMPORTANT: correct name
    features["sensitive_words_count"] = sum(
        word in url.lower() for word in SENSITIVE_WORDS
    )

    features["path_length"] = len(parsed.path)
    features["isHttps"] = 1 if parsed.scheme == "https" else 0
    features["nb_dots"] = url.count(".")
    features["nb_hyphens"] = url.count("-")
    features["nb_and"] = url.count("&")
    features["nb_or"] = url.lower().count("or")
    features["nb_www"] = url.lower().count("www")
    features["nb_com"] = url.lower().count(".com")
    features["nb_underscore"] = url.count("_")

    return features
