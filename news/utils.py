import re


def clean_text(text):
    """Clean text by removing special characters and converting to lower case."""
    text = re.sub(r"\W+", " ", text)
    return text.lower()
