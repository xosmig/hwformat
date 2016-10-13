#!/bin/bash

function install {
    target="/usr/local/bin/hwformat"
    path="$PWD"

    if "true"; then
        printf "#!"
        printf "/bin/bash\n"
        printf "python3 -- \"$path/src/hwformat.py\" \"\$@\"\n"
    fi > "$target" &&
    chmod ug=rwx "$target" &&
    chmod o=rx "$target"
}

function ok {
    GREEN='\e[1;32m'
    NC='\033[0m' # No Color
    printf "${GREEN}[^_^]${NC}\n"
}

function fail {
    RED='\e[1;31m'
    NC='\033[0m' # No Color
    printf "${RED}FAIL${NC}\n"
}

if install; then
    ok
else
    fail
fi
