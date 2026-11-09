"""URLs and parsers for the three applicant-tracking systems."""


def board_url(ats: str, slug: str) -> str:
    if ats == "greenhouse":
        return f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    if ats == "lever":
        return f"https://api.lever.co/v0/postings/{slug}?mode=json"
    if ats == "ashby":
        return f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    raise ValueError(f"unknown ats {ats!r}")


def parse_jobs(ats: str, data) -> list:
    """Return [{'id','title','location'}]. Raises ValueError on an unexpected shape."""
    if ats == "greenhouse":
        if not isinstance(data, dict) or not isinstance(data.get("jobs"), list):
            raise ValueError("greenhouse: expected {'jobs': [...]}")
        return [{"id": str(j["id"]), "title": j.get("title", ""),
                 "location": (j.get("location") or {}).get("name", "")} for j in data["jobs"]]
    if ats == "lever":
        if not isinstance(data, list):
            raise ValueError("lever: expected a list")
        return [{"id": str(j["id"]), "title": j.get("text", ""),
                 "location": (j.get("categories") or {}).get("location", "")} for j in data]
    if ats == "ashby":
        if not isinstance(data, dict) or not isinstance(data.get("jobs"), list):
            raise ValueError("ashby: expected {'jobs': [...]}")
        return [{"id": str(j["id"]), "title": j.get("title", ""),
                 "location": j.get("location", "")} for j in data["jobs"]]
    raise ValueError(f"unknown ats {ats!r}")
