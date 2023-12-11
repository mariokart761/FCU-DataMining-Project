import os
import pandas as pd
from ast import literal_eval

class SimGameAnalyzer:
    def __init__(self, 
                 sim_app_csv_path = f'{os.path.dirname(os.path.realpath(__file__))}/../data/sim_app_predict.csv', 
                 games_csv_path = f'{os.path.dirname(os.path.realpath(__file__))}/../data/games.csv'):
        self.sim_app_df = pd.read_csv(sim_app_csv_path)
        print(f'[INFO] {sim_app_csv_path}讀取完成')
        self.games_df = pd.read_csv(games_csv_path)
        print(f'[INFO] {games_csv_path}讀取完成')

    def get_sim_app_ids(self, app_id):
        row = self.sim_app_df[self.sim_app_df['app_id'] == app_id]
        if not row.empty:
            sim_app_ids = literal_eval(row['sim_app_list'].values[0])
            return sim_app_ids
        else:
            return None

    def get_sim_games(self, app_id_to_search):
        sim_app_ids = self.get_sim_app_ids(app_id_to_search)
        if sim_app_ids is not None:
            sim_games = pd.merge(pd.DataFrame({'app_id': sim_app_ids}),
                                 self.games_df[['app_id', 'title']], on='app_id', how='left')['title'].tolist()
            return sim_app_ids, sim_games
        else:
            return None

# 使用範例
# sim_game_analyzer = SimGameAnalyzer()
# sim_app_ids, sim_games = sim_game_analyzer.get_sim_games(10)
# print(sim_app_ids)
# print(sim_games)
