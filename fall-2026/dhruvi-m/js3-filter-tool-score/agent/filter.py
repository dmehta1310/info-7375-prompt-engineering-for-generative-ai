"""FILTER.md as code. Verdicts: relevant / rejected / cannot_tell, always with reasons.

The wrong_* flags turn on the WRONG versions listed in FILTER.md, so tests can show
that each one gives a different (wrong) answer.
"""
import re

US_STATES = {
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware",
    "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky",
    "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
    "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey", "new mexico",
    "new york", "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania",
    "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah", "vermont",
    "virginia", "washington", "west virginia", "wisconsin", "wyoming", "district of columbia",
}
US_ABBR = {
    "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga", "hi", "id", "il", "in", "ia", "ks",
    "ky", "la", "me", "md", "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny",
    "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv",
    "wi", "wy", "dc", "d.c.",
}
US_CITIES = {
    "san francisco", "south san francisco", "sf", "nyc", "new york city", "seattle", "sea", "chicago",
    "chi", "atlanta", "boston", "washington dc", "washington d.c.", "denver", "palo alto",
    "los angeles", "austin", "dallas", "miami", "philadelphia", "san jose", "mountain view",
    "sunnyvale", "redwood city", "menlo park", "oakland", "portland", "salt lake city", "pittsburgh",
    "detroit", "minneapolis", "phoenix", "san diego", "houston", "nashville", "raleigh", "arlington",
    "reston", "mclean", "bethesda", "columbus", "indianapolis", "honolulu", "tampa", "boulder",
}
COUNTRY_US = re.compile(r"\b(united states|usa|u\.s\.a?\.?|us)\b", re.I)
REMOTE_ONLY = {"remote", "anywhere", "hybrid", "flexible", "worldwide", "global"}


def _parts(location):
    return [p.strip() for p in re.split(r"[,;/|()]| - | or | and ", location.lower()) if p.strip()]


def location_is_us(location, wrong_contains_us=False, wrong_missing_is_us=False):
    """True = US, False = not US, None = I cannot tell (missing, or 'Remote' with no country)."""
    loc = (location or "").strip()
    if not loc:
        return True if wrong_missing_is_us else None
    if wrong_contains_us:
        return "us" in loc.lower()
    parts = _parts(loc)
    for p in parts:
        if (p in US_STATES or p in US_ABBR or p in US_CITIES or COUNTRY_US.search(p)
                or p.startswith("us-") or p.endswith("-us")):
            return True
    if all(p in REMOTE_ONLY for p in parts):
        return None
    return False


def title_matches(title, words, wrong_case_sensitive=False, wrong_substring=False):
    flags = 0 if wrong_case_sensitive else re.I
    for w in words:
        pat = re.escape(w) if wrong_substring else r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])"
        if re.search(pat, title or "", flags):
            return w
    return None


def min_years(text):
    nums = [int(m.group(1)) for m in
            re.finditer(r"(\d{1,2})\s*\+?\s*(?:(?:-|–|to)\s*\d{1,2}\s*\+?\s*)?years?", text or "", re.I)]
    nums = [n for n in nums if 0 < n <= 30]
    return min(nums) if nums else None


def skills_found(text, skills):
    return [s for s in skills if re.search(r"(?<!\w)" + re.escape(s) + r"(?!\w)", text or "", re.I)]


def judge(p, cfg, **wrong):
    """One posting -> {'verdict', 'reasons', 'checks'}. Follows FILTER.md order."""
    checks = {}
    miss = [m for m in p.get("missing", []) if m in ("location", "text")]
    if miss and not wrong.get("wrong_missing_is_us"):
        return {"verdict": "cannot_tell", "reasons": [f"missing {', '.join(miss)}"], "checks": checks}
    hit = title_matches(p["title"], cfg["title_words"],
                        wrong.get("wrong_case_sensitive", False), wrong.get("wrong_substring", False))
    checks["title_word"] = hit
    if not hit:
        return {"verdict": "rejected", "reasons": ["title has none of the target words"], "checks": checks}
    us = location_is_us(p["location"], wrong.get("wrong_contains_us", False), wrong.get("wrong_missing_is_us", False))
    checks["us_location"] = us
    if us is None:
        return {"verdict": "cannot_tell", "reasons": [f"location '{p['location']}' does not say the country"], "checks": checks}
    if not us:
        return {"verdict": "rejected", "reasons": [f"location '{p['location']}' is not in the US"], "checks": checks}
    if cfg.get("max_years") is not None:
        y = min_years(p["text"])
        checks["min_years"] = y
        if y is None:
            return {"verdict": "cannot_tell", "reasons": ["no number of years stated"], "checks": checks}
        if y > cfg["max_years"]:
            return {"verdict": "rejected", "reasons": [f"asks for {y}+ years (> {cfg['max_years']})"], "checks": checks}
    if cfg.get("min_skills") is not None:
        found = skills_found(p["text"], cfg["skills"])
        checks["skills_found"] = found
        if len(found) < cfg["min_skills"]:
            return {"verdict": "rejected", "reasons": [f"only {len(found)} of Priya's skills"], "checks": checks}
    return {"verdict": "relevant", "reasons": [f"title has '{hit}'", "US location"], "checks": checks}
