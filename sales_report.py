import sys
import csv


def load(path):
    f = open(path)
    r = csv.reader(f)
    next(r)
    d = []
    for row in r:
        try:
            d.append(row)
        except:
            pass
    return d


def summarize(d):
    tmp = {}
    for row in d:
        shop = row[1]
        amount = float(row[3])
        if shop in tmp:
            tmp[shop] = tmp[shop] + amount
        else:
            tmp[shop] = amount
    return tmp


def main():
    path = sys.argv[1]
    d = load(path)
    tmp = summarize(d)

    total = 0
    for k in tmp:
        total = total + tmp[k]

    print("店舗別売上")
    for k in tmp:
        print(k, tmp[k], tmp[k] / total * 100)

    print("合計", total)
    print("平均", total / len(tmp))


main()
