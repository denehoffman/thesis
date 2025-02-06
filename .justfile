build:
  # latexmk -verbose -synctex=1 -interaction=nonstopmode -shell-escape -pdf
  pdflatex main
  bibtex main
  pdflatex main
  pdflatex main

open: build
  sioyek main.pdf
