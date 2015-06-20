#!/usr/bin/python
#-*- encoding: utf-8 -*-
# Sample codes for ThinkStats2 by @myuuuuun
# pandas tutorial: http://pandas.pydata.org/pandas-docs/stable/tutorials.html

import sys
import math
sys.path.append('./code')
import pandas as pd
import nsfg
import thinkstats2
import thinkplot
import chap01ex as ex1


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