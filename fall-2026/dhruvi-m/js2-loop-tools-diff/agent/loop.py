"""The bounded agent loop (GATE.md: exits, budgets, repeat rule, error policy)."""
import json
import socket
import time
import urllib.error
import urllib.request

from boards import board_url, parse_jobs
from policy import PolicyError, check_request

REQUEST_TIMEOUT = 15  # seconds per HTTP request


def http_get(url: str, timeout: float):
    """Real fetch. Returns (status, body_bytes). Raises TimeoutError on timeout."""
    check_request(url, "GET")  # policy is checked again right before any network call
    req = urllib.request.Request(url, headers={"User-Agent": "js2-student-agent (INFO7375)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except (socket.timeout, TimeoutError):
        raise TimeoutError(f"timeout after {timeout}s")
    except urllib.error.URLError as e:
        if isinstance(e.reason, (socket.timeout, TimeoutError)):
            raise TimeoutError(f"timeout after {timeout}s")
        raise


def run_loop(boards, budget, seen, fetch=http_get, clock=time.monotonic, empty_rule=True):
    """Visit boards under the budget. Never invents a value for a failed board.

    seen: {board_name: [job ids from the last approved run]} (may be empty)
    empty_rule: GATE.md's empty-board rule. False = the WRONG version, used only in the demo.
    """
    start = clock()
    trace, results, done_actions = [], {}, set()
    requests = 0
    budget_hit = None

    def log(board, event, **detail):
        trace.append({"t": round(clock() - start, 3), "board": board, "event": event, **detail})

    log(None, "start", budget=budget, boards=[b["name"] for b in boards])
    for b in boards:
        name = b["name"]
        if len([r for r in results.values()]) >= budget["max_boards"]:
            budget_hit = "max_boards"
            break
        if clock() - start >= budget["max_seconds"]:
            budget_hit = "max_seconds"
            break
        url = board_url(b["ats"], b["slug"])
        try:
            check_request(url, "GET")
        except PolicyError as e:
            log(name, "policy-refused", reason=str(e))
            return _report("error", trace, results, requests, clock() - start, boards, error=str(e))
        action = ("GET", url)
        if action in done_actions:
            log(name, "repeat-blocked", url=url)
            results[name] = {"status": "repeat-blocked", "url": url}
            continue
        done_actions.add(action)

        tries, outcome = 0, None
        while True:
            if requests >= budget["max_requests"]:
                budget_hit = "max_requests"
                break
            time_left = budget["max_seconds"] - (clock() - start)
            if time_left < 1:
                budget_hit = "max_seconds"
                break
            requests += 1
            tries += 1
            log(name, "request", url=url, attempt=tries, requests_used=requests)
            try:
                status, body = fetch(url, timeout=min(REQUEST_TIMEOUT, time_left))
            except TimeoutError as e:
                status, body, kind = None, b"", "timeout"
            else:
                kind = ("ok" if status == 200 else "not-found" if status == 404
                        else "server-error" if status >= 500 else "bad-response")
            log(name, "response", http_status=status, kind=kind, bytes=len(body))
            if kind in ("timeout", "server-error") and tries == 1:
                log(name, "retry", reason=kind)   # one retry only, for temporary errors
                continue
            outcome = (kind, status, body)
            break
        if outcome is None:  # budget ran out before or during this board
            if tries > 0:
                results[name] = {"status": "not-finished", "reason": budget_hit, "url": url}
            break

        kind, status, body = outcome
        if kind != "ok":
            results[name] = {"status": "failed", "reason": kind, "http_status": status,
                             "url": url, "attempts": tries, "raw": body or None}
            log(name, "board-failed", reason=kind)
            continue
        try:
            jobs = parse_jobs(b["ats"], json.loads(body))
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            results[name] = {"status": "failed", "reason": "bad-response", "detail": str(e),
                             "url": url, "attempts": tries, "raw": body}
            log(name, "board-failed", reason="bad-response", detail=str(e))
            continue
        ids = [j["id"] for j in jobs]
        prev = seen.get(name)
        if empty_rule and len(ids) == 0 and prev:
            results[name] = {"status": "suspicious-empty", "count": 0, "previous_count": len(prev),
                             "url": url, "raw": body}
            log(name, "board-suspicious", reason="0 jobs but had jobs last run", previous=len(prev))
            continue
        new_ids = [] if prev is None else sorted(set(ids) - set(prev))
        results[name] = {"status": "ok", "count": len(ids), "baseline": prev is None,
                         "new_ids": new_ids, "ids": ids, "jobs": jobs, "url": url, "raw": body}
        log(name, "board-ok", count=len(ids), new=len(new_ids), baseline=prev is None)

    elapsed = clock() - start
    attempted = set(results)
    if budget_hit or attempted != {b["name"] for b in boards}:
        status = "budget-exhausted"
    elif all(r["status"] == "ok" for r in results.values()):
        status = "finished"
    else:
        status = "incomplete"
    return _report(status, trace, results, requests, elapsed, boards, budget_hit=budget_hit)


def _report(status, trace, results, requests, elapsed, boards, error=None, budget_hit=None):
    trace.append({"t": round(elapsed, 3), "board": None, "event": "exit", "status": status})
    return {
        "status": status,
        "error": error,
        "budget_hit": budget_hit,
        "requests_used": requests,
        "seconds": round(elapsed, 3),
        "never_attempted": [b["name"] for b in boards if b["name"] not in results],
        "boards": results,
        "trace": trace,
    }
