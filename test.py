from gevent import monkey

monkey.patch_all()

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json, atexit, time
import subprocess

USERS_PATH = 'data/users.json'
ITEMS_PATH = 'data/items.json'
TRANSACTIONS_PATH = 'data/transactions.json'
DEBUG = False

app = Flask(__name__)
app.config.from_object(__name__)

sio = SocketIO(app, cors_allowed_origins='http://localhost:8080')

CORS(app, resources={r'/*': {'origins': 'http://localhost:8080'}})


def send_code(barcode):
    sio.emit('codeScanned', barcode)


@app.route('/cdp', methods=['POST'])
def post_cdp():
    return 'CDP updated!'


@app.route('/screensaver', methods=['POST'])
def post_screensaver():
    subprocess.run(["xscreensaver-command -activate"], shell=True)
    return 'Screensaver started!'


@app.route('/<path:path>')
def get_data(path):
    segments = path.split('/')
    if segments[0] == 'users':
        result = users
    elif segments[0] == 'items':
        result = items
    elif segments[0] == 'transactions':
        result = transactions
    else:
        return 'Invalid path!'
    segments.pop(0)
    for segment in segments:
        if segment in result:
            result = result[segment]
        elif type(result) == list and segment.isdigit() and len(result) > int(segment):
            result = result[int(segment)]
        else:
            return 'Invalid path!'
    return jsonify(result)


@app.route('/transactions/add', methods=['POST'])
def post_transactions_add():
    transaction = request.json
    transaction['date'] = time.strftime('%d.%m.%Y, %H:%M:%S')

    user_index = None
    for index, user in enumerate(users['users']):
        if user['id'] == transaction['user']['id']:
            user_index = index
            break
    if user_index is None:
        return 'Invalid user ID!'

    transactions.append(transaction)
    users['users'][user_index]['balance'] += transaction['impact']

    save_json(transactions, TRANSACTIONS_PATH)
    save_json(users, USERS_PATH)
    return 'Transaction received!'


@app.route('/transactions/undo', methods=['POST'])
def post_transactions_undo():
    date = request.json['date']

    transaction_index = None
    for index, t in enumerate(transactions):
        if t['date'] == date:
            transaction_index = index
            break
    if transaction_index is None:
        return 'Invalid transaction date!'

    transaction = transactions[transaction_index]

    user_index = None
    for index, user in enumerate(users['users']):
        if user['id'] == transaction['user']['id']:
            user_index = index
            break
    if user_index is None:
        return 'Transaction user could not be found!'

    users['users'][user_index]['balance'] -= transaction['impact']
    transactions.pop(transaction_index)
    save_json(transactions, TRANSACTIONS_PATH)
    save_json(users, USERS_PATH)
    return 'Transaction undone!'


@app.route('/favorites/add', methods=['POST'])
def post_favorites_add():
    favorite = request.json
    id = favorite['id']
    barcode = favorite['barcode']

    users['users'][id]['favorites'].append(barcode)

    save_json(users, USERS_PATH)
    return 'Favorite added!'


@app.route('/favorites/remove', methods=['POST'])
def post_favorites_remove():
    favorite = request.json
    id = favorite['id']
    barcode = favorite['barcode']

    users['users'][id]['favorites'].remove(barcode)

    save_json(users, USERS_PATH)
    return 'Favorite removed!'


def load_json(path):
    with open(path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def save_json(data_to_save, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)


def load_data():
    global users, items, transactions
    users = load_json(USERS_PATH)
    items = load_json(ITEMS_PATH)
    transactions = load_json(TRANSACTIONS_PATH)


def save_data():
    save_json(users, USERS_PATH)
    save_json(items, ITEMS_PATH)
    save_json(transactions, TRANSACTIONS_PATH)


def run():
    load_data()

    atexit.register(save_data)

    # app.run(host='0.0.0.0')
    sio.run(app, host='0.0.0.0')


if __name__ == '__main__':
    run()
