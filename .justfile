default: build

import:
  rsync -av nhoffman@ernest.phys.cmu.edu:/raid3/nhoffman/thesis_analysis/analysis/plots/ figures
  rsync -av nhoffman@ernest.phys.cmu.edu:/raid3/nhoffman/thesis_analysis/analysis/reports/ reports

bib:
  biber --tool --configfile=format_bib.conf references.bib
  mv references_bibertool.bib references.bib
  ./unescape.py

build: clean
  #!/usr/bin/env bash
  set -x
  pdflatex -draftmode -interaction=batchmode -shell-escape main
  biber main
  pdflatex -draftmode -interaction=batchmode -shell-escape main
  pdflatex -interaction=batchmode -shell-escape main
  exit 0

update:
  pdflatex -interaction=batchmode -shell-escape main

open: build
  zathura main.pdf

clean:
  latexmk -CA
  rm -f *SAVE-ERROR
  rm -f main.bbl
  rm -f references.bib.blg
