python
"""店舗別の売上を集計して出力する。

使い方:
    python3 sales_report.py sales.csv
"""

import sys
import csv

DATE_COLUMN = 0
SHOP_COLUMN = 1
AMOUNT_COLUMN = 3


def load_rows(path):
    """CSVを読み込み、ヘッダー行を除いた行のリストを返す。"""
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        return list(reader)


def summarize(rows):
    """店舗名をキー、売上合計を値とする辞書を返す。
    パースできない行は標準エラーに出力してスキップする。
    """
    sales_by_shop = {}
    for line_no, row in enumerate(rows, start=2):
        try:
            shop = row[SHOP_COLUMN]
            amount = float(row[AMOUNT_COLUMN].replace(",", ""))
        except (IndexError, ValueError) as e:
            print(f"{line_no}行目をスキップしました: {e}", file=sys.stderr)
            continue
        sales_by_shop[shop] = sales_by_shop.get(shop, 0) + amount
    return sales_by_shop


def summarize_by_month(rows):
    """年月（YYYY-MM）をキー、売上合計を値とする辞書を返す。
    日付がパースできない行は標準エラーに出力してスキップする。
    """
    sales_by_month = {}
    for line_no, row in enumerate(rows, start=2):
        try:
            month = row[DATE_COLUMN][:7]  # "2026-01-15" -> "2026-01"
            amount = float(row[AMOUNT_COLUMN].replace(",", ""))
        except (IndexError, ValueError) as e:
            print(f"{line_no}行目をスキップしました: {e}", file=sys.stderr)
            continue
        sales_by_month[month] = sales_by_month.get(month, 0) + amount
    return sales_by_month


def main():
    if len(sys.argv) < 2:
        print("使い方: python3 sales_report.py <CSVファイル>", file=sys.stderr)
        return 1

    path = sys.argv[1]
    try:
        rows = load_rows(path)
    except OSError as e:
        print(f"ファイルを読み込めませんでした: {e}", file=sys.stderr)
        return 1

    sales_by_shop = summarize(rows)
    if not sales_by_shop:
        print("集計できる行がありませんでした。", file=sys.stderr)
        return 1

    total = sum(sales_by_shop.values())

    print("店舗別売上")
    for shop, amount in sorted(sales_by_shop.items(), key=lambda item: item[1], reverse=True):
        share = amount / total * 100 if total else 0
        print(f"{shop}: {amount:,.0f}円 ({share:.1f}%)")

    print(f"合計: {total:,.0f}円")
    print(f"平均: {total / len(sales_by_shop):,.0f}円")

    sales_by_month = summarize_by_month(rows)
    print()
    print("月別推移")
    for month, amount in sorted(sales_by_month.items()):
        print(f"{month}: {amount:,.0f}円")

    return 0


if __name__ == "__main__":
    sys.exit(main())