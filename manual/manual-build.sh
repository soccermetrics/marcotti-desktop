#!/bin/sh
python /usr/bin/elyxer.py --destdirectory images/ --title "FMRD User Manual" fmrd-manual.lyx fmrd-manual.html
python /usr/bin/elyxer.py --tocfor fmrd-manual.html --css "docs/toc.css" --destdirectory images/ --target "toc" fmrd-manual.lyx fmrd-manual-toc.html
