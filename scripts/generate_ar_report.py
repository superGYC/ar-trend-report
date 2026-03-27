#!/usr/bin/env python3
"""
AR Trend Report Generator
Generate professional accounts receivable trend reports with MoM analysis
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
except ImportError as e:
    print(f"Error: Missing required package - {e}")
    print("Please install: pip install pandas matplotlib numpy")
    sys.exit(1)


def validate_input(file_path: str) -> Path:
    """Validate input file exists and is readable"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    if path.suffix.lower() not in ['.csv', '.xlsx', '.xls']:
        raise ValueError("Input must be CSV or Excel file")
    return path


def load_data(file_path: Path) -> pd.DataFrame:
    """Load data from CSV or Excel"""
    suffix = file_path.suffix.lower()
    if suffix == '.csv':
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()
    
    # Map common column name variations
    column_map = {
        '月份': 'month', '日期': 'month', 'period': 'month',
        '应收余额': 'ar_balance', '余额': 'ar_balance', 'balance': 'ar_balance',
        '新增应收': 'new_ar', '新增': 'new_ar', 'new': 'new_ar',
        '回款': 'collection', '回款金额': 'collection', 'collected': 'collection',
        '逾期': 'overdue', '逾期金额': 'overdue', 'overdue_amount': 'overdue'
    }
    
    df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
    
    # Validate required columns
    required = ['month', 'ar_balance']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Found: {list(df.columns)}")
    
    # Add optional columns with defaults if missing
    if 'new_ar' not in df.columns:
        df['new_ar'] = 0
    if 'collection' not in df.columns:
        df['collection'] = 0
    if 'overdue' not in df.columns:
        df['overdue'] = 0
    
    # Convert month to datetime
    df['month'] = pd.to_datetime(df['month'])
    df = df.sort_values('month')
    
    return df


def calculate_metrics(df: pd.DataFrame) -> dict:
    """Calculate key metrics"""
    current = df.iloc[-1]
    first = df.iloc[0]
    
    # MoM calculations
    df['mom_change'] = df['ar_balance'].pct_change() * 100
    df['mom_abs'] = df['ar_balance'].diff()
    
    # YoY calculation (if data spans 12+ months)
    yoy_change = ((current['ar_balance'] - first['ar_balance']) / first['ar_balance']) * 100
    
    # Identify trend
    recent_3m = df['mom_change'].tail(3).mean()
    if recent_3m > 2:
        trend = "increasing"
        trend_emoji = "📈"
    elif recent_3m < -2:
        trend = "decreasing"
        trend_emoji = "📉"
    else:
        trend = "stable"
        trend_emoji = "➡️"
    
    return {
        'current_balance': current['ar_balance'],
        'current_month': current['month'].strftime('%Y-%m'),
        'first_balance': first['ar_balance'],
        'first_month': first['month'].strftime('%Y-%m'),
        'avg_balance': df['ar_balance'].mean(),
        'max_balance': df['ar_balance'].max(),
        'min_balance': df['ar_balance'].min(),
        'yoy_change': yoy_change,
        'mom_change': current.get('mom_change', 0) if pd.notna(current.get('mom_change', 0)) else 0,
        'mom_abs': current.get('mom_abs', 0) if pd.notna(current.get('mom_abs', 0)) else 0,
        'trend': trend,
        'trend_emoji': trend_emoji,
        'months_count': len(df),
        'avg_new_ar': df['new_ar'].mean(),
        'avg_collection': df['collection'].mean(),
        'current_overdue': current['overdue'],
        'overdue_ratio': (current['overdue'] / current['ar_balance'] * 100) if current['ar_balance'] > 0 else 0
    }


def generate_charts(df: pd.DataFrame, metrics: dict, output_path: Path, title: str = "AR Trend Report"):
    """Generate visualization dashboard"""
    
    # Ensure MoM columns exist
    if 'mom_change' not in df.columns:
        df['mom_change'] = df['ar_balance'].pct_change() * 100
        df['mom_abs'] = df['ar_balance'].diff()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"{title}\n({metrics['first_month']} to {metrics['current_month']})", 
                 fontsize=14, fontweight='bold')
    
    months_label = [m.strftime('%y-%m') for m in df['month']]
    
    # Chart 1: AR Balance Trend
    ax1 = axes[0, 0]
    ax1.plot(range(len(df)), df['ar_balance'], marker='o', linewidth=2.5, 
             markersize=7, color='#2563eb', label='AR Balance')
    ax1.fill_between(range(len(df)), df['ar_balance'], alpha=0.25, color='#2563eb')
    ax1.set_title('AR Balance Trend', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Balance')
    ax1.set_xticks(range(len(df)))
    ax1.set_xticklabels(months_label, rotation=45)
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000:.0f}K'))
    
    # Mark high/low
    max_idx = df['ar_balance'].idxmax()
    min_idx = df['ar_balance'].idxmin()
    max_pos = df.index.get_loc(max_idx)
    min_pos = df.index.get_loc(min_idx)
    ax1.annotate(f'High: ¥{df.loc[max_idx, "ar_balance"]/1000:.0f}K', 
                 xy=(max_pos, df.loc[max_idx, 'ar_balance']),
                 xytext=(max_pos-0.5, df.loc[max_idx, 'ar_balance'] + 15000),
                 fontsize=9, color='green', fontweight='bold')
    ax1.annotate(f'Low: ¥{df.loc[min_idx, "ar_balance"]/1000:.0f}K', 
                 xy=(min_pos, df.loc[min_idx, 'ar_balance']),
                 xytext=(min_pos+0.5, df.loc[min_idx, 'ar_balance'] - 20000),
                 fontsize=9, color='red', fontweight='bold')
    
    # Chart 2: MoM Change
    ax2 = axes[0, 1]
    mom_data = df['mom_change'].dropna()
    colors = ['#22c55e' if x > 0 else '#ef4444' for x in mom_data]
    bars = ax2.bar(range(1, len(df)), mom_data, color=colors, alpha=0.8, width=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.set_title('Month-over-Month Change (%)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('MoM Change (%)')
    ax2.set_xticks(range(1, len(df)))
    ax2.set_xticklabels(months_label[1:], rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Chart 3: New AR vs Collection
    ax3 = axes[1, 0]
    x = range(len(df))
    width = 0.38
    ax3.bar([i - width/2 for i in x], df['new_ar'], width, 
            label='New AR', color='#3b82f6', alpha=0.85)
    ax3.bar([i + width/2 for i in x], df['collection'], width, 
            label='Collection', color='#10b981', alpha=0.85)
    ax3.set_title('New AR vs Collection', fontsize=11, fontweight='bold')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Amount')
    ax3.set_xticks(x)
    ax3.set_xticklabels(months_label, rotation=45)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000:.0f}K'))
    
    # Chart 4: Overdue Trend
    ax4 = axes[1, 1]
    ax4.plot(range(len(df)), df['overdue'], marker='s', linewidth=2.5, 
             markersize=7, color='#ef4444', label='Overdue')
    ax4.fill_between(range(len(df)), df['overdue'], alpha=0.25, color='#ef4444')
    
    # Warning line at 20% of avg AR
    warning_line = df['ar_balance'].mean() * 0.2
    ax4.axhline(y=warning_line, color='orange', linestyle='--', linewidth=1.5, 
                label=f'Warning Line (¥{warning_line/1000:.0f}K)')
    
    ax4.set_title('Overdue Amount Trend', fontsize=11, fontweight='bold')
    ax4.set_xlabel('Month')
    ax4.set_ylabel('Overdue Amount')
    ax4.set_xticks(range(len(df)))
    ax4.set_xticklabels(months_label, rotation=45)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x/1000:.0f}K'))
    
    plt.tight_layout()
    chart_path = output_path.with_name(output_path.stem + '_charts.png')
    plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return chart_path


def generate_markdown_report(df: pd.DataFrame, metrics: dict, title: str) -> str:
    """Generate markdown report"""
    
    # Ensure MoM columns exist
    if 'mom_change' not in df.columns:
        df['mom_change'] = df['ar_balance'].pct_change() * 100
        df['mom_abs'] = df['ar_balance'].diff()
    
    # Calculate MoM stats
    mom_increases = df[df['mom_change'] > 0]['mom_change']
    mom_decreases = df[df['mom_change'] < 0]['mom_change']
    
    report = f"""# {title}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Period**: {metrics['first_month']} to {metrics['current_month']}  
**Data Points**: {metrics['months_count']} months

---

## 📊 Key Metrics

| Metric | Value | Change |
|--------|-------|--------|
| Current AR Balance | ¥{metrics['current_balance']:,.0f} | {metrics['mom_change']:+.1f}% MoM |
| 12-Month Average | ¥{metrics['avg_balance']:,.0f} | - |
| Highest Balance | ¥{metrics['max_balance']:,.0f} | - |
| Lowest Balance | ¥{metrics['min_balance']:,.0f} | - |
| YoY Growth | {metrics['yoy_change']:+.1f}% | {metrics['trend_emoji']} {metrics['trend'].title()} |
| Overdue Ratio | {metrics['overdue_ratio']:.1f}% | - |

---

## 📈 Month-over-Month Analysis

| Month | AR Balance | MoM Change | MoM % |
|-------|------------|------------|-------|
"""
    
    for _, row in df.iterrows():
        month = row['month'].strftime('%Y-%m')
        balance = f"¥{row['ar_balance']:,.0f}"
        mom_abs = f"¥{row['mom_abs']:+.0f}" if pd.notna(row['mom_abs']) else "-"
        mom_pct = f"{row['mom_change']:+.1f}%" if pd.notna(row['mom_change']) else "-"
        report += f"| {month} | {balance} | {mom_abs} | {mom_pct} |\n"
    
    report += f"""

---

## 💡 Insights

- **Trend**: AR balance is {metrics['trend']} over the recent period
- **Growth**: {metrics['yoy_change']:+.1f}% change from start to end of period
- **Collection**: Average monthly collection ¥{metrics['avg_collection']:,.0f}
- **New AR**: Average monthly new AR ¥{metrics['avg_new_ar']:,.0f}
- **Overdue**: Current overdue ratio is {metrics['overdue_ratio']:.1f}%

---

## 🎯 Recommendations

"""
    
    if metrics['overdue_ratio'] > 20:
        report += "- ⚠️ **High overdue ratio** - Review collection procedures\n"
    elif metrics['overdue_ratio'] > 10:
        report += "- ⚡ **Monitor overdue** - Follow up on aging receivables\n"
    else:
        report += "- ✅ **Overdue healthy** - Maintain current practices\n"
    
    if metrics['yoy_change'] > 20:
        report += "- 📈 **AR growing fast** - Review credit policies\n"
    elif metrics['yoy_change'] < -10:
        report += "- 📉 **AR declining** - Potential collection improvement or sales drop\n"
    
    if metrics['trend'] == 'increasing':
        report += "- 🔍 **Upward trend** - Monitor cash flow impact\n"
    elif metrics['trend'] == 'decreasing':
        report += "- 💰 **Downward trend** - Good collection performance\n"
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Generate AR Trend Report')
    parser.add_argument('--input', '-i', required=True, help='Input CSV/Excel file')
    parser.add_argument('--output', '-o', default='ar_report', help='Output filename prefix')
    parser.add_argument('--title', '-t', default='AR Trend Analysis Report', help='Report title')
    parser.add_argument('--format', choices=['png', 'md', 'both'], default='both', 
                       help='Output format')
    args = parser.parse_args()
    
    try:
        # Load and validate data
        print(f"📂 Loading data from: {args.input}")
        input_path = validate_input(args.input)
        df = load_data(input_path)
        print(f"✅ Loaded {len(df)} months of data")
        
        # Calculate metrics
        print("📊 Calculating metrics...")
        metrics = calculate_metrics(df)
        
        # Generate charts
        output_base = Path(args.output)
        if args.format in ['png', 'both']:
            print("📈 Generating charts...")
            chart_path = generate_charts(df, metrics, output_base, args.title)
            print(f"✅ Charts saved: {chart_path}")
        
        # Generate markdown report
        if args.format in ['md', 'both']:
            print("📝 Generating report...")
            report = generate_markdown_report(df, metrics, args.title)
            report_path = output_base.with_suffix('.md')
            with open(report_path, 'w') as f:
                f.write(report)
            print(f"✅ Report saved: {report_path}")
        
        # Print summary
        print("\n" + "="*50)
        print("📋 SUMMARY")
        print("="*50)
        print(f"Current AR: ¥{metrics['current_balance']:,.0f}")
        print(f"MoM Change: {metrics['mom_change']:+.1f}%")
        print(f"YoY Growth: {metrics['yoy_change']:+.1f}%")
        print(f"Trend: {metrics['trend_emoji']} {metrics['trend'].title()}")
        print("="*50)
        
        # Output JSON for integration
        # Convert numpy types to Python native types
        def convert_to_native(obj):
            if hasattr(obj, 'item'):  # numpy scalar
                return obj.item()
            elif isinstance(obj, dict):
                return {k: convert_to_native(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_native(i) for i in obj]
            return obj
        
        result = {
            'success': True,
            'metrics': convert_to_native(metrics),
            'charts_path': str(chart_path) if args.format in ['png', 'both'] else None,
            'report_path': str(report_path) if args.format in ['md', 'both'] else None
        }
        print(f"\n📤 JSON_RESULT: {json.dumps(result)}")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        result = {'success': False, 'error': str(e)}
        print(f"\n📤 JSON_RESULT: {json.dumps(result)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
