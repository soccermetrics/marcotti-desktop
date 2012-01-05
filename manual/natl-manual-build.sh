#!/bin/sh
python /usr/bin/elyxer.py --destdirectory images/ --title "FMRD User Manual" fmrd-natl-manual.lyx fmrd-natl-manual.html
python /usr/bin/elyxer.py --tocfor fmrd-natl-manual.html --css "docs/toc.css" --destdirectory images/ --target "toc" fmrd-natl-manual.lyx fmrd-natl-manual-toc.html
