#!/usr/bin/env python3
# !-*- coding:utf-8 -*-

from dataclasses import replace
import re

qnums = [
    "0０零", "1１一壱", "2２二弐", "3３三参", "4４四", "5５五伍", "6６六", "7７七", "8８八", "9９九",
    "万萬", "十拾", "千阡",
]

maybenums1 = "".join(qnums)

qnums = [list(x) for x in qnums]
qnummap = dict([
    (int(x[0]), x[1:])
    for x in qnums[:10]
])
###del x

qmandigit = [
    ["兆", 12],
    ["億", 8],
    ["万", 4],
    ["千", 3],
    ["百", 2],
    ["十", 1],
    ["z", 0],  # 番人
]

jkpattern = r"([" + maybenums1 + "".join([z[0] for z in qmandigit[:-1]]) + "]+)"
jkp = re.compile(jkpattern)
del maybenums1, jkpattern

qmanany = re.compile(r"(\d*)(\D)")
qmandict = dict(qmandigit)


def replace_jpnumeric_int(src):
    while True:
        qk = jkp.search(src)
        if qk == None:
            break
        rsrc = qk.group(1)
        result = to_int(rsrc)
        if str(result) == rsrc:
            break
        src = src.replace(rsrc, str(result))
    return src


def to_int(src):
    # src = src
    for qmap in qnums:  # 和数字を先にある程度数字に変換
        for q1 in qmap[1:]:
            src = src.replace(q1, qmap[0])
        del q1
    del qmap
    total = 0  # 合計
    ototal = 0  # 万進法未満の値
    for qk in qmanany.finditer(src + qmandigit[-1][0]):  # 単位文字で分割
        pick = qk.group(1)  # 今回の数字
        jkn = qmandict[qk.group(2)]  # の桁

        if jkn == 0 and pick == "":
            break

        if pick == "":
            if ototal == 0: # 1省略に雑に対応
                pick = "1"
            else:
                pick = "0"

        if jkn < 4:
            ototal += int(pick) * (10 ** jkn)
        else:
            ototal += int(pick)
            total += ototal * (10 ** jkn)
            ototal = 0
        pass
    total += ototal  # 万未満の残り
    return total

__all__ = [
    replace_jpnumeric_int.__name__,
    to_int.__name__
]
