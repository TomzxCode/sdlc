#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyyaml",
#     "markdown",
#     "pymdown-extensions",
#     "structlog",
# ]
# ///
"""Build a GitHub Pages site of SDLC status dashboards.

Discovers every ``.sdlc`` directory in the repository, renders a status
dashboard for it via the bundled ``sdlc-status.py`` module, and writes an
index page linking to each report.

Usage:
    uv run scripts/build-sdlc-site.py [--root ROOT] [--out OUT]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import importlib.util
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import structlog

EXCLUDED_SEGMENTS = {".git", "node_modules", ".venv", "site", "scripts", "__pycache__"}
RENDERER_PATH = Path(__file__).resolve().parent / "sdlc-status.py"

# Import the vendored renderer as a module so the whole site builds in one
# uv process instead of spawning a subprocess per .sdlc directory.
_spec = importlib.util.spec_from_file_location("sdlc_status", RENDERER_PATH)
renderer = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(renderer)


@dataclass
class Project:
    sdlc_dir: Path
    project_rel: str  # path of the .sdlc parent, relative to repo root
    out_path: Path  # site/<project_rel>/index.html
    url: str  # link relative to site root
    title: str
    org: str
    name: str
    description: str
    feature_count: int


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    while cur.parent != cur:
        if (cur / ".git").exists():
            return cur
        cur = cur.parent
    return start.resolve()


def discover_sdlc_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    for path in root.rglob(".sdlc"):
        if not path.is_dir():
            continue
        if any(part in EXCLUDED_SEGMENTS for part in path.parts):
            continue
        found.append(path)
    found.sort()
    return found


def count_features(sdlc_dir: Path) -> int:
    features = sdlc_dir / "features"
    if not features.is_dir():
        return 0
    return sum(1 for p in features.iterdir() if p.is_dir() and p.name != "templates")


def extract_description(sdlc_dir: Path) -> str:
    overview = sdlc_dir / "context" / "project-overview.md"
    if not overview.exists():
        return ""
    text = overview.read_text(encoding="utf-8")
    m = re.search(r"^##\s*Purpose\s*$(.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    section = m.group(1).strip() if m else ""
    section = re.sub(r"^#.*$", "", section, flags=re.MULTILINE).strip()
    if not section:
        return ""
    first = re.split(r"(?<=[.!?])\s+", section)[0]
    return re.sub(r"\s+", " ", first).strip()


def render_dashboard(sdlc_dir: Path, out_path: Path) -> bool:
    page = renderer.render_dashboard_html(sdlc_dir)
    if page is None:
        sys.stderr.write(f"[warn] no features in {sdlc_dir}\n")
        return False
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")
    return True


INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SDLC Status Dashboards</title>
<style>
  :root {{
    --bg: #0f1117; --surface: #1a1d27; --surface-alt: #222636;
    --border: #2e3347; --text: #e1e4ed; --text-muted: #8b8fa3;
    --accent: #6c8cff; --green: #4ade80; --blue: #60a5fa;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.6; padding: 2rem;
    max-width: 1100px; margin: 0 auto;
  }}
  header {{ margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border); }}
  header h1 {{ color: var(--accent); font-size: 1.4rem; font-weight: 600; }}
  header p {{ color: var(--text-muted); font-size: 0.85rem; margin-top: 0.25rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.25rem; }}
  .card {{
    background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
    padding: 1.25rem 1.4rem; text-decoration: none; color: inherit; display: flex;
    flex-direction: column; gap: 0.5rem; transition: border-color 0.15s, transform 0.15s;
  }}
  .card:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
  .card .org {{ font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; }}
  .card .name {{ font-size: 1.05rem; font-weight: 700; color: var(--text); }}
  .card .desc {{ font-size: 0.82rem; color: var(--text-muted); flex: 1; }}
  .meta {{ display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 0.25rem; }}
  .pill {{
    font-size: 0.7rem; font-weight: 600; padding: 0.15rem 0.5rem; border-radius: 999px;
    background: var(--surface-alt); color: var(--text-muted);
  }}
  .pill.features {{ background: rgba(96,165,250,0.15); color: var(--blue); }}
  .pill.link {{ background: rgba(108,140,255,0.15); color: var(--accent); }}
  .empty {{ color: var(--text-muted); font-style: italic; }}
  footer {{ margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid var(--border); font-size: 0.72rem; color: var(--text-muted); }}
  footer a {{ color: var(--accent); text-decoration: none; }}
</style>
</head>
<body>
<header>
  <h1>SDLC Status Dashboards</h1>
  <p>{project_count} projects &middot; generated {generated}</p>
</header>
{body}
<footer>Published automatically from the <a href="{repo_url}">{repo_name}</a> repository.</footer>
</body>
</html>
"""


def card_html(project: Project) -> str:
    desc = project.description or "No project overview available."
    pills = (
        f'<span class="pill features">{project.feature_count} features</span>'
        if project.feature_count
        else '<span class="pill">no features</span>'
    )
    pills += f'<span class="pill link">view dashboard &rarr;</span>'
    return (
        f'<a class="card" href="{html.escape(project.url)}">'
        f'<span class="org">{html.escape(project.org)}</span>'
        f'<span class="name">{html.escape(project.name)}</span>'
        f'<span class="desc">{html.escape(desc)}</span>'
        f'<span class="meta">{pills}</span>'
        f"</a>"
    )


def build_index(projects: list[Project], out: Path, root: Path) -> None:
    if not projects:
        body = '<p class="empty">No SDLC directories found.</p>'
    else:
        body = '<div class="grid">\n' + "\n".join(card_html(p) for p in projects) + "\n</div>"
    generated = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d %H:%M UTC")
    repo_url = "https://github.com/TomzxCode/sdlc"
    repo_name = "TomzxCode/sdlc"
    page = INDEX_TEMPLATE.format(
        project_count=len(projects),
        generated=html.escape(generated),
        body=body,
        repo_url=repo_url,
        repo_name=repo_name,
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")


def main() -> int:
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(format="%(message)s", level=logging.WARNING, stream=sys.stderr)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=None, help="Repository root (default: auto-detect)")
    parser.add_argument("--out", default="site", help="Output directory (default: site)")
    args = parser.parse_args()

    root = find_repo_root(Path(args.root)) if args.root else find_repo_root(Path(__file__).parent)
    out_dir = (root / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    sdlc_dirs = discover_sdlc_dirs(root)
    if not sdlc_dirs:
        sys.stderr.write(f"[warn] no .sdlc directories found under {root}\n")

    projects: list[Project] = []
    for sdlc_dir in sdlc_dirs:
        project_rel = str(sdlc_dir.parent.relative_to(root))
        if not project_rel or project_rel == ".":
            project_rel = "repository"
        out_path = out_dir / project_rel / "index.html"
        url = f"{project_rel}/index.html"
        parts = project_rel.split("/")
        org = parts[0] if len(parts) >= 1 else ""
        name = parts[-1]
        title = " / ".join(parts)

        if not (sdlc_dir / "features").is_dir():
            sys.stderr.write(f"[skip] {project_rel}: no features directory\n")
            continue
        if not render_dashboard(sdlc_dir, out_path):
            continue

        projects.append(
            Project(
                sdlc_dir=sdlc_dir,
                project_rel=project_rel,
                out_path=out_path,
                url=url,
                title=title,
                org=org,
                name=name,
                description=extract_description(sdlc_dir),
                feature_count=count_features(sdlc_dir),
            )
        )
        try:
            shown = str(out_path.relative_to(root))
        except ValueError:
            shown = str(out_path)
        sys.stderr.write(f"[ok] rendered {project_rel} -> {shown}\n")

    index_path = out_dir / "index.html"
    build_index(projects, index_path, root)
    try:
        shown = str(index_path.relative_to(root))
    except ValueError:
        shown = str(index_path)
    sys.stderr.write(f"[done] index -> {shown} ({len(projects)} projects)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
