import copy
import json
import random
from collections import Counter
from os.path import *

from flask import Flask, redirect, request, jsonify

from wiredwolf.snow_flake import SnowFlake
from wiredwolf.lru_dic import LruDic

folder=abspath(join(dirname(__file__), '..'))
app = Flask(__name__, static_url_path='/', static_folder=folder)

snow = SnowFlake()
games = LruDic(timeout=5 * 3600)  # 如果两个小时没有碰游戏，则删除游戏


@app.route("/")
def haha():
    return redirect('index.html')


def get_user():
    return request.cookies['userid']


@app.route("/api/create_room", methods=['POST'])
def create_room():
    form = json.loads(request.get_data(as_text=True))['game']
    for i in form:
        form[i] = int(form[i])
    room = str(snow.get_id())
    user = get_user()
    games.set(room, {
        'info': form,  # 房间信息
        'manager': user,  # 房主信息
        'room': room,
        'turn': 1,  # 当前是第几局游戏
        'people': {},  # 每个人的角色映射
    })
    return jsonify(games.get(room))


@app.route("/api/newgame")
def new_game():
    # 房主点击新开一局
    user = request.cookies['userid']
    room = request.args['room']
    game = games.get(room)
    assert game['manager'] == user
    game['turn'] += 1
    game['people'] = {}
    game['fetched'] = 0
    return jsonify(game)


def get_role(game):
    info = game['info']
    c = Counter(game['people'].values())
    left = []
    for k, v in info.items():
        assert v - c.get(k, 0) >= 0
        left.extend([k] * (v - c.get(k, 0)))
    role = random.choice(left)
    return role


@app.route("/api/test")
def test():
    return 'good'


@app.route("/api/fetch")
def fetch_info():
    # 用户获取房间信息
    room = request.args['room']
    user = get_user()
    game = games.get(room)
    if user not in game['people'] and user != game['manager']:
        game['people'][user] = get_role(game)
    game = copy.deepcopy(game)
    game['fetched'] = len(game['people'])
    if user != game['manager']:
        # 如果不是管理员，只返回一个角色
        role = game['people'][user]
        game['people'] = {
            user: role,
        }
    return jsonify(game)


if __name__ == '__main__':
    app.run(port=9876, debug=False, host='0.0.0.0')
