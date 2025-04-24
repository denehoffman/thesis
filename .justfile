default: build

import:
  rsync -av nhoffman@ernest.phys.cmu.edu:/raid3/nhoffman/thesis_analysis/analysis/plots/ figures

bib:
  biber --tool --configfile=format_bib.conf references.bib
  mv references_bibertool.bib references.bib
  ./unescape.py

build: clean bib
  latexmk -interaction=nonstopmode -halt-on-error -file-line-error -pdf -f main
  # pdflatex main -interaction=nonstopmode -halt-on-error -file-line-error
  # biber main
  # pdflatex main -interaction=nonstopmode -halt-on-error -file-line-error
  # pdflatex main -interaction=nonstopmode -halt-on-error -file-line-error

open: build
  zathura main.pdf

clean:
  latexmk -CA
  rm -f *SAVE-ERROR
  rm -f main.bbl
  rm -f references.bib.blg
