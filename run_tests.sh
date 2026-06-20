#!/bin/bash

# ─── Config ───────────────────────────────────────
RESULTS_DIR="allure-results"
REPORTS_BASE="allure-reports"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
REPORT_DIR="$REPORTS_BASE/$TIMESTAMP"

echo "🚀 Bắt đầu chạy test: $TIMESTAMP"

# ─── Bước 1: Xoá results cũ ───────────────────────
rm -rf $RESULTS_DIR
mkdir -p $RESULTS_DIR

# ─── Bước 2: Chạy pytest ──────────────────────────
pytest tests/ --alluredir=$RESULTS_DIR -v

# ─── Bước 3: Copy history từ lần chạy gần nhất ───
LATEST=$(ls -t $REPORTS_BASE 2>/dev/null | head -1)
if [ -n "$LATEST" ]; then
  echo "📋 Copy history từ: $LATEST"
  cp -r "$REPORTS_BASE/$LATEST/history" "$RESULTS_DIR/history"
else
  echo "ℹ️  Lần đầu chạy, chưa có history"
fi

# ─── Bước 4: Generate report vào thư mục mới ──────
mkdir -p $REPORT_DIR
allure generate $RESULTS_DIR -o $REPORT_DIR --clean

echo ""
echo "✅ Done! Report tại: $REPORT_DIR"
echo "👉 Mở report: allure open $REPORT_DIR"