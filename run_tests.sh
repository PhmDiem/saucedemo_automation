#!/bin/bash
set -euo pipefail

# ─── Config ───────────────────────────────────────
RESULTS_DIR="allure-results"
REPORTS_BASE="reports"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
REPORT_DIR="$REPORTS_BASE/$TIMESTAMP"

echo "Starting test run: $TIMESTAMP"

# ─── Step 1: Remove previous results ─────────────
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

# ─── Step 2: Run pytest ───────────────────────────
set +e
pytest tests/ --alluredir="$RESULTS_DIR" -v
PYTEST_EXIT=$?
set -e

# ─── Step 3: Copy history from the latest run ─────
LATEST=$(ls -td "$REPORTS_BASE"/*/ 2>/dev/null | head -1 || true)
if [ -n "$LATEST" ]; then
  echo "Copying history from: $LATEST"
  if [ -d "${LATEST}history" ]; then
    cp -r "${LATEST}history" "$RESULTS_DIR/history"
  else
    echo "No history available in the latest report"
  fi
else
  echo "First run; no history available"
fi

# ─── Step 4: Generate report in a new directory ───
mkdir -p "$REPORT_DIR"
allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean

echo ""
echo "Done! Report: $REPORT_DIR"
echo "Open report: allure open $REPORT_DIR"

exit "$PYTEST_EXIT"
