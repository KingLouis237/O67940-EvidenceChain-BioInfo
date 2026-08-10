#!/usr/bin/env bash

set -euo pipefail

VERSION="18-8cc5c"

URL="https://github.com/soedinglab/MMseqs2/releases/download/${VERSION}/mmseqs-linux-sse41.tar.gz"

EXPECTED_ARCHIVE_SHA256="0ece6a6af8f5d198bccabc98cb5fddfc9212ce04bb332e486bfdcc468c0d7b08"
EXPECTED_BINARY_SHA256="0930c12e79b78d5f3546adac8cd7e302a1a0a308b30edb8178f7466f3855ec4f"

DEST="tools/mmseqs2_${VERSION}_sse41"

if ! grep -qm1 '\bsse4_1\b' /proc/cpuinfo; then
    echo "ERROR: SSE4.1 support was not detected on this host." >&2
    exit 1
fi

TMPDIR_LOCAL=$(mktemp -d)
trap 'rm -rf "$TMPDIR_LOCAL"' EXIT

ARCHIVE="${TMPDIR_LOCAL}/mmseqs-linux-sse41.tar.gz"

echo "Downloading MMseqs2 ${VERSION} SSE4.1 build..."

wget -q \
    "$URL" \
    -O "$ARCHIVE"

echo "${EXPECTED_ARCHIVE_SHA256}  ${ARCHIVE}" \
    | sha256sum -c -

rm -rf "$DEST"
mkdir -p "$DEST"

tar -xzf \
    "$ARCHIVE" \
    -C "$DEST" \
    --strip-components=1

echo "${EXPECTED_BINARY_SHA256}  ${DEST}/bin/mmseqs" \
    | sha256sum -c -

echo
echo "Installed binary:"
"$DEST/bin/mmseqs" version
