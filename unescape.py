#!/usr/bin/env python3
from pathlib import Path

def main():
    f = Path('references.bib')
    text = f.read_text()
    text = text.replace(r'\{', '{').replace(r'\}', '}')
    f.write_text(text)

if __name__ == "__main__":
    main()
