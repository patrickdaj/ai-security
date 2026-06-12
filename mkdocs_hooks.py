"""MkDocs hook: make single-sourced README links work in the site.

The module READMEs are pulled into the docs site via include-markdown. Their
links point at repo paths (code files, other module dirs) that aren't doc
pages, so in the rendered site they 404. This hook rewrites any link that
resolves OUTSIDE the docs tree to an absolute GitHub URL (blob for files, tree
for dirs), and leaves genuine doc-to-doc links untouched.

Runs as an on_page_markdown hook (after the include-markdown plugin, so the
included content's links are already present and rewritten relative to the page).
"""

from __future__ import annotations

import os
import posixpath
import re

BRANCH = "main"

# [text](url) and ![alt](url) — capture the url so we can rewrite just that.
_LINK = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)(\))")

_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def on_page_markdown(markdown, page, config, files, **kwargs):
    repo_url = (config.get("repo_url") or "").rstrip("/")
    if not repo_url:
        return markdown

    src_dir = posixpath.dirname(page.file.src_path)  # docs-relative dir of this page

    def rewrite(match: re.Match) -> str:
        prefix, url, close = match.groups()
        if url.startswith(("http://", "https://", "//", "#", "mailto:")):
            return match.group(0)

        path, _, anchor = url.partition("#")
        if not path:
            return match.group(0)

        resolved = posixpath.normpath(posixpath.join(src_dir, path))
        if not resolved.startswith(".."):
            return match.group(0)  # stays within docs/ -> a real doc page link

        repo_path = re.sub(r"^(?:\.\./)+", "", resolved)
        kind = "tree" if os.path.isdir(os.path.join(_REPO_ROOT, repo_path)) else "blob"
        suffix = f"#{anchor}" if anchor else ""
        return f"{prefix}{repo_url}/{kind}/{BRANCH}/{repo_path}{suffix}{close}"

    return _LINK.sub(rewrite, markdown)
