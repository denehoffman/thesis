build:
  biber main
  latexmk -verbose -synctex=1 -interaction=nonstopmode -shell-escape

open: build
  sioyek main.pdf

transfer:
  rsync -avz nhoffman@ernest.phys.cmu.edu:/raid3/nhoffman/gluex_ksks/analysis/plots/* figures/
