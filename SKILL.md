---
name: ar-trend-report
description: Generate professional accounts receivable trend reports with month-over-month (MoM) analysis, year-over-year (YoY) comparison, and interactive visualizations. Input CSV/Excel with AR data, output comprehensive trend reports with charts.
version: 1.0.0
author: Custom
tags: [finance, accounting, receivable, report, trend, analysis]
---

# AR Trend Report Generator

Generate professional accounts receivable trend reports with comprehensive analytics and visualizations.

## What It Does

1. **Trend Analysis** — Visualize AR balance trends over 12+ months
2. **MoM Analysis** — Calculate and display month-over-month changes
3. **YoY Comparison** — Compare current period with same period last year
4. **Interactive Charts** — Generate 4-chart dashboard (trend, MoM, inflow/outflow, overdue)
5. **Executive Summary** — Auto-generate key insights and recommendations

## Input Data Format

CSV/Excel with columns:
- `month` (YYYY-MM format)
- `ar_balance` (月末应收余额)
- `new_ar` (本月新增应收)
- `collection` (本月回款金额)
- `overdue` (逾期金额)

Example:
```csv
month,ar_balance,new_ar,collection,overdue
2024-04,385000,125000,118000,42000
2024-05,412000,138000,111000,48000
```

## Usage

### Generate Report from CSV
```
Generate AR trend report from /path/to/ar_data.csv
```

### Generate with Custom Title
```
Create AR trend report titled "Q1 2025 Receivable Analysis" from data.csv
```

### Quick Analysis
```
Analyze my receivable trend and show MoM changes
```

## Output

- **PNG Charts**: 4-panel visualization dashboard
- **Markdown Report**: Executive summary with key metrics
- **CSV Export**: Detailed metrics for further analysis

## Report Includes

| Section | Content |
|---------|---------|
| Trend Chart | 12-month AR balance with high/low markers |
| MoM Chart | Month-over-month change percentage |
| Flow Chart | New AR vs Collection comparison |
| Overdue Chart | Overdue amount trend with warning line |
| Metrics | Current balance, avg, growth rate, YoY change |

## Installation

```bash
skillhub install ar-trend-report
# or copy to workspace/skills/ar-trend-report/
```

## Requirements

- Python 3.8+
- pandas
- matplotlib
- numpy

## Example Output

```
📊 AR Trend Analysis Report
===========================
Period: 2024-04 to 2025-03

Key Metrics:
- Current AR: ¥461,000 (-3.6% MoM)
- 12-Month Avg: ¥450,417
- Growth: +19.7% YoY
- Peak: ¥510,000 (2024-12)

Charts generated: ar_trend_dashboard.png
```
