# AR Trend Report Generator

Generate professional accounts receivable trend reports with month-over-month (MoM) analysis, year-over-year (YoY) comparison, and interactive visualizations.

## Features

- 📈 **Trend Analysis** — Visualize AR balance trends over 12+ months
- 📊 **MoM Analysis** — Calculate and display month-over-month changes  
- 📉 **YoY Comparison** — Compare current period with same period last year
- 🎨 **Interactive Charts** — Generate 4-chart dashboard
- 📝 **Executive Summary** — Auto-generate key insights and recommendations
- 🌐 **Multi-language** — Support for Chinese/English column names

## Installation

```bash
# Clone this repository
git clone https://github.com/your-username/ar-trend-report.git

# Install dependencies
pip install pandas matplotlib numpy
```

## Quick Start

```bash
# Generate report from sample data
python scripts/generate_ar_report.py \
  --input examples/sample_data.csv \
  --output my_report \
  --title "AR Trend Analysis"
```

## Input Data Format

CSV or Excel with columns:

| Column | Chinese | Required | Description |
|--------|---------|----------|-------------|
| `month` | 月份 | ✅ | YYYY-MM format |
| `ar_balance` | 应收余额 | ✅ | Month-end AR balance |
| `new_ar` | 新增应收 | ❌ | New AR this month |
| `collection` | 回款 | ❌ | Collection amount |
| `overdue` | 逾期 | ❌ | Overdue amount |

### Example CSV

```csv
month,ar_balance,new_ar,collection,overdue
2024-04,385000,125000,118000,42000
2024-05,412000,138000,111000,48000
2024-06,398000,142000,156000,52000
```

## Usage

### Command Line

```bash
python scripts/generate_ar_report.py \
  --input data.csv \
  --output report_name \
  --title "My AR Report" \
  --format both
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--input, -i` | Input CSV/Excel file | Required |
| `--output, -o` | Output filename prefix | `ar_report` |
| `--title, -t` | Report title | `AR Trend Analysis` |
| `--format` | Output format: png/md/both | `both` |

## Output

### 1. Chart Dashboard (`*_charts.png`)
Four-panel visualization:
- **AR Balance Trend** — 12-month trend with high/low markers
- **MoM Change (%)** — Month-over-month percentage change
- **New AR vs Collection** — Side-by-side comparison
- **Overdue Trend** — Overdue amount with warning line

### 2. Markdown Report (`*.md`)
- Key metrics summary
- Detailed MoM analysis table
- Automated insights
- Actionable recommendations

## Sample Output

```
📊 AR Trend Analysis Report
===========================
Period: 2024-04 to 2025-03

Key Metrics:
- Current AR: ¥461,000 (-3.6% MoM)
- 12-Month Avg: ¥450,417
- YoY Growth: +19.7%
- Peak: ¥510,000 (2024-12)

Charts generated: ar_report_charts.png
```

## OpenClaw Integration

Add to your OpenClaw skills folder:

```bash
cp -r ar-trend-report ~/.openclaw/workspace/skills/
```

Then use natural language:
```
"Generate AR trend report from data.csv"
"Analyze my receivable trend for the past year"
```

## License

MIT License - Feel free to use and modify!

## Contributing

Pull requests welcome! Please include test data with any changes.
