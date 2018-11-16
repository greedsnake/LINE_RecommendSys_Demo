# -*-coding: utf-8 -*-
'''

'''
# import modules

import time
import sys
from typing import Dict

named_libs = [('pandas', 'pd'),
              ('numpy', 'np')] # (library_name, shorthand)

for (name, short) in named_libs:
    try:
        lib = __import__(name)
    except:
        print(sys.exc_info())
    else:
        globals()[short] = lib


try: 
    from surprise import SVD, NMF, accuracy
    from surprise import Dataset, Reader
    from surprise.model_selection import cross_validate, train_test_split
    from scipy.spatial.distance import cosine
except:
    print(sys.exc_info())    


    
    
    
#     
class svd_recommand_sys():    

    
    def __init__(self):
        pass
    
    
    
    def result_in_different_col(self, df_res, res_users, top_n):
        '''
        ==============================================
        put result in different columns
        |        | recommand_1 | ... | recommand_n |
        |--------|-------------|-----|-------------|
        | user_k | top_item_1  | ... | top_item_n  |
        |   ...  |       ...   | ... |    ...      |
        ==============================================
        '''
        result = pd.DataFrame(index=res_users,
                              columns=[f'recommand_{count}' for count in range(1, top_n+1)])
        for user in res_users:
            top = list(df_res.loc[user].nlargest(top_n).index)
            count = 1 
            for recommand in top: 
                result[f'recommand_{count}'][user] = recommand
                count += 1
        return result


    def svd_scores(self, items, users, model):    
        '''
        ==============================================
        to calculate each user-item pair's score by svd vectors dot.  
        ==============================================
        >* items
        >* users
        '''
        df_res = pd.DataFrame(columns=items, index=users)
        for user in users:
            for item in items:
                item_vector = self.get_vector_by_item_title(item, model)
                user_vector = self.get_vector_by_user_name(user, model)
                df_res.loc[user][item] = svd_recommand_sys.dot_product(user_vector, item_vector)
        return df_res    

    
    @classmethod
    def dot_product(cls, vector_a, vector_b):
        return vector_a.dot(vector_b)


    def get_vector_by_user_name(self, user_name, trained_model):
        """
        ==============================================
        Returns the latent features of a movie in the form of a numpy array
        ==============================================
        >* user_name: (str)
        >* trained_model: (SVD)
        """
        item_row_idx = trained_model.trainset._raw2inner_id_users[user_name]
        return trained_model.pu[item_row_idx]


    def get_vector_by_item_title(self, item_title, trained_model):
        """
        ==============================================
        Returns the latent features of a movie in the form of a numpy array
        ==============================================
        >* item_title: (str)
        >* trained_model: (SVD)
        """
        item_row_idx = trained_model.trainset._raw2inner_id_items[item_title]
        return trained_model.qi[item_row_idx]


    def svd_recommand(self, df, user_id, item_id, rating_scale, n_factors, test_size=.25, top_n=5):
        '''
            ==============================================
             Training a SVD using Surprise in 4 simple steps:
                Step 1: create a Reader. 
                        A reader tells our SVD what the lower and upper bound of our ratings is.
                        (ex:itemLens ratings are from 1 to 5)
                Step 2: create a new Dataset instance with a DataFrame and the reader. 
                        The DataFrame needs to have 3 columns in this specific order: [user_id, item_id, rating]
                Step 3: keep test_size (ex:25%) of your trainset for testing
                Step 4: train a new SVD with latent_features (ex:100) latent features (number was chosen arbitrarily)
            ==============================================
            >* itemlens_df = 

                  |  user_id  |   item_title   | rating |
                  |-----------|----------------|--------|
            36649 | User 742  |     item_1     | 4      |
            ...   |   ...     |       ...      |...     |
            (pandas.DataFrame)

            >* rating_scale: the scale of rating score.
            >* test_size: the size of your trainset for testing. (float: between 0 to 1)
            >* latent_features: the latent features number SVD(n_factors). defalt is 100. (int)
            >* model_normalize: defalt is True. That means do normalize after training SVD model. (bool) 
        '''
        df[user_id] = df[user_id].astype(str)
        df[item_id] = df[item_id].astype(str)

        reader = Reader(rating_scale=rating_scale)   # Step 1
        data = Dataset.load_from_df(df, reader)  # Step 2
        trainset, testset = train_test_split(data, test_size=test_size)   # Step 3
        model = SVD(n_factors=n_factors)    # Step 4
        model.fit(trainset)

        # RMSE
        predictions = model.test(testset)
        print('RMSE:', accuracy.rmse(predictions))

        # Mapping every vector back to it's item. 
        item_to_row_idx: Dict[any, int] = model.trainset._raw2inner_id_items

        users = list(model.trainset._raw2inner_id_users.keys())
        items = list(model.trainset._raw2inner_id_items.keys())

        df_res = self.svd_scores(items, users, model)

        df_res = df_res.astype(float)
        res_users = list(df_res.index)

        return self.result_in_different_col(df_res, res_users, top_n=top_n) 

 
    @classmethod
    def top_recommand(cls, df, user_title, rating_title, top_n, groupby_title=None):
        '''
        ==============================================
        to recommand top n items by rating.
        ==============================================
        >* df: the pandas DataFrame of user-item rating. it should look like this:
            | user_title | item_title | rating |
            |------------|------------|--------|
            |   user_1   |    item_1  |   r1   |
            |    ...     |     ...    |   ...  |
        >* user_title:  the name of user column.
        >* rating_title: the name of rating column.
        >* top_n: top n to reommand.
        >* groupby_title: the target to goupby. It can be user_title or item_title. None is to recommand top n of all rating. default is None.
        '''
        # recommand top n
        if groupby_title == None: 
            return df.sort_values([rating_title],ascending=False).head(top_n)
        
        # recommand top n for user
        else:
            return df.sort_values([user_title, rating_title],ascending=False).groupby(groupby_title).head(top_n)

 
    
# import sys
# import getopt

# '''
# http://codingpy.com/article/guido-shows-how-to-write-main-function/
# '''

# class Usage(Exception):
#     def __init__(self, msg):
#         self.msg = msg

# def main(argv=None):
#     if argv is None:
#         argv = sys.argv
#     try:
#         try:
#             opts, args = getopt.getopt(argv[1:], "h", ["help"])
#         except getopt.error, msg:
#              raise Usage(msg)
#         # more code, unchanged
#         rs = recommand_system()
#         result = rs.svd_recommand(sys.argv[1:])
#     except Usage:
#         print >>sys.stderr, err.msg
#         print >>sys.stderr, "for help use --help"
#         return 2    
    
    

# if __name__ == '__main__':
#     '''
#     example:
#     sys.argv=[name, df, user_id, item_id, rating_scale, n_factors, test_size, top_n]
#     sys.argv=[name, df_brand_rating, 'group', 'brand', (1,10), 50, .25, 5]
#     '''
#     sys.exit(main(sys.argv))
    
    
    
    
    
    