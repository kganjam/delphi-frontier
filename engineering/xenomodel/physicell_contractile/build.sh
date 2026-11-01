#!/usr/bin/env bash
# Build the contractile-construct PhysiCell 1.14.2 executable from a pristine upstream tree.
# usage: build.sh <pristine PhysiCell 1.14.2 tree> <build dir>
set -euo pipefail
SRC=$(cd "$(dirname "$0")" && pwd); PRISTINE=$1; B=$2
test "$(cat "$PRISTINE/VERSION.txt")" = "1.14.2"
rm -rf "$B"; cp -r "$PRISTINE" "$B"; chmod -R u+w "$B"; cd "$B"
make template >/dev/null
cp "$SRC/main.cpp" main.cpp
cp "$SRC/custom_modules/custom.cpp" "$SRC/custom_modules/custom.h" custom_modules/
cp "$SRC/PhysiCell_settings.xml" config/PhysiCell_settings.xml
make -j4 PROGRAM_NAME=xm_contractile
sha256sum xm_contractile
