#!/usr/bin/python
#-*- encoding: utf-8 -*-
"""
Sample Codes for ThinkStats2

Copyright 2015 @myuuuuun
URL: https://github.com/myuuuuun/ThinkStats2-Notebook
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function
from collections import defaultdict
import numpy as np
import pandas as pd
import sys
sys.path.append('./code')
import thinkstats2


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


def ReadFemResp(dct_file='./code/2002FemResp.dct',
                dat_file='./code/2002FemResp.dat.gz'):
    """Reads the NSFG pregnancy data.

    dct_file: string file name
    dat_file: string file name

    returns: DataFrame
    """
    dct = thinkstats2.ReadStataDct(dct_file)
    df = dct.ReadFixedWidth(dat_file, compression='gzip')
    return df


def MakeRespMap(df):
    """Make a map from caseid to list of preg indices.

    df: DataFrame

    returns: dict that maps from caseid to list of indices into preg df
    """
    d = defaultdict(list)
    for index, caseid in df.caseid.iteritems():
        d[caseid].append(index)
    return d


def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    df = ReadFemResp()
    print(df.shape)
    print('%s: All tests passed.' % script)

if __name__ == '__main__':
    main(*sys.argv)







