import json
import re
from pathlib import Path

def load_skills_map(path: str | Path = "data/skills_map.json") -> dict:
    """Load your skill-synonym map once at startup."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"skills_map.json not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_text(text: str, skills_map: dict) -> tuple[str, set[str]]:
    """
    Normalize text by replacing all synonym variants with canonical skill terms.
    Returns the normalized text and a set of detected canonical skill names.
    """
    detected = set()
    normalized_text = text.lower()

    for canonical, synonyms in skills_map.items():
        for syn in synonyms:
            # escape regex special chars and match whole words
            pattern = r"\b" + re.escape(syn.lower()) + r"\b"
            if re.search(pattern, normalized_text):
                normalized_text = re.sub(pattern, canonical.lower(), normalized_text)
                detected.add(canonical.lower())
        # also check if canonical term itself exists in text
        if re.search(r"\b" + re.escape(canonical.lower()) + r"\b", normalized_text):
            detected.add(canonical.lower())

    return normalized_text, detected


# # ---- Example usage ----
# if __name__ == "__main__":
#     skills_map = load_skills_map("data/skills_map.json")

#     jd_text = """
#     We need experience with AD, MFA, Terraform, and VMware.
#     Familiarity with Azure AD (Entra ID) and PowerShell scripting preferred.
#     """

#     normalized, found_skills = normalize_text(jd_text, skills_map)

#     print("Normalized Text:\n", normalized)
#     print("\nDetected Skills:\n", sorted(found_skills))
