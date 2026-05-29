DEFAULT_RULES: dict[str, str] = {
    "starbucks": "dining",
    "whole foods": "groceries",
    "shell": "transportation",
}


def categorize(description: str) -> str:
    normalized = description.lower()
    for key, category in DEFAULT_RULES.items():
        if key in normalized:
            return category
    return "uncategorized"
