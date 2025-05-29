#!/bin/bash

# Usage: ./tikz2png.sh diagram.tex

# Check input
if [ $# -ne 1 ]; then
  echo "Usage: $0 <filename.tex>"
  exit 1
fi

TEXFILE="$1"
BASENAME="${TEXFILE%.tex}"

# Compile to PDF
echo "Compiling $TEXFILE to PDF..."
pdflatex -interaction=nonstopmode "$TEXFILE" > /dev/null

if [ ! -f "$BASENAME.pdf" ]; then
  echo "PDF not generated. Check LaTeX errors."
  exit 1
fi

# Convert PDF to PNG using ImageMagick
echo "Converting PDF to PNG..."
convert -density 300 "$BASENAME.pdf" -quality 90 "$BASENAME.png"

if [ -f "$BASENAME.png" ]; then
  echo "Done: $BASENAME.png"
else
  echo "Conversion failed."
fi
