#!/bin/bash

# Временно, чтобы можно было как-то пользоваться
# Потом надо будет сделать это как-нибудь нормально и кросплатформенно

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

function check_root {
    if [[ "$EUID" -ne 0 ]]; then
        echo "You must be a root user" 1>&2
        return 1
    fi
    return 0
}

check_root &&
TARGET="/usr/local/bin/hwformat" &&
SOURCE="ubuntu_run_script_template.sh" &&
cp "$SOURCE" "$TARGET" &&
sed -i "s|PATH_TO_SRC|$PWD/src|g" "$TARGET" &&
sudo chmod ug=rwx "$TARGET" &&
sudo chmod o=rx "$TARGET" &&
ok || fail

