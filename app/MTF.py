# -*-coding: utf-8 -*-

import pandas as pd

# ---------------------------------------------------------------------
# Load data 
path = ['data/', 'result/']
file = ['client', 'all_data']
res_file = ['group_top_n_brand', 'group_top_n_category', 'group_top_n_pair']

df_group_brand_res = pd.read_csv(f'{path[1]}{res_file[0]}.csv', encoding='utf8')
df_group_cat_res = pd.read_csv(f'{path[1]}{res_file[1]}.csv', encoding='utf8')
df_cb_res = pd.read_csv(f'{path[1]}{res_file[2]}.csv', encoding='utf8')


# ---------------------------------------------------------------------
# transformate data
def insert_trans(insert_data, bins):
    result=['']
    for i in range(len(bins)):
        if insert_data[0] in range(bins[i], bins[i+1]):
            result[0] = i
            break

    if insert_data[1] == 0: result.append(0)
    elif insert_data[1] == 1: result.append(1)
    else: result.append(-1)

    group_id = str(result[0])+'_'+str(result[1])
    
    return group_id
	

	
# get data
def tar_recommand(df_res, user_title, tar_user, tar_title_list):
    '''
    ==============================================
    
    ==============================================
    >* df_res: the dataframe with users and top n recommand target
    >* user_title: the name of column where user in 
    >* tar_user: the target user 
    >* tar_title_list: list of target items
    '''
    return df_res[df_res[user_title]==tar_user][tar_title_list]

# ---------------------------------------------------------------------	

# transformate data
"""
A = (55, 0) 
bins = [0, 19, 22, 23, 32, 40, 100]
group_id = insert_trans(A, bins)

# ---------------------------------------------------------------------
# get data: brand
tar_recommand(df_group_brand_res, 'group', group_id, ['brand'])
# ---------------------------------------------------------------------
# get data: category
tar_recommand(df_group_cat_res, 'group', group_id, ['category'])
# ---------------------------------------------------------------------
# get data: category & brand pair
tar_recommand(df_cb_res, 'group', group_id, ['category', 'brand'])
"""
