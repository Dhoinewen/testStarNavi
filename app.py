from flask import Flask, request, jsonify
from models import session, User, Post
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from data import get_all_users, add_new_user, get_all_posts, get_users_posts, find_user, add_new_post, post_delete,\
    get_posts_filter_by_date
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "some-secret"
jwt = JWTManager(app)
api = Api(app)

parser_new_user = reqparse.RequestParser()
parser_new_user.add_argument('nick', type=str)
parser_new_user.add_argument('password', type=str)

parser_new_post = reqparse.RequestParser()
parser_new_post.add_argument('text', type=str)

parser_dates = reqparse.RequestParser()
parser_dates.add_argument('date_from', type=str)
parser_dates.add_argument('date_to', type=str)


class UsersPosts(Resource):
    @jwt_required()
    def get(self, user_id):
        posts = get_users_posts(user_id)
        if posts is None:
            return '', 404
        else:
            return posts

    @jwt_required()
    def post(self, user_id):
        user = find_user(user_id)
        if user is None:
            return '', 404
        else:
            args = parser_new_post.parse_args()
            return add_new_post(user, args['text'])

    @jwt_required()
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


class Posts(Resource):
    def get(self):
        args = parser_dates.parse_args()
        if args['date_from'] and args['date_to'] is not None:
            return get_posts_filter_by_date(datetime.strptime(args['date_from'], '%Y-%m-%d'),
                                            datetime.strptime(args['date_to'], '%Y-%m-%d'))
        else:
            return get_all_posts()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return session.query(User).filter(User.id == identity).one_or_none()


class Login(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = session.query(User).filter(User.nickname == username).first()
        if not user or not user.check_password(password):
            return '', 401
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)


class Register(Resource):
    def post(self):
        args = parser_new_user.parse_args()
        return add_new_user(args['nick'], args['password'])


api.add_resource(UsersPosts, '/users/<user_id>/posts', '/users/<user_id>/posts/<post_id>')
api.add_resource(Users, '/users')
api.add_resource(Posts, '/posts')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')


if __name__ == '__main__':
    app.run(debug=True)
