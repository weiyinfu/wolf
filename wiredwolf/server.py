import copy
import json
import random
from os.path import *

from flask import Flask, redirect, request, jsonify, make_response

from wiredwolf.snow_flake import SnowFlake

app = Flask(__name__, static_url_path='/', static_folder=join(dirname(__file__), '..'))

snow = SnowFlake()
games = {}


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
    games[room] = {
        'info': form,  # 房间信息
        'manager': user,  # 房主信息
        'room': room,
        'turn': 1,
        'people': {},  # 每个人的角色映射
    }
    return jsonify(games[room])


@app.route("/api/newgame")
def new_game():
    # 房主点击新开一局
    user = request.cookies['userid']
    room = request.args['room']
    game = games[room]
    assert game['manager'] == user
    game['turn'] += 1
    game['people'] = {}
    game['fetched'] = 0
    return jsonify(game)


def get_role(game):
    info = copy.deepcopy(game['info'])
    for k in game['people'].values():
        info[k] -= 1
        assert info[k] >= 0
    left = []
    for k, v in info.items():
        for j in range(v):
            left.append(k)
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
    game = games[room]
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
    app.run(port=9876, debug=True, host='0.0.0.0')
