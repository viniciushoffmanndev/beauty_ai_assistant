def normalize_text(text: str, max_length: int) -> str:
    text = " ".join(text.split())
    return text[:max_length]
