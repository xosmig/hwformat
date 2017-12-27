#!/bin/bash

function ok {
    GREEN='\e[1;32m'
    NC='\033[0m' # No Color
    printf "${GREEN}[^_^]${NC}\n"
    exit 0
}

function fail {
    RED='\e[1;31m'
    NC='\033[0m' # No Color
    printf "${RED}FAIL${NC}\n"
    exit 1
}

SRC_PATH="PATH_TO_SRC" &&
python3 -- "$SRC_PATH/hwformat.py" "$@" &&
file="$1" &&
tex="${file%.hw}.tex" &&
pdflatex "$tex" &&
pdflatex "$tex" &&
aux="${file%.hw}.aux" &&
log="${file%.hw}.log" &&
rm -f "$log" "$aux" &&
ok || fail
