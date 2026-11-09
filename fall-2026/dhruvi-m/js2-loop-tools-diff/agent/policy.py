"""Permission policy from GATE.md, enforced in code (not in a prompt)."""
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
CONFIG = ROOT / "config"
STATE_FILE = ROOT / "state" / "seen_ids.json"
ALLOWED_HOSTS = {"boards-api.greenhouse.io", "api.lever.co", "api.ashbyhq.com"}
ALLOWED_METHODS = {"GET"}


class PolicyError(Exception):
    """An action the permission policy refuses."""


class ApprovalRequired(PolicyError):
    """An action that needs Dhruvi's explicit approval (--approve)."""


def check_request(url: str, method: str = "GET") -> None:
    if method.upper() not in ALLOWED_METHODS:
        raise PolicyError(f"method {method} refused: GET only")
    p = urlparse(url)
    if p.scheme != "https":
        raise PolicyError(f"scheme {p.scheme!r} refused: https only")
    if p.username or p.password:
        raise PolicyError("credentials in URL refused")
    if p.hostname not in ALLOWED_HOSTS:          # exact match, not 'contains'
        raise PolicyError(f"host {p.hostname!r} is not on the allow-list")


def _inside(path, root: Path) -> bool:
    real = Path(path).resolve()                    # resolves '..' and symlinks
    root = root.resolve()
    return real == root or real.is_relative_to(root)


def check_write(path) -> Path:
    if not _inside(path, OUT):
        raise PolicyError(f"write refused: {path} is outside out/")
    return Path(path).resolve()


def check_read(path) -> Path:
    if not (_inside(path, OUT) or _inside(path, CONFIG)):
        raise PolicyError(f"read refused: {path} is outside out/ and config/")
    return Path(path).resolve()


def check_state_write(path, approved: bool) -> Path:
    if Path(path).resolve() != STATE_FILE.resolve():
        raise PolicyError(f"state write refused: only {STATE_FILE.name} may be written")
    if not approved:
        raise ApprovalRequired("overwriting the state file needs --approve")
    return STATE_FILE.resolve()
