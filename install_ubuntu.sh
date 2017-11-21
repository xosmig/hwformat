#!/bin/bash

# Временно, чтобы можно было как-то пользоваться
# Потом надо будет сделать это как-нибудь нормально и кросплатформенно

GREEN='\e[1;32m'
RED='\e[1;31m'
NO_COLLOR='\033[0m'

function ok {
    printf "${GREEN}[^_^]${NO_COLLOR}\n"
    exit 0
}

function fail {
    printf "${RED}FAIL${NO_COLLOR}\n"
    exit 1
}

dir="$(dirname "$(realpath "$0")")" &&
target="$HOME/.local/bin/hwformat" &&
source="$dir/ubuntu_run_script_template.sh" &&
cp "$source" "$target" &&
sed -i "s|PATH_TO_SRC|$dir/src|g" "$target" &&
chmod ug=rwx "$target" &&
chmod o=rx "$target" &&
ok || fail

