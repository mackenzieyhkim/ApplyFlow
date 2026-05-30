import re


def clean_text(text: str) -> str:
    """
    Removes extra spaces, weird line breaks, and duplicate whitespace.
    """

    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = text.strip()

    return text

