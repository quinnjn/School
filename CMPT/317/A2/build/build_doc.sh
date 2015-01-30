#!/bin/bash
for file in `find . -name *.tex`;do pdflatex $file; done
