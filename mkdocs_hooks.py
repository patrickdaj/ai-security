"""MkDocs hook: resolve single-sourced README links sensibly in the site.

The module READMEs are pulled into the docs site via include-markdown. Their
links are repo-relative (correct on GitHub) but have nowhere to go in the site.
This hook rewrites them per their target:

  * Links to a page that EXISTS in the docs site (another module README, the
    showcase, conventions, labs, the home README) -> the in-site doc page, so
    cross-module navigation stays in the site and matches the nav.
  * Links to repo files with no doc page (code in project/ reference/ aug/,
    workflows, terraform) -> absolute GitHub URL (blob for files, tree for dirs).
  * Genuine doc-to-doc links and absolute URLs -> left untouched.

Runs as an on_page_markdown hook (after include-markdown, so the included
content's links are already present and rewritten relative to the page).
"""

from __future__ import annotations

import os
import posixpath
import re

BRANCH = "main"
_LINK = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)(\))")
_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
_DOCS = os.path.join(_REPO_ROOT, "docs")


def _doc_target(repo_path: str) -> str | None:
    """Map a repo path to its docs-source .md file, or None if it has no page."""
    p = repo_path[:-len("/README.md")] if repo_path.endswith("/README.md") else repo_path
    fixed = {
        "README.md": "index.md",
        "SHOWCASE.md": "showcase.md",
        "modules/CONVENTIONS.md": "conventions.md",
        "labs": "labs.md",
    }
    if repo_path in fixed:
        return fixed[repo_path]
    if p in fixed:
        return fixed[p]
    m = re.fullmatch(r"modules/([^/]+)", p)
    if m and os.path.isfile(os.path.join(_DOCS, "modules", f"{m.group(1)}.md")):
        return f"modules/{m.group(1)}.md"
    return None


def on_page_markdown(markdown, page, config, **kwargs):
    repo_url = (config.get("repo_url") or "").rstrip("/")
    src_dir = posixpath.dirname(page.file.src_path)  # docs-relative dir of this page

    def rewrite(match: re.Match) -> str:
        prefix, url, close = match.groups()
        if url.startswith(("http://", "https://", "//", "#", "mailto:")):
            return match.group(0)

        path, _, anchor = url.partition("#")
        if not path:
            return match.group(0)
        suffix = f"#{anchor}" if anchor else ""

        resolved = posixpath.normpath(posixpath.join(src_dir, path))
        if not resolved.startswith(".."):
            return match.group(0)  # stays within docs/ -> a real doc page link

        repo_path = re.sub(r"^(?:\.\./)+", "", resolved)

        # In-site doc page? Point at its .md relative to this page; MkDocs resolves
        # it to the correct URL (works locally and on the deployed base path).
        target = _doc_target(repo_path)
        if target is not None:
            rel = posixpath.relpath(target, src_dir or ".")
            return f"{prefix}{rel}{suffix}{close}"

        # Otherwise it's a repo file with no doc page -> canonical GitHub view.
        if not repo_url:
            return match.group(0)
        kind = "tree" if os.path.isdir(os.path.join(_REPO_ROOT, repo_path)) else "blob"
        return f"{prefix}{repo_url}/{kind}/{BRANCH}/{repo_path}{suffix}{close}"

    return _LINK.sub(rewrite, markdown)
