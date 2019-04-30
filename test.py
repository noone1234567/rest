# импортируем библиотеки
from flask import Flask, request
import requests
import logging
import chess
import random
from PIL import Image
import json


app = Flask(__name__)
board = chess.Board()


logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи библиотеки json
    # преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    # Отправляем request.json и response в функцию handle_dialog.
    # Она сформирует оставшиеся поля JSON, которые отвечают
    # непосредственно за ведение диалога
    handle_dialog(request.json, response)

    logging.info('Response: %r', request.json)

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    global board
    if req['session']['new']:
        board = chess.Board()
        sessionStorage[user_id] = {'suggests': ["Помощь", "Посмотреть поле"]}
    res['response']['buttons'] = get_suggests(user_id)

    if board.is_game_over():
        res['response']['text'] = 'Вы выиграли. Хотеите играть снова?'
        sessionStorage[user_id] = {'suggests': [
            "Нет",
            "Да"]}
        if req['request']['original_utterance'].lower() == 'нет':
            res['response']['end_session'] = True
        else:
            res['response']['text'] = 'Отлично, сыграем ещё раз!'
            board = chess.Board()
        return

    res['response']['text'] = 'Ваш ход'
    a = req['request']['original_utterance']
    if not a:
        return

    if a.lower() == 'помощь':
        res['response']['text'] = 'Это игра в шахматы. Почти. Во время вашего хода вы вводите значение вида "e2e4" ' \
                                  'Чтобы сходить фигурой с клетки e2 на клетку e4. Затем в мой ход я делаю тоже самое.'\
                                  'Также вы можете посмотреть всё поле.'
        return

    elif a.lower() == 'посмотреть поле':
        chess_pieces = list(map(lambda x: x.split(), str(board).replace('.', '  .  ').split('\n')))
        r = requests.get('https://github.com/noone1234567/alisa_project/blob/master/chess.jpg?raw=true')
        with open('picture.png', 'wb') as file:
            file.write(r.content)
        img = Image.open('picture.png').convert("RGB")

        r = requests.get('https://github.com/noone1234567/alisa_project/blob/master/all_chess.png?raw=true')
        with open('picture1.png', 'wb') as file:
            file.write(r.content)
        img1 = Image.open('picture1.png')
        chess_dict = {'r': [0, 0], 'n': [1, 0], 'b': [2, 0], 'q': [3, 0], 'k': [4, 0], 'p': [1, 1],
                      'R': [0, 3], 'N': [1, 3], 'B': [2, 3], 'Q': [3, 3], 'K': [4, 3], 'P': [1, 2]}
        for i in range(8):
            for j in range(8):
                if chess_pieces[j][i] in chess_dict:
                    x = 90 + chess_dict[chess_pieces[j][i]][0] * 200
                    y = 90 + chess_dict[chess_pieces[j][i]][1] * 200
                    area = (x, y, x + 200, y + 200)
                    cropped_img = img1.crop(area)
                    cropped_img.thumbnail((77, 77), Image.ANTIALIAS)
                    r, g, b, a = cropped_img.split()
                    top = Image.merge("RGB", (r, g, b))
                    mask = Image.merge("L", (a,))
                    img.paste(top, (18 + 77*i, 18 + 77*j, 18 + 77*(i + 1), 18 + 77*(j + 1)),  mask)


        img.save("new_chess.png")
        response = requests.get("https://www.pythonanywhere.com/user/alwin123/files/home/alwin123/new_chess.png&format=json")
        res['response']['text'] = response.json()
        '''res['response']['card'] = {"type": "BigImage",
                                   "image_id": need,
                                   "title": "Поле",
                                   "description": "шахматы",
                                   "button": {"text": "незнаю",
                                              "url": "https://www.pythonanywhere.com/user/alwin123/files/home/alwin123/new_chess.png",
                                              "payload": {}
                                             }
                                    }'''

    try:
        mymv = chess.Move.from_uci(a)
        board.push_san(board.san(mymv))

        b = board.legal_moves
        mv = chess.Move.from_uci(str(random.choice(list(b))))
        board.push_san(board.san(mv))
        res['response']['text'] = str(mv)
    except Exception as e:
        res['response']['text'] = str(e)
        return

# Функция возвращает подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем подсказки из массива.
    suggests = [{'title': suggest, 'hide': True}
                for suggest in session['suggests']]

    return suggests


if __name__ == '__main__':
    app.run()
