#!/usr/bin/python
#-*- encoding: utf-8 -*-
"""
Sample Codes for ThinkStats2 - Chapter2

Copyright 2015 @myuuuuun
URL: https://github.com/myuuuuun/ThinkStats2-Notebook
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import sys
sys.path.append('./code')
import pandas as pd
import nsfg
import custom_functions as cf
import sys
import math
import thinkstats2
import thinkplot


# Cohenのdを求める
def CohenEffectSize(g1, g2):
    diff = g1.mean() - g2.mean()
    var1 = g1.var()
    var2 = g2.var()
    n1 = len(g1)
    n2 = len(g2)

    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    d = diff / math.sqrt(pooled_var)
    return d


# 回答者の年齢をヒストグラムで表示する
def ex2pr1():
    df = cf.ReadFemResp()
    #print(df.age_r.value_counts().sort_index())  #年齢の頻度を表示（年齢順）
    #print(df.age_r.value_counts())  #年齢の頻度を表示（頻度順）
    hist = thinkstats2.Hist(df.age_r, label='age_r')
    thinkplot.Hist(hist)
    thinkplot.Show()


#ex2pr1()


# 回答者の家族人数をヒストグラムで表示する
def ex2pr2():
    df = cf.ReadFemResp()
    #print(df.numfmhh.value_counts().sort_index())  #家族人数の頻度を表示（家族の人数順）
    #print(df.numfmhh.value_counts())  #家族人数の頻度を表示（頻度順）
    hist = thinkstats2.Hist(df.numfmhh, label='anumfmhh')
    thinkplot.Hist(hist)
    thinkplot.Show()


#ex2pr2()


# 出産した子供の人数をヒストグラムで表示する
def ex2pr3():
    df = cf.ReadFemResp()
    #print(df.parity.value_counts().sort_index())  #出産人数の頻度を表示（家族人数順）。22や16はエラーとみなせるかもしれない。
    #print(df.parity.value_counts())  #出産人数の頻度を表示（頻度順）
    hist = thinkstats2.Hist(df.parity, label='parity')
    thinkplot.Hist(hist)
    thinkplot.Show()


#ex2pr3()


# 出産人数上位n件を表示する
def ex2pr4():
    df = cf.ReadFemResp()
    #print(df.parity.value_counts().sort_index())  #出産人数の頻度を表示（家族人数順）。22や16はエラーとみなせるかもしれない。
    #print(df.parity.value_counts())  #出産人数の頻度を表示（頻度順）
    hist = thinkstats2.Hist(df.parity)
    print(hist.Largest(5))


#ex2pr4()


# 富裕層の出産人数をヒストグラムで表示する
# totincrの詳細: http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=MALE&section=R&subSec=7958&srtLabel=609776
# 収入75000$以上の人（totincr = 14の人）をrich peopleとかんがえる。
def ex2pr5():
    df = cf.ReadFemResp()
    rich = df[df.totincr == 14]
    #print(rich.parity.value_counts().sort_index())  #出産人数の頻度を表示（家族人数順）
    #print(rich.parity.value_counts())  #出産人数の頻度を表示（頻度順）
    hist = thinkstats2.Hist(rich.parity, label='r_parity')
    thinkplot.Hist(hist)
    thinkplot.Show()


#ex2pr5()


# 富裕層の出産人数上位n件を表示する
def ex2pr6():
    df = cf.ReadFemResp()
    rich = df[df.totincr == 14]
    #print(rich.parity.value_counts().sort_index())  #出産人数の頻度を表示（家族人数順）
    #print(rich.parity.value_counts())  #出産人数の頻度を表示（頻度順）
    hist = thinkstats2.Hist(rich.parity)
    print(hist.Largest(5))


#ex2pr6()


# 富裕層とそれ以外の出産人数の平均を比較する
def ex2pr7():
    df = cf.ReadFemResp()
    rich = df[df.totincr == 14]
    norich = df[df.totincr != 14]
    print("富裕層の平均出産人数: ", rich.parity.mean())
    print("それ以外の平均出産人数: ", norich.parity.mean())


#ex2pr7()


# Exercise2.3
# Histオブジェクトを引数に取り、最頻値を返す関数
def Mode(hist):
    for key, freq in sorted(hist.Items(), key=lambda x:x[1], reverse=True): # 頻度の多い順に並び替えてループ
        return key # 1週目で関数を抜ける


# Histオブジェクトを引数に取り、頻度の降順に並び替えた[key, frequency]のリスト（二重配列）を返す関数
def AllModes(hist):
    m_list = []
    for key, freq in sorted(hist.Items(), key=lambda x:x[1], reverse=True): # 頻度の多い順に並び替えてループ
        m_list += [[key, freq]]
    return m_list


def ex3():
    df = cf.ReadFemResp()
    hist = thinkstats2.Hist(df.parity)
    print(Mode(hist))
    print(AllModes(hist))


#ex3()


# Exercise2.4
# 一番目の赤ちゃんは他の子どもよりも軽いか重いかを調べる
def ex4():
    df = nsfg.ReadFemPreg()
    first = df[df.birthord == 1]
    others = df[df.birthord > 1]
    hist1 = thinkstats2.Hist(first.totalwgt_lb, label='first')
    hist2 = thinkstats2.Hist(others.totalwgt_lb, label='others')
    
    print("1番目の赤ちゃんの重さの平均は: ", first.totalwgt_lb.mean(), " pounds")
    print("その他の赤ちゃんの重さの平均は: ", others.totalwgt_lb.mean(), " pounds")
    print("Cohenのdは: ", CohenEffectSize(others.totalwgt_lb, first.totalwgt_lb))


#ex4()



