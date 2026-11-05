#!/usr/bin/env bash
# install.sh - Zero-clone bootstrap for macOS and Linux
# Usage: curl -fsSL https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/install.sh | bash

set -euo pipefail

TARGET_DIR="${PANTHEON_TARGET_DIR:-$(pwd)}"
REF="${PANTHEON_REF:-main}"
REPO_RAW_URL="https://raw.githubusercontent.com/apswood/pantheon-ai-kit/${REF}"

echo "======================================================================"
echo "  PANTHEON AI SETUP KIT - UNIX BOOTSTRAPPER (macOS & Linux)"
echo "======================================================================"
echo "  Target Directory : ${TARGET_DIR}"
echo "  Release Reference: ${REF}"

mkdir -p "${TARGET_DIR}"
cd "${TARGET_DIR}"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "  [ERROR] Python 3.10+ was not found on PATH."
    echo "          Please install Python 3.10 or higher and run again."
    exit 1
fi

echo "  Using Python: $($PYTHON_CMD --version 2>&1)"

TMP_SETUP="$(mktemp -t pantheon_setup_XXXXXX.py 2>/dev/null || mktemp /tmp/pantheon_setup_XXXXXX.py)"
trap 'rm -f "${TMP_SETUP}"' EXIT

echo "  Fetching installer..."
curl -fsSL "${REPO_RAW_URL}/setup.py" -o "${TMP_SETUP}"

$PYTHON_CMD "${TMP_SETUP}" --init-env --target-dir "${TARGET_DIR}" --ref "${REF}" "$@"
