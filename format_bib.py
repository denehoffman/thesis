#!/usr/bin/env python3
import re
from pathlib import Path


def main():
    f = Path('references.bib')
    text = f.read_text()
    text = text.replace(r'\{', '{').replace(r'\}', '}')
    text = wrap_bibtex_titles_braced(text)
    text = remove_braced_abstract_and_url(text)
    text = rename_journal_to_journaltitle(text)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == '@inproceedings{Dick2014,' and (
            i + 1 >= len(lines) or not lines[i + 1].lstrip().lower().startswith('url')
        ):
            lines.insert(i + 1, '  url = {https://api.semanticscholar.org/CorpusID:9473630},')
            break
    f.write_text('\n'.join(lines))


def wrap_bibtex_titles_braced(text: str) -> str:
    """
    Adds exactly one extra {} around every braced BibTeX title value.
    Robust to nested braces and titles embedded on the same line.
    """
    pat = re.compile(r'(?i)\btitle\s*=\s*(?=\{)')  # lookahead so we don't consume '{'
    i, out, n = 0, [], len(text)

    while True:
        m = pat.search(text, i)
        if not m:
            out.append(text[i:])
            break

        j = m.end()  # position of the '{'
        out.append(text[i:j])  # up to before '{'
        end, inner = _read_braced(text, j)
        out.append('{{' + inner + '}}')
        i = end + 1  # skip original closing '}'

    return ''.join(out)


def _read_braced(s: str, start: int):
    """Return (end_index_of_matching_brace, inner_text) for s[start]=='{' with nesting."""
    depth, k, n = 0, start, len(s)
    while k < n:
        ch = s[k]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return k, s[start + 1 : k]
        k += 1
    return n - 1, s[start + 1 :]  # fallback if unmatched


def remove_braced_abstract_and_url(bib_text: str) -> str:
    """
    Remove 'abstract' and 'url' fields whose values are {...} (possibly multi-line),
    and also remove the now-empty line. Case-insensitive field names.
    """
    pat = re.compile(r'(?mi)^\s*(abstract|url)\s*=\s*\{')
    s = bib_text
    out = []
    i = 0

    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:])
            break

        # keep everything before start-of-line of the field
        out.append(s[i : m.start()])

        # find matching closing brace of the field value
        open_idx = m.end() - 1  # points to the '{'
        depth = 0
        j = open_idx
        esc = False
        while j < len(s):
            c = s[j]
            if c == '{' and not esc:
                depth += 1
            elif c == '}' and not esc:
                depth -= 1
                if depth == 0:
                    break
            esc = c == '\\' and not esc
            j += 1
        if j >= len(s):  # unmatched brace; bail out safely
            out.append(s[m.start() :])
            break

        k = j + 1  # first char after the closing '}'

        # swallow trailing spaces/tabs, optional comma, and spaces/tabs again
        while k < len(s) and s[k] in ' \t':
            k += 1
        if k < len(s) and s[k] == ',':
            k += 1
            while k < len(s) and s[k] in ' \t':
                k += 1

        # remove ONE newline (CRLF or LF) to avoid leaving an empty blank line
        if s.startswith('\r\n', k):
            k += 2
        elif k < len(s) and s[k] in '\r\n':
            k += 1

        # continue scanning after the removed field
        i = k

    return ''.join(out)


def rename_journal_to_journaltitle(bib_text: str) -> str:
    """
    Rename BibTeX 'journal' field to biblatex 'journaltitle' (case-insensitive).
    Assumes field is on one line. Preserves spacing and commas.
    """
    pat = re.compile(r'^(\s*)journal\b(\s*=)', re.IGNORECASE)
    return ''.join(pat.sub(r'\1journaltitle\2', line) for line in bib_text.splitlines(keepends=True))


if __name__ == '__main__':
    main()
