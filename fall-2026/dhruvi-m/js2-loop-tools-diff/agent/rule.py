"""The relevance RULE (the record): deterministic, recomputable by hand.

JS1 rule (CONTRACT.md) had 3 checks: title, 3+ skills, US location.
JS2 adds check 4, years of experience, because the JS1 rule wrongly marked
posting 8026689 (5-10 years) as relevant. It also adds "United States" to the
US list (JS1 missed posting 7964568).
"""
import html
import re

US_MARKERS = {
    "united states", "usa", "us", "u.s.", "us-remote", "us remote", "remote", "n/a",
    "north america", "us/canada", "remote-canada",
    "nyc", "new york", "new york city", "ny", "sf", "san francisco", "south san francisco",
    "seattle", "sea", "chicago", "chi", "atlanta", "georgia", "boston", "washington dc",
}
YEARS_RE = re.compile(r"(\d{1,2})\s*\+?\s*(?:(?:-|–|to)\s*\d{1,2}\s*\+?\s*)?years?", re.I)


def clean(text: str) -> str:
    """HTML -> plain text (Greenhouse content is HTML-escaped twice)."""
    t = html.unescape(html.unescape(text or ""))
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def location_is_us(location: str) -> bool:
    loc = (location or "").lower().strip()
    if not loc:
        return False
    if loc == "canada":
        return False
    parts = [p.strip() for p in re.split(r"[,;/|()]| or ", loc) if p.strip()]
    return any(p in US_MARKERS or p.startswith("us-") or p.startswith("remote from the us")
               for p in parts) or loc in US_MARKERS


def min_years(text: str):
    """Lowest number of years the posting asks for, or None if none is stated."""
    nums = [int(m.group(1)) for m in YEARS_RE.finditer(text or "")]
    nums = [n for n in nums if 0 < n <= 30]
    return min(nums) if nums else None


def evaluate(job: dict, persona: dict, years_check: bool = True) -> dict:
    """job: {'title','location','text'}. years_check=False is the JS1 (wrong) version."""
    title = job.get("title", "")
    text = clean(job.get("text", ""))
    title_ok = any(t.lower() in title.lower() for t in persona["target_titles"])
    skills_found = [s for s in persona["skills"]
                    if re.search(r"(?<!\w)" + re.escape(s) + r"(?!\w)", text, re.I)]
    skills_ok = len(skills_found) >= 3
    loc_ok = location_is_us(job.get("location", ""))
    yrs = min_years(text)
    years_ok = (yrs is None or yrs <= persona["years_experience"]) if years_check else True
    return {
        "relevant": title_ok and skills_ok and loc_ok and years_ok,
        "title_ok": title_ok, "skills_found": skills_found, "skills_ok": skills_ok,
        "location_ok": loc_ok, "min_years": yrs, "years_ok": years_ok,
    }
