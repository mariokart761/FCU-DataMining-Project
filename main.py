from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from modules.sim_user_analyzer import SimUserAnalyzer
from modules.sim_game_analyzer import SimGameAnalyzer
import os
import time

sim_user_analyzer = SimUserAnalyzer()
sim_game_analyzer = SimGameAnalyzer()
app = FastAPI()
app.mount("/static", StaticFiles(directory='dist'), name="static")

# 設定 CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # 設定允許的來源（域名），設為 "*"則允許所有網域
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_html():
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/api/sim_user_analyzer")
async def handle_request(user_id: int = Form(...)):
    try:
        print(f'[INFO] 收到請求，user_id為{user_id}')
        similar_users_ids = sim_user_analyzer.get_similar_users(user_id)
        recommend_game_ids = sim_user_analyzer.get_games_from_sim_user(user_id, similar_users_ids)
        recommend_game_names = sim_user_analyzer.get_game_names(recommend_game_ids)
        print(f'User {user_id} 的推薦遊戲為 {recommend_game_names}')
        ...
        time.sleep(1) # Response Delay
        return {"recommend_game_ids": recommend_game_ids, "recommend_game_names": recommend_game_names}
    
    except Exception as e:
        return {'error': str(e)}

@app.post("/api/sim_game_analyzer")
async def handle_request(game_id: int = Form(...)):
    try:
        sim_game_analyzer = SimGameAnalyzer()
        sim_app_ids, sim_game_names = sim_game_analyzer.get_sim_games(game_id)
        print(f'Game {game_id} 的相似遊戲為 {sim_game_names}')
        ...
        time.sleep(1) # Response Delay
        return {"sim_app_ids": sim_app_ids, "sim_game_names": sim_game_names}
    
    except Exception as e:
        return {'error': str(e)}

favicon_path = 'favicon.ico'
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

rootPath = os.path.dirname(__file__)

if __name__ == '__main__':
    os.system(f'python -m uvicorn main:app --port 8000 --reload')