#!/bin/sh
elyxer --destdirectory images/ --title "FMRD User Manual" fmrd-manual.lyx fmrd-manual.html
elyxer --tocfor fmrd-manual.html --css "docs/toc.css" --destdirectory images/ --target "toc" fmrd-manual.lyx fmrd-manual-toc.html
