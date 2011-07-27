#!/bin/bash

#    Title: installdb-fmrd.sh
# Synopsis: Setup FMRD schema and pre-load lookup tables
#   Format: ./installdb-fmrd.sh
#     Date: 2010-08-02
#  Version: 0.8
#   Author: Howard Hamilton, Soccermetrics Research & Consulting, LLC

dropdb $1
createdb $1

psql -f fmrd.sql $1
psql -f fmrd-views.sql $1

./PreloadTables.pl $1