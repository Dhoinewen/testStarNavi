from flask import Flask
from flask_restful import Api, Resource, reqparse
from data import get_all_users, add_new_user, get_all_posts, get_users_posts, find_user, add_new_post


app = Flask(__name__)
api = Api(app)
parser_new_user = reqparse.RequestParser()
parser_new_user.add_argument('nick', type=str)

parser_new_post = reqparse.RequestParser()
parser_new_post.add_argument('text', type=str)


class UsersPosts(Resource):
    def get(self, user_id):
        posts = get_users_posts(user_id)
        if posts is None:
            return '', 404
        else:
            return posts

    def post(self, user_id):
        user = find_user(user_id)
        if user is None:
            return '', 404
        else:
            args = parser_new_post.parse_args()
            return add_new_post(user, args['text'])


class Users(Resource):
    def get(self):
        users = get_all_users()
        if users is None:
            return '', 404
        else:
            return users

    def post(self):
        args = parser_new_user.parse_args()
        return add_new_user(args['nick'])


class Posts(Resource):
    def get(self):
        return get_all_posts()

api.add_resource(UsersPosts, '/users/<user_id>/posts')
api.add_resource(Users, '/users')


if __name__ == '__main__':
    app.run(debug=True)
