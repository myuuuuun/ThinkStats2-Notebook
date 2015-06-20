#!/usr/bin/python
#-*- encoding: utf-8 -*-
# Sample codes for ThinkStats2 by @myuuuuun
# pandas tutorial: http://pandas.pydata.org/pandas-docs/stable/tutorials.html

import sys
sys.path.append('./code')
import pandas as pd
import nsfg
import chap01ex as ex2


df = nsfg.ReadFemPreg()
df2 = ex2.ReadFemResp()
#print(df.describe())


# Show All Rows
def printf(rows):
    pd.set_option('display.max_rows', len(rows))
    print(rows)
    pd.reset_option('display.max_rows')


# Usage of printf
    # printf(df.birthord)     # print all rows
    # printf(pregord[0:400])  # you can use slices


# Show All Columns
def printf_c(cols):
    pd.set_option('display.max_columns', cols.shape[1])
    pd.set_option('display.width', 200)
    print(cols)
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')


def show_info_df(DataFrame):
    print("行数: {0}, 列数: {1}\n".format(DataFrame.shape[0], DataFrame.shape[1]))
    print(DataFrame.info())
    print("\n\n\n# 基本統計量 + 先頭5行\n")
    describe = DataFrame.describe()
    head = DataFrame.head()
    printf_c(describe.append(head))


#show_info_df(df)


# Ex1 "Print value counts for prglngth and compare to results published in the codebook"
# Data: http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=PREG&section=A&subSec=8016&srtLabel=611931

def ex1pr1(df):
    prglngth = df.prglngth
    printf(prglngth.value_counts().sort_index())

    print(type(prglngth), "\n")

    print("13 WEEKS OR LESS: {0}"    .format(prglngth[prglngth <= 13].count()))
    print("14-26 WEEKS: {0}"         .format(prglngth[(13 < prglngth) & (prglngth <= 26)].count()))
    print("27 WEEKS OR LONGER: {0}"  .format(prglngth[prglngth > 26].count()))
    print("\nTOTAL: {0}"             .format(len(prglngth))) 


#ex1pr1(df)


# Ex1 "Print value counts for agepreg and compare to results published in the codebook."
# Data: http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=PREG&section=A&subSec=8016&srtLabel=611935

def ex1pr2(df):
    agepreg = df.agepreg
    printf(agepreg.value_counts().sort_index())

    print(type(agepreg), "\n")

    print("INAPPLICABLE: {0}"  .format(agepreg.isnull().sum()))
    print("UNDER 20 YEARS: {0}".format(df[df.agepreg < 20].agepreg.count()))
    print("20-24 YEARS: {0}"   .format(len(agepreg[(20 <= agepreg) & (agepreg < 25)])))  #条件が複数ある時は()でくくる。演算子はビット演算子を使う。
    print("25-29 YEARS: {0}"   .format(len(df.query("agepreg >= 25 & agepreg < 30"))))   #queryも利用できる
    print("30-44 YEARS: {0}"   .format(len([x for x in agepreg if x >= 30])))            #普通のリストと同様にリスト内包表記も使える

    print("\nTOTAL: {0}"  .format(len(agepreg)))  #len()は全要素数を、count()はNaNやNullを除いた要素数を返す
    print("TOTAL - INAPPLICABLE: {0}"  .format(agepreg.count()))


#ex1pr2(df)


# Ex1 "Create a new column named totalwgt_kg that contains birth weight in kilograms. Compute its mean."

def ex1pr3(df):
    df['totalwgt_kg'] = df.totalwgt_lb / 2.2
    print(df[['totalwgt_kg', 'totalwgt_lb']])
    print("Mean(kg): {0}\nMean(pounds): {1}".format(df.totalwgt_kg.mean(), df.totalwgt_lb.mean()))


#ex1pr3(df)


# Ex1 "Look through the codebook and find a variable, other than the ones mentioned in the book, that you find interesting.
#      Compute values counts, means, or other statistics."
# Explanation of variables: http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=pregResp
# Data(BABYSEX): http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=PREG&section=&subSec=8014&srtLabel=611801

def ex1pr4(df):
    #show_info_df(df)
    babysex = df['babysex']
    print(babysex.describe(), "\n")
    print(babysex.replace({1: "Male", 2:"Female"}))
    print("\nTotal: {0}\nMale: {1}\nFemale: {2}\nNaN: {3}\n" \
        .format(len(babysex), len(df[df.babysex == 1]), len(df[df.babysex == 2]), df.babysex.isnull().sum()))
    print("Percentage of Male: {0:.3f}%\nPercentage of Feale: {1:.3f}%" \
        .format((len(df[df.babysex == 1]) * 100 / df.babysex.count()), (len(df[df.babysex == 2]) * 100 / df.babysex.count())))


#ex1pr4(df)


# Ex1 "Count the number of live births with birthwgt_lb between 9 and 95 pounds (including both). The result should be 798"

def ex1pr5(df):
    live = df[df.outcome == 1]
    birthwgt_lb = df.birthwgt_lb

    print("From 9 to 95 pounds: {0}".format(len(live.query("birthwgt_lb >= 9 & birthwgt_lb <= 95"))))


#ex1pr5(df)


# Ex1 "Compute the mean prglngth for first babies and others. Compute the difference in means, expressed in hours."

def ex1pr6(df):
    firsts = df[df.birthord == 1]
    others = df[df.birthord > 1]
    weeks_f = firsts['prglngth'].mean()
    weeks_o = others['prglngth'].mean()
    difference = (weeks_f - weeks_o) * 7 * 24

    print("1st babies prglngth(mean): {0:.3} WEEKS".format(weeks_f))
    print("Other babies prglngth(mean): {0:.3} WEEKS".format(weeks_o))
    print("Difference(firsts - others): {0:.3} hours".format(difference))


#ex1pr6(df)


# Ex2 "Print the value counts for this variable(pregnum: how many times each respondent has been pregnant) and compare them to the published results."
# Data: http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=FEM&section=R&subSec=7869&srtLabel=606835

def ex2pr1(df):
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
    

#ex2pr1(df2)


# Ex2 Preg辞書とResp辞書のそれぞれで、同じcaseidを持つ回答者が同じpregnumの値を答えているか調べる
def ex2pr2(df, df2):
    dict_preg = nsfg.MakePregMap(df)

    for caseid in sorted(dict_preg):
        pregnum_of_df = len(dict_preg[caseid])
        pregnum_of_df2 = df2[df2.caseid == caseid].pregnum.values[0]

        print("\ncaseid: {0}さんは、".format(caseid))

        is_valid = pregnum_of_df == pregnum_of_df2
        message = "正しいデータです！" if is_valid else "不正なデータです！"
        print(message)
        print("Preg: {0}人、 Resp: {1}人\n".format(pregnum_of_df, pregnum_of_df2))
        print("+" + "-" * 20 + "+")


#ex2pr2(df, df2)













