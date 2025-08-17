import re
import difflib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

from bs4 import BeautifulSoup, NavigableString
from mstp_rules import MSTP_RULES

# Optional: LanguageTool (uses public API if available)
try:
    import language_tool_python
    _lt = language_tool_python.LanguageToolPublicAPI('en-US')
except Exception:
    _lt = None


@dataclass
class TextNodeRef:
    node: NavigableString
    path: str  # CSS-like path for display


def _node_path(node) -> str:
    parts = []
    curr = node.parent
    while curr and curr.name:
        name = curr.name
        if curr.get("id"):
            name += f"#{curr.get('id')}"
        if curr.get("class"):
            cls = "." + ".".join(curr.get("class"))
            name += cls
        parts.append(name)
        curr = curr.parent
    return " > ".join(reversed(parts))


def extract_text_nodes(soup: BeautifulSoup) -> List[TextNodeRef]:
    """Get navigable strings that look like user-facing text."""
    nodes = []
    blacklist = {"script", "style"}
    for text in soup.find_all(string=True):
        if not isinstance(text, NavigableString):
            continue
        if text.parent and text.parent.name in blacklist:
            continue
        raw = str(text)
        if not raw or raw.isspace():
            continue
        if len(raw.strip()) < 2:
            continue
        nodes.append(TextNodeRef(node=text, path=_node_path(text)))
    return nodes


def _snippet(s: str, maxlen: int = 120) -> str:
    s = s.replace("\n", " ").strip()
    return s if len(s) <= maxlen else s[:maxlen] + "…"


def apply_mstp_rules_to_nodes(nodes: List[TextNodeRef]) -> List[Dict[str, Any]]:
    suggestions = []
    for ref in nodes:
        original = str(ref.node)
        for rule in MSTP_RULES:
            # Search all matches
            for m in rule["pattern"].finditer(original):
                before = m.group(0)
                # Replace inside the matched span only
                after = rule["pattern"].sub(rule["repl"], before)
                if before == after:
                    continue
                suggestions.append({
                    "type": "MSTP",
                    "rule_id": rule["id"],
                    "description": rule["desc"],
                    "path": ref.path,
                    "before": before,
                    "after": after,
                    "apply": False
                })
    return dedupe_suggestions(suggestions)


def apply_langtool_to_nodes(nodes: List[TextNodeRef]) -> List[Dict[str, Any]]:
    if _lt is None:
        return []

    suggestions = []
    for ref in nodes:
        text = str(ref.node)
        try:
            matches = _lt.check(text)
        except Exception:
            continue

        for m in matches:
            if not m.replacements:
                continue
            before = text[m.offset:m.offset + m.errorLength]
            after = m.replacements[0]
            if before.strip() == after.strip() or not before.strip():
                continue
            suggestions.append({
                "type": "Grammar",
                "rule_id": m.ruleId,
                "description": m.message,
                "path": ref.path,
                "before": before,
                "after": after,
                "apply": False
            })
    return dedupe_suggestions(suggestions)


def dedupe_suggestions(suggs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for s in suggs:
        key = (s["type"], s["rule_id"], s["path"], s["before"], s["after"])
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def apply_selected_changes(soup: BeautifulSoup, df) -> Tuple[str, int]:
    """Apply selected changes to the soup in-place."""
    changes = df[df.get("apply", False) == True].to_dict("records")
    applied = 0

    by_path = {}
    for c in changes:
        by_path.setdefault(c["path"], []).append((c["before"], c["after"]))

    for text in soup.find_all(string=True):
        if not isinstance(text, NavigableString):
            continue
        path = _node_path(text)
        if path not in by_path:
            continue

        original = str(text)
        new_text = original
        for before, after in by_path[path]:
            new_text = new_text.replace(before, after, 1)
        if new_text != original:
            text.replace_with(new_text)
            applied += 1

    return str(soup), applied


def render_diff_html(before_html: str, after_html: str) -> str:
    before_lines = before_html.splitlines(keepends=False)
    after_lines = after_html.splitlines(keepends=False)
    diff = difflib.unified_diff(
        before_lines, after_lines,
        fromfile="original.html", tofile="cleaned.html", lineterm=""
    )
    html = ["<pre style='font-family: ui-monospace, Menlo, Consolas, monospace; font-size:12px; white-space: pre-wrap'>"]
    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            html.append(f"<span style='background:#eaffea'>{line}</span>")
        elif line.startswith("-") and not line.startswith("---"):
            html.append(f"<span style='background:#ffecec'>{line}</span>")
        else:
            html.append(line)
    html.append("</pre>")
    return "\n".join(html)