#!/usr/bin/env python3
"""Convert the Markdown subset used by pr-overview to Atlassian Document Format.

Usage: python3 md-to-adf.py input.md > output.json

Supported: headings (#-######), paragraphs, bullet and ordered lists (nested by
indentation), pipe tables, horizontal rules, fenced code blocks,
<details><summary>Title</summary> ... </details> (rendered as an ADF expand),
and inline **bold**, *italic*, `code` and [links](url).
"""
import json
import re
import sys

INLINE = re.compile(r"(\*\*(.+?)\*\*|`([^`]+)`|\[([^\]]+)\]\(([^)\s]+)\)|(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*))")


def inline(text):
    nodes, pos = [], 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            nodes.append({"type": "text", "text": text[pos:m.start()]})
        if m.group(2) is not None:
            for n in inline(m.group(2)):
                n.setdefault("marks", []).append({"type": "strong"})
                nodes.append(n)
        elif m.group(3) is not None:
            nodes.append({"type": "text", "text": m.group(3), "marks": [{"type": "code"}]})
        elif m.group(4) is not None:
            nodes.append({"type": "text", "text": m.group(4), "marks": [{"type": "link", "attrs": {"href": m.group(5)}}]})
        else:
            for n in inline(m.group(6)):
                n.setdefault("marks", []).append({"type": "em"})
                nodes.append(n)
        pos = m.end()
    if pos < len(text):
        nodes.append({"type": "text", "text": text[pos:]})
    return [n for n in nodes if n.get("text")]


def para(text):
    return {"type": "paragraph", "content": inline(text.strip())}


LIST_ITEM = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def parse_list(lines, i, indent):
    m = LIST_ITEM.match(lines[i])
    ordered = m.group(2)[0].isdigit()
    node = {"type": "orderedList" if ordered else "bulletList", "content": []}
    while i < len(lines):
        m = LIST_ITEM.match(lines[i])
        if not m or len(m.group(1)) < indent:
            break
        if len(m.group(1)) > indent:
            child, i = parse_list(lines, i, len(m.group(1)))
            node["content"][-1]["content"].append(child)
            continue
        text = m.group(3)
        i += 1
        # Continuation lines of the same item.
        while i < len(lines) and lines[i].strip() and not LIST_ITEM.match(lines[i]) and lines[i].startswith(" " * (indent + 2)):
            text += " " + lines[i].strip()
            i += 1
        node["content"].append({"type": "listItem", "content": [para(text)]})
    return node, i


def parse_table(lines, i):
    rows = []
    while i < len(lines) and lines[i].strip().startswith("|"):
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            rows.append(cells)
        i += 1
    table = {"type": "table", "content": []}
    for r, cells in enumerate(rows):
        kind = "tableHeader" if r == 0 else "tableCell"
        table["content"].append({"type": "tableRow", "content": [
            {"type": kind, "content": [para(c) if c else {"type": "paragraph"}]} for c in cells]})
    return table, i


def parse(lines):
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s or s.startswith("<!--"):
            i += 1
        elif s.startswith("<details"):
            title = re.search(r"<summary>(.*?)</summary>", s) or (
                re.search(r"<summary>(.*?)</summary>", lines[i + 1].strip()) if i + 1 < len(lines) else None)
            j = i + 1
            depth = 1
            while j < len(lines):
                if lines[j].strip().startswith("<details"):
                    depth += 1
                if lines[j].strip().startswith("</details>"):
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            body = [l for l in lines[i + 1:j] if "<summary>" not in l]
            out.append({"type": "expand", "attrs": {"title": re.sub(r"<[^>]+>", "", title.group(1)) if title else "Details"},
                        "content": parse(body) or [{"type": "paragraph"}]})
            i = j + 1
        elif s.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            code = "\n".join(lines[i + 1:j])
            out.append({"type": "codeBlock", "attrs": {"language": s[3:].strip() or None},
                        "content": [{"type": "text", "text": code}] if code else []})
            i = j + 1
        elif re.match(r"^#{1,6}\s", s):
            level = len(s) - len(s.lstrip("#"))
            out.append({"type": "heading", "attrs": {"level": level}, "content": inline(s[level:].strip())})
            i += 1
        elif re.fullmatch(r"(-{3,}|\*{3,})", s):
            out.append({"type": "rule"})
            i += 1
        elif s.startswith("|"):
            node, i = parse_table(lines, i)
            out.append(node)
        elif LIST_ITEM.match(line):
            node, i = parse_list(lines, i, len(LIST_ITEM.match(line).group(1)))
            out.append(node)
        else:
            text = [s]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^\s*(#|\||```|<|[-*+]\s|\d+[.)]\s)", lines[i]):
                text.append(lines[i].strip())
                i += 1
            out.append(para(" ".join(text)))
    return out


def main():
    src = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    doc = {"version": 1, "type": "doc", "content": parse(src.splitlines())}
    json.dump(doc, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
