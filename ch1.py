#!/usr/bin/python
#-*- encoding: utf-8 -*-
"""
Sample Codes for ThinkStats2 - Chapter1

Copyright 2015 @myuuuuun
URL: https://github.com/myuuuuun/ThinkStats2-Notebook
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import sys
sys.path.append('./code')
import pandas as pd
import nsfg
import custom_functions as cf


# Ex1 "Print value counts for prglngth and compare to results published in the codebook"
# DataBook: http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=PREG&section=A&subSec=8016&srtLabel=611931
def ex1pr1():
    # 2002年のPrefnancyに関するNSFGのデータフレームを読み込む
    df = nsfg.ReadFemPreg()

    # データフレームから妊娠期間の列を代入
    prglngth = df.prglngth

    # 妊娠週ごとに集計して表示
    print(prglngth.value_counts().sort_index())

    # 上記DataBookの表記に合うように集計
    print("\n+-----------------------------+")
    print("13 WEEKS OR LESS: {0}"  .format(prglngth[prglngth <= 13].count()))
    print("14-26 WEEKS: {0}"         .format(prglngth[(13 < prglngth) & (prglngth <= 26)].count()))
    print("27 WEEKS OR LONGER: {0}"  .format(prglngth[prglngth > 26].count()))
    print("\nTOTAL: {0}"             .format(len(prglngth)))
    print("+-----------------------------+")


#ex1pr1()


# Ex1 "Print value counts for agepreg and compare to results published in the codebook."
# DataBook: http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=PREG&section=A&subSec=8016&srtLabel=611935
def ex1pr2():
    # 2002年のPrefnancyに関するNSFGのデータフレームを読み込む
    df = nsfg.ReadFemPreg()

    # 妊娠した年齢の列を代入
    agepreg = df.agepreg

    # 妊娠した年齢を集計して表示
    print(agepreg.value_counts().sort_index())

    # 上記DataBookの表記に合うように集計
    print("\n+-----------------------------+")
    print("INAPPLICABLE: {0}"  .format(agepreg.isnull().sum()))
    print("UNDER 20 YEARS: {0}".format(df[df.agepreg < 20].agepreg.count()))
    print("20-24 YEARS: {0}"   .format(len(agepreg[(20 <= agepreg) & (agepreg < 25)])))  #条件が複数ある時は()でくくる。演算子はビット演算子を使う。
    print("25-29 YEARS: {0}"   .format(len(df.query("agepreg >= 25 & agepreg < 30"))))   #queryも利用できる
    print("30-44 YEARS: {0}"   .format(len([x for x in agepreg if x >= 30])))            #普通のリストと同様にリスト内包表記も使える

    print("\nTOTAL: {0}"  .format(len(agepreg)))  #len()は全要素数を、count()はNaNやNullを除いた要素数を返す
    print("TOTAL - INAPPLICABLE: {0}"  .format(agepreg.count()))
    print("+-----------------------------+")


#ex1pr2()


# Ex1 "Create a new column named totalwgt_kg that contains birth weight in kilograms. Compute its mean."
def ex1pr3():
    df = nsfg.ReadFemPreg()

    # 妊婦 +（お腹の）赤ちゃんの重さはポンドで記録されているので、データフレームに新しい列を追加し、そこにkgの重さを代入
    # pandas.DataFrameに新しい列をつくる時は dataframe['hoge'] のようにする。（dataframe.hoge = ... はダメ）
    df['totalwgt_kg'] = df.totalwgt_lb / 2.2  #1ポンド = 0.45kg

    # ポンドの列と、新しく作ったkgの列を比較（ちゃんと2.2倍くらいになっているか?）
    print(df[['totalwgt_kg', 'totalwgt_lb']])

    # ポンドの列の平均と、kgの列の平均を比較
    print("Mean(kg): {0}\nMean(pounds): {1}".format(df.totalwgt_kg.mean(), df.totalwgt_lb.mean()))


#ex1pr3()


# Ex1 "Look through the codebook and find a variable, other than the ones mentioned in the book, that you find interesting.
#      Compute values counts, means, or other statistics."
# Explanation of variables: http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=pregResp
# DataBook (BABYSEX): http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=PREG&section=&subSec=8014&srtLabel=611801
def ex1pr4():
    df = nsfg.ReadFemPreg()

    # データフレームにある全ての列と、その基本統計量を表示する
    #cf.show_info_df(df)

    # ここでは、赤ちゃんの性別がどの位の割合で分布しているか確かめてみる
    # 一般には、男105 : 女100 くらいだと言われている
    babysex = df['babysex']

    # babysexの列の基本統計量を表示
    print(babysex.describe(), "\n")

    # 「1」は男、「2」は女の意味（DataBookを参照）なので、置き換えて何行か表示してみる
    print(babysex.replace({1: "Male", 2:"Female"}))

    # 男女比がどのくらいか調べてみる
    print("\nTotal: {0}\nMale: {1}\nFemale: {2}\nNaN: {3}\n" \
        .format(len(babysex), len(df[df.babysex == 1]), len(df[df.babysex == 2]), df.babysex.isnull().sum()))
    print("Percentage of Male: {0:.3f}%\nPercentage of Feale: {1:.3f}%" \
        .format((len(df[df.babysex == 1]) * 100 / df.babysex.count()), (len(df[df.babysex == 2]) * 100 / df.babysex.count())))


#ex1pr4()


# Ex1 "Count the number of live births with birthwgt_lb between 9 and 95 pounds (including both). The result should be 798"
def ex1pr5():
    df = nsfg.ReadFemPreg()

    # outcome列を使い、生きて産まれた赤ちゃんだけを取り出す。
    live = df[df.outcome == 1]

    # 取り出した赤ちゃんの重さを表示する
    birthwgt_lb = df.birthwgt_lb
    print("From 9 to 95 pounds: {0}".format(len(live.query("birthwgt_lb >= 9 & birthwgt_lb <= 95"))))


#ex1pr5()


# Ex1 "Compute the mean prglngth for first babies and others. Compute the difference in means, expressed in hours."
def ex1pr6():
    df = nsfg.ReadFemPreg()

    # 1人目の赤ちゃんと、2人目以降の赤ちゃんをとり出す
    firsts = df[df.birthord == 1]
    others = df[df.birthord > 1]

    # それぞれ妊娠期間の平均を計算する
    weeks_f = firsts['prglngth'].mean()
    weeks_o = others['prglngth'].mean()

    # その差をhour単位に換算
    difference = (weeks_f - weeks_o) * 7 * 24

    print("1st babies prglngth(mean): {0:.3} WEEKS".format(weeks_f))
    print("Other babies prglngth(mean): {0:.3} WEEKS".format(weeks_o))
    print("Difference(firsts - others): {0:.3} hours".format(difference))


#ex1pr6()


# Ex2 "Print the value counts for this variable(pregnum: how many times each respondent has been pregnant) and compare them to the published results."
# DataBook: http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=FEM&section=R&subSec=7869&srtLabel=606835
def ex2pr1():
    df = cf.ReadFemResp()

    # データが何回目の妊娠かを出力
    pregnum = df['pregnum']
    #printf(pregnum)
    print(pregnum.value_counts().sort_index(), "\n") #19回は信頼性のある数字か？
    print("NONE: {0}".format(len(df.query("pregnum == 0"))))
    print("1 PREGNANCY: {0}".format(len(df.query("pregnum == 1"))))
    print("2 PREGNANCIES: {0}".format(len(df.query("pregnum == 2"))))
    print("3 PREGNANCIES: {0}".format(len(df.query("pregnum == 3"))))
    print("4 PREGNANCIES: {0}".format(len(df.query("pregnum == 4"))))
    print("5 PREGNANCIES: {0}".format(len(df.query("pregnum == 5"))))
    print("6 PREGNANCIES: {0}".format(len(df.query("pregnum == 6"))))
    print("7 OR MORE PREGNANCIES: {0}".format(len(df.query("pregnum > 6"))))
    print("\nTOTAL: {0}".format(pregnum.count()))
    

#ex2pr1()


# Ex2 Preg辞書とResp辞書のそれぞれで、同じcaseidを持つ回答者が同じpregnumの値を答えているか調べる
def ex2pr2():
    df = nsfg.ReadFemPreg()
    df2 = cf.ReadFemResp()
    dict_preg = nsfg.MakePregMap(df)

    for caseid in sorted(dict_preg):
        pregnum_of_df = len(dict_preg[caseid])
        pregnum_of_df2 = df2[df2.caseid == caseid].pregnum.values[0]

        # 一致していたらtrue
        is_valid = pregnum_of_df == pregnum_of_df2

        # 全てのcaseidについて、2つの辞書で妊娠回数が一致しているかprint
        """
        print("\ncaseid: {0}さんは、".format(caseid))
        message = "正しいデータです！" if is_valid else "不正なデータです！"
        print(message)
        print("Preg: {0}人、 Resp: {1}人\n".format(pregnum_of_df, pregnum_of_df2))
        print("+" + "-" * 20 + "+")
        """

        if is_valid == False:
            break

    # 全て一致していたらTrue, 1つでも違ったらFalse
    print(is_valid)


#ex2pr2()



