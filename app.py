from flask import Flask
from flask_restful import Api, Resource, reqparse
from datetime import date, datetime
from data import get_all_users, add_new_user, get_all_posts, get_users_posts, find_user, add_new_post, post_delete,\
    get_posts_filter_by_date


app = Flask(__name__)
api = Api(app)
parser_new_user = reqparse.RequestParser()
parser_new_user.add_argument('nick', type=str)

parser_new_post = reqparse.RequestParser()
parser_new_post.add_argument('text', type=str)

parser_dates = reqparse.RequestParser()
parser_dates.add_argument('date_from', type=str)
parser_dates.add_argument('date_to', type=str)


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

    def delete(self, user_id, post_id):
        post_delete(post_id)
        return '', 204


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
        args = parser_dates.parse_args()
        if args['date_from'] and args['date_to'] is not None:
            return get_posts_filter_by_date(datetime.strptime(args['date_from'], '%Y-%m-%d'),
                                            datetime.strptime(args['date_to'], '%Y-%m-%d'))
        else:
            return get_all_posts()


api.add_resource(UsersPosts, '/users/<user_id>/posts', '/users/<user_id>/posts/<post_id>')
api.add_resource(Users, '/users')
api.add_resource(Posts, '/posts')


if __name__ == '__main__':
    app.run(debug=True)
