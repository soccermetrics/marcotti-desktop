#!/bin/bash

#    Title: installdb-fmrd.sh
# Synopsis: Setup FMRD schema and pre-load lookup tables
#   Format: ./installdb-fmrd.sh
#     Date: 2010-08-02
#  Version: 0.8
#   Author: Howard Hamilton, Soccermetrics Research & Consulting, LLC


dropdb fmrd_test
createdb fmrd_test

psql -f fmrd.sql fmrd_test
psql -f fmrd-views.sql fmrd_test

./PreloadTables.pl