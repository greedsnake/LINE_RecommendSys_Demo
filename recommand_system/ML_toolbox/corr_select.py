# -*- coding: utf-8 -*-
'''
This tool provides tools to select features by correlation. 
----------------------------------
This module require install pandas and numpy. 
pip install pandas
pip install numpy
'''

import pandas as pd
import numpy as np
import seaborn as sns
import sys
from sklearn.decomposition import PCA



def multicollinearity_prevent(df, y_lab, corr_method = 'spearman', level=0.7):
    '''
    ----------------------------------
    prevent multicollinearity. 
    if the features pair reach the level, compare their correlation value with y.
    Then drop the lower one. 
    ----------------------------------
    df: target dataframe contain y 
    tar: y
    corr_method: the method of correlation calculate (‘pearson’, ‘kendall’, ‘spearman’), default 'spearman' 
    level: the level u want to select to remove feature, default 0.7
    '''
    corr_table = df.corr(method = corr_method)
    
    left_col = list(corr_table.index)
    drop_list = []

    for row in left_col:
        for col in  left_col:
            if abs(corr_table[row][col]) > level:
                drop_list.append([row, col])

    drop_col = []
    for pair_list in drop_list:
        if pair_list[0] == pair_list[1]:     # skip diagonal, because it always be 1
            pass
        else: 
            corr_A = corr_table[y_lab][pair_list[0]]
            corr_B = corr_table[y_lab][pair_list[1]]
            if corr_A > corr_B: drop_col.append(pair_list[0])
            else: drop_col.append(pair_list[1])

#     return df.drop(columns=set(drop_col))
    return set(drop_col)




def corr_select(df, y_lab, corr_method, level):
    '''
    ----------------------------------
    select the features which reach the level have set.
    ----------------------------------
    df: target dataframe contain y 
    y_lab: y label
    corr_method: the method of correlation calculate (‘pearson’, ‘kendall’, ‘spearman’), default 'spearman' 
    level: the level you want to select to remove feature
    '''
    drop_list=[]
    for i in df.columns[2:]:   # beside row_id and country_code
        if abs(df[y_lab].corr(df[i], method = corr_method)) < level:
            drop_list.append(i)

    df.drop(drop_list, axis = 1, inplace=True)
    print(df.shape)
    print(df.columns)
    
    

    
    
def corr_plot(df, tar_list, method='spearman'):
    '''
    ----------------------------------
    show the correlation between features in tar_list, then return the correlation table.
    ----------------------------------
    >* df: target dataframe (pandas.DataFrame)
    >* tar_list: the target features (list)
    >* method: the method of correlation calculate ('pearson','kendall','spearman'). default is 'spearman' (sting)
    '''
    # create correlation table
    corr_table = df[tar_list].corr(method=method)
    
    # picture of correlation table
    fig = plt.figure()
    fig.set_figheight(20)
    fig.set_figwidth(20)

    g=sns.heatmap(corr_table,
                  vmax=1,
                  linewidths=0.01,
                  square=True,
                  cmap='YlGnBu',
                  linecolor="white")
    
    plt.title('Correlation between features')
    
    return corr_table
    
    
    

def pca_reduce_col(df_list, tar_list, size):
    '''
    ----------------------------------
    use pca to solve multicollinearity problem.
    ----------------------------------
    >* df_list: the list contain all target dataframe. (list contain pd.DataFrame)
    >* tar_list: the list contain target features name. (list contain strings)
    >* size: n_components in PCA 
    '''
    for df in df_list:
        count=1
        print('df size before PCA: ', df.shape)

        for tar in tar_list:
            pca = PCA(n_components=size)
            pca = pca.fit(df_train[tar])

    #         unit_vec = pca.components_
    #         print('{} unit components: '.format(tar), unit_vec)

            reduce_data_train = pca.transform(df[tar])

            df.drop(columns=tar, inplace=True)

            df['PCA_{}'.format(count)] = reduce_data
            count+=1

        print('df size after PCA: ', df.shape)
    
# if __name__ == '__main__':


