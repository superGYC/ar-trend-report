#!/bin/bash
# AR Trend Report Skill Installer

echo "📦 Installing AR Trend Report Skill..."

SKILL_DIR="${HOME}/.openclaw/workspace/skills/ar-trend-report"

# Create directory
mkdir -p "${SKILL_DIR}/scripts"
mkdir -p "${SKILL_DIR}/examples"

# Check Python dependencies
echo "🔍 Checking dependencies..."
python3 -c "import pandas, matplotlib, numpy" 2>/dev/null || {
    echo "⚠️  Installing required Python packages..."
    pip3 install pandas matplotlib numpy -q
}

echo "✅ AR Trend Report Skill installed successfully!"
echo ""
echo "📖 Usage:"
echo "  python3 ${SKILL_DIR}/scripts/generate_ar_report.py --input your_data.csv --output report"
echo ""
echo "📁 Example data: ${SKILL_DIR}/examples/sample_data.csv"
