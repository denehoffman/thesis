build:
  biber main
  latexmk -verbose -synctex=1 -interaction=nonstopmode -shell-escape

open: build
  sioyek main.pdf
