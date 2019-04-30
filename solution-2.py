from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify, make_response
from DBManager import *


app = Flask(__name__)
api = Api(app)
db = DB()

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('user_id', required=True, type=int)

parser_put = reqparse.RequestParser()
parser_put.add_argument('part', required=True)
parser_put.add_argument('text', required=True)

parser_new_user = reqparse.RequestParser()
parser_new_user.add_argument('login', required=True)
parser_new_user.add_argument('password', required=True)


def abort_if_news_not_found(news_id, data_base):
    if not data_base.get(news_id):
        abort(404, message="News {} not found".format(news_id))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class News(Resource):
    def get(self, news_id):
        news = NewsModel(db.get_connection())
        abort_if_news_not_found(news_id, news)
        return jsonify({'news': news.get(news_id)})

    def delete(self, news_id):
        news = NewsModel(db.get_connection())
        abort_if_news_not_found(news_id, news)
        news.delete(news_id)
        return jsonify({'success': 'OK'})
    
    def put(self, news_id):
        news = NewsModel(db.get_connection())
        abort_if_news_not_found(news_id, news)
        args = parser_put.parse_args()
        news.update(news_id, args['part'], args['text'])
        return jsonify({'success': 'OK'})        


class NewsList(Resource):
    def get(self):
        news = NewsModel(db.get_connection()).get_all()
        return jsonify({'news': news})

    def post(self):
        args = parser.parse_args()
        NewsModel(db.get_connection()).insert(args['title'], args['content'], args['user_id'])
        return jsonify({'success': 'OK'})
    
    
class User(Resource):
    def get(self, user_id):
        user = UserModel(db.get_connection())
        abort_if_news_not_found(user_id, user)
        return jsonify({'users': user.get(user_id)})

    def delete(self, user_id):
        user = UserModel(db.get_connection())
        abort_if_news_not_found(user_id, user)
        user.delete(user_id)
        return jsonify({'success': 'OK'})
    
    def put(self, user_id):
        user = UserModel(db.get_connection())
        abort_if_news_not_found(user_id, user)
        args = parser_put.parse_args()
        user.update(user_id, args['part'], args['text'])
        return jsonify({'success': 'OK'})        


class UserList(Resource):
    def get(self):
        user = UserModel(db.get_connection()).get_all()
        return jsonify({'users': user})

    def post(self):
        args = parser_new_user.parse_args()
        UserModel(db.get_connection()).insert(args['login'], args['password'])
        return jsonify({'success': 'OK'})


if __name__ == '__main__':
    api.add_resource(NewsList, '/news')
    api.add_resource(News, '/news/<int:news_id>')
    api.add_resource(UserList, '/users')
    api.add_resource(User, '/users/<int:user_id>')    
    app.run(port=8080, host='127.0.0.1')
