# jd_parser.py
# Windows-friendly, no external downloads needed.
# Uses normalize_skills.py and data/skills_map.json

import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Set

# ---- Local imports
from normalize_skills import load_skills_map, normalize_text


# ---------------------------
# Heuristics / configuration
# ---------------------------

# Lightweight stopwords for keyword extraction (no NLTK needed)
_STOPWORDS = {
    "the", "and", "or", "to", "of", "in", "on", "for", "with", "a", "an", "by", "as",
    "is", "are", "be", "will", "this", "that", "we", "you", "our", "your", "at", "from",
    "across", "including", "such", "etc", "about", "into", "within", "over", "under",
    "more", "most", "least", "ability", "experience", "years", "year", "plus", "etc.",
    "responsibilities", "requirements", "preferred", "must", "nice", "have", "skills",
    "role", "job", "description", "position", "candidate", "ideal", "work", "working"
}

# Common section headers we’ll try to parse from JD text
_SECTION_HEADERS = {
    "responsibilities": r"(responsibilities|what you'll do|what you will do|duties|role and responsibilities)",
    "must_haves": r"(requirements|must[-\s]*have|qualifications|required)",
    "nice_to_haves": r"(nice[-\s]*to[-\s]*have|preferred|bonus|good to have)"
}

# Guess seniority from common cues
_SENIORITY_MAP = [
    (r"\b(principal|lead|staff)\b", "Principal/Lead"),
    (r"\b(senior|sr\.)\b", "Senior"),
    (r"\b(mid[-\s]*level|intermediate)\b", "Mid"),
    (r"\b(junior|jr\.)\b", "Junior"),
]


# ---------------------------
# Public API
# ---------------------------

def parse_jd(
    jd_text: str,
    skills_map_path: str | Path = "data/skills_map.json",
    top_kw: int = 30,
) -> Dict:
    """
    Parse and normalize a Job Description into a structured dict.

    Returns:
        {
          "title": str,
          "company": str,
          "location": str,
          "seniority": str,
          "must_haves": [str],
          "nice_to_haves": [str],
          "responsibilities": [str],
          "keywords": [str],                # top N keywords from normalized JD text
          "normalized_skills": [str],       # canonical skills detected via skills_map
          "normalized_text": str            # fully normalized JD text (for downstream scoring)
        }
    """
    jd_text = jd_text.strip()
    skills_map = _safe_load_skills_map(skills_map_path)

    # 1) Extract simple fields first (raw text)
    title = _extract_title(jd_text)
    company = _extract_company(jd_text)
    location = _extract_location(jd_text)
    seniority = _guess_seniority(jd_text)

    # 2) Extract sections (raw)
    must_haves_raw = _extract_bullets(jd_text, _SECTION_HEADERS["must_haves"])
    nice_to_haves_raw = _extract_bullets(jd_text, _SECTION_HEADERS["nice_to_haves"])
    responsibilities_raw = _extract_bullets(jd_text, _SECTION_HEADERS["responsibilities"])

    # 3) Normalize the full JD text for consistent keyword/skill detection
    normalized_text, detected_skills = normalize_text(jd_text, skills_map)

    # 4) Normalize list sections too (helps downstream matching)
    must_haves = _normalize_lines(must_haves_raw, skills_map)
    nice_to_haves = _normalize_lines(nice_to_haves_raw, skills_map)
    responsibilities = _normalize_lines(responsibilities_raw, skills_map)

    # 5) Extract top keywords from normalized text
    keywords = _top_keywords(normalized_text, n=top_kw)

    return {
        "title": title,
        "company": company,
        "location": location,
        "seniority": seniority,
        "must_haves": must_haves[:15],
        "nice_to_haves": nice_to_haves[:15],
        "responsibilities": responsibilities[:30],
        "keywords": keywords,
        "normalized_skills": sorted(detected_skills),
        "normalized_text": normalized_text
    }


# ---------------------------
# Helpers
# ---------------------------

def _safe_load_skills_map(path: str | Path) -> Dict:
    try:
        return load_skills_map(path)
    except FileNotFoundError:
        # Fallback to empty map to avoid breaking UI
        return {}


def _extract_title(text: str) -> str:
    # Try a labeled line
    m = re.search(r"(?im)^\s*title\s*[:\-]\s*(.+)$", text)
    if m: 
        return _clean_line(m.group(1))

    # Try first prominent heading (heuristic)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines:
        first = lines[0]
        # avoid company names or generic phrases
        if len(first.split()) <= 12 and not re.search(r"(company|about us|who we are)", first, re.I):
            return _clean_line(first)
    return ""


def _extract_company(text: str) -> str:
    m = re.search(r"(?im)^\s*company\s*[:\-]\s*(.+)$", text)
    if m:
        return _clean_line(m.group(1))

    # Look for "About <Company>" style
    m = re.search(r"(?im)about\s+([A-Z][A-Za-z0-9&\-\s]{2,40})", text)
    if m:
        return _clean_line(m.group(1))
    return ""


def _extract_location(text: str) -> str:
    # Label-based
    m = re.search(r"(?im)^\s*location\s*[:\-]\s*(.+)$", text)
    if m:
        return _clean_line(m.group(1))

    # Common city/country cues
    m = re.search(r"(?i)\b(singapore|london|new york|sydney|remote|hybrid|onsite)\b", text)
    return m.group(0).title() if m else ""


def _guess_seniority(text: str) -> str:
    for pat, label in _SENIORITY_MAP:
        if re.search(pat, text, re.I):
            return label
    return ""


def _extract_bullets(text: str, header_regex: str) -> List[str]:
    """
    Finds a section by header and pulls the bullet list beneath it.
    Accepts bullets like -, *, •.
    Stops at a blank line or next header-like chunk.
    """
    # Find header line
    header = re.search(header_regex, text, re.I)
    if not header:
        return []

    # Slice from header start
    start = header.start()
    section = text[start:]

    # Find first bullet list after header
    m = re.search(r"(?s)(?:\r?\n|\r)\s*([\-*\u2022].+?)(?:\n\s*\n|$)", section)
    if not m:
        return []

    bullets_block = m.group(1)
    lines = [l.strip() for l in bullets_block.splitlines()]

    # Keep only bullet lines, strip markers
    out = []
    for line in lines:
        if re.match(r"^\s*[\-*\u2022]\s+", line):
            cleaned = re.sub(r"^\s*[\-*\u2022]\s+", "", line).strip()
            if cleaned:
                out.append(_clean_line(cleaned))
    return out


def _normalize_lines(lines: List[str], skills_map: Dict) -> List[str]:
    out = []
    for l in lines:
        normalized, _skills = normalize_text(l, skills_map)
        # restore capitalization lightly (sentence case)
        out.append(_sentence_case(normalized))
    return out


def _sentence_case(s: str) -> str:
    s = s.strip()
    if not s:
        return s
    return s[0].upper() + s[1:]


def _clean_line(s: str) -> str:
    s = s.strip()
    # Remove trailing punctuation that often appears in headings
    s = re.sub(r"[;,:.\-–]+$", "", s).strip()
    return s


def _top_keywords(text: str, n: int = 30) -> List[str]:
    # Tokenize words (letters, digits, +, #, . allowed)
    words = re.findall(r"[A-Za-z0-9\+\#\.]{3,}", text.lower())
    freq = {}
    for w in words:
        if w in _STOPWORDS:
            continue
        freq[w] = freq.get(w, 0) + 1

    # return top-N by frequency
    return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:n]]


# ---------------------------
# CLI (optional quick test)
# ---------------------------

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python jd_parser.py <jd_text_file> [skills_map.json]")
        sys.exit(1)

    jd_file = Path(sys.argv[1])
    sm_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("data/skills_map.json")

    jd_text = jd_file.read_text(encoding="utf-8")
    result = parse_jd(jd_text, sm_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
