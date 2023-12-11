import pandas as pd
import ast
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import coo_matrix
import random
import os
import json

# Example code from https://www.kaggle.com/code/thakursankalp/steam-game-recommendation-engine

class DataProcessor:
    def __init__(self, main_data_path=f'{os.path.dirname(os.path.realpath(__file__))}/../data/filtered_main_data.csv',
                 user_game_data_path=f'{os.path.dirname(os.path.realpath(__file__))}/../data/filtered_user_game.json',
                 games_csv_path = f'{os.path.dirname(os.path.realpath(__file__))}/../data/games.csv'):
        self.main_data_path = main_data_path
        self.user_game_data_path = user_game_data_path
        self.games_csv_path = games_csv_path
        self.main_data_df, self.user_game_data_df, self.games_df = self.load_data()
        self.user_ids = self.get_user_ids()
        self.item_ids = self.get_item_ids()
        self.unique_user_ids = self.get_unique_user_ids()
        self.user_item_matrix = self.get_user_item_matrix()
        self.model_knn = self.get_model_knn()
        
    # def reduce_reading_memory(self, df):
    #     for col in df.columns:
    #         if df[col].dtype == 'float64':
    #             df[col] = df[col].astype('float32')
    #         if df[col].dtype == 'int64':
    #             df[col] = df[col].astype('int32')
    #     return df

    def load_data(self):
        # 讀取filtered_main_data.csv
        # main_data_df = self.reduce_reading_memory(pd.read_csv(self.main_data_path))
        main_data_df = pd.read_csv(self.main_data_path)
        print(f'[INFO] {self.main_data_path}讀取完成')
        # 讀取filtered_user_game.csv
        with open(self.user_game_data_path, 'r') as json_file:
            data = json.load(json_file)
        user_game_data_df = pd.json_normalize(data['user_games'])
        user_game_data_df['user_id'] = user_game_data_df['user_id'].astype('int64')
        print(type(user_game_data_df['user_id'][0]))
        print(type(user_game_data_df['app_id'][0]))
        print(f'[INFO] {self.user_game_data_path}讀取完成')
        # # 讀取games.csv
        games_df = pd.read_csv(self.games_csv_path)
        print(f'[INFO] {self.games_csv_path}讀取完成')
        return main_data_df, user_game_data_df,games_df

    def get_user_ids(self):
        user_ids = self.main_data_df['user_id'].astype('category').cat.codes
        return user_ids

    def get_item_ids(self):
        item_ids = self.main_data_df['app_id'].astype('category').cat.codes
        return item_ids

    def get_unique_user_ids(self):
        unique_user_ids = self.main_data_df['user_id'].astype('category').cat.categories
        return unique_user_ids

    def get_unique_item_ids(self):
        unique_item_ids = self.main_data_df['app_id'].astype('category').cat.categories
        return unique_item_ids

    def get_user_item_matrix(self, weight_attr='hours'):
        user_item_matrix = coo_matrix((self.main_data_df[weight_attr], (self.user_ids, self.item_ids)))
        return user_item_matrix
    
    def get_model_knn(self):
        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(self.user_item_matrix)
        return model_knn
    

class SimUserAnalyzer:
    def __init__(self, data_processor = DataProcessor()):
        self.data_processor = data_processor

    def get_similar_users(self, user_id, n_neighbors=11):
        unique_user_ids = self.data_processor.unique_user_ids
        user_item_matrix = self.data_processor.user_item_matrix
        model_knn = self.data_processor.model_knn
        distances, indices = model_knn.kneighbors(user_item_matrix.getrow(user_id), n_neighbors=n_neighbors)
        similar_users_ids = [unique_user_ids[i] for i in indices.flatten()[1:]]
        return similar_users_ids
    
    def get_games_from_sim_user(self, user_id, similar_users_ids, count_limit = 10):
        # "相似使用者的遊戲的聯集"中去除"自己擁有的遊戲"，再從中抽選10筆(若小於10筆則有n筆列出n筆)
        
        # 找出 list 中所有user的遊戲的聯集
        df = self.data_processor.user_game_data_df
        union_of_similar_user_games = set()
        for user_id in similar_users_ids:
            games = set(df[df['user_id'] == user_id]['app_id'].iloc[0])
            union_of_similar_user_games.update(games)

        # input user_id擁有的遊戲set
        input_user_game_ids = set(df[df['user_id'] == user_id]['app_id'].iloc[0])

        # 從聯集中移除使用者 A 擁有的遊戲的 ID，並轉換為list
        recommend_game_set = union_of_similar_user_games - input_user_game_ids
        recommend_game_list = list(recommend_game_set)

        # # 若商品數量>count_limit項，則隨機選出count_limit項
        if len(recommend_game_list) > count_limit:
            recommend_game_list = random.sample(recommend_game_list, k=count_limit)
        
        return recommend_game_list
    
    def get_game_names(self, app_ids):
        if app_ids is not None:
            game_names = pd.merge(pd.DataFrame({'app_id': app_ids}),
                                 self.data_processor.games_df[['app_id', 'title']], on='app_id', how='left')['title'].tolist()
            return game_names
        else:
            return None
        
# 使用範例
# sim_user_analyzer = SimUserAnalyzer()
# user_id_to_find_similar = 0 
# similar_users_ids = sim_user_analyzer.get_similar_users(user_id_to_find_similar)
# print(similar_users_ids)
# recommend_game_list = sim_user_analyzer.get_games_from_sim_user(user_id_to_find_similar, similar_users_ids)
# print(recommend_game_list)
# get_game_names = sim_user_analyzer.get_game_names(recommend_game_list)
# print(get_game_names)