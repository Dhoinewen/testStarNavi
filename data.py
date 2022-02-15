from models import session, User, Post, Like


def get_likes_filter_by_date(date_from, date_to):
    likes_list = []
    likes = session.query(Like).filter(Like.time_created.between(date_from, date_to)).all()
    for like in likes:
        time = like.time_created
        sample = {'id': like.id,
                  'liked_by': like.liked_by,
                  'liked_post': like.liked_post,
                  'created data': time.strftime("%d/%m/%Y, %H:%M:%S"),
                  }
        likes_list.append(sample)
    return likes_list


def get_all_likes():
    likes_list = []
    likes = session.query(Like).all()
    for like in likes:
        time = like.time_created
        sample = {'id': like.id,
                  'liked_by': like.liked_by,
                  'liked_post': like.liked_post,
                  'created data': time.strftime("%d/%m/%Y, %H:%M:%S"),

                  }
        likes_list.append(sample)
    return likes_list

def like_post(user, post_id):
    like = Like(liked_by=user.id, liked_post=post_id)
    session.add(like)
    session.commit()


def unlike_post(user, post_id):
    session.query(Like).filter(Like.liked_by == user.id or Like.liked_post == post_id).delete()
    session.commit()


def get_posts_filter_by_date(date_from, date_to):
    posts_list = []
    posts = session.query(Post).filter(Post.time_created.between(date_from, date_to)).all()
    for post in posts:
        time = post.time_created
        sample = {'id': post.id,
                  'text': post.text,
                  'creator': post.creator,
                  'created data': time.strftime("%d/%m/%Y, %H:%M:%S"),
                  'liked by': f'{post.liked}'
                  }
        posts_list.append(sample)
    return posts_list


def post_delete(post_id):
    session.query(Post).filter(Post.id == post_id).delete()
    session.commit()


def find_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    else:
        return user


def add_new_post(user, text):
    post = Post(text=text, creator=user.id)
    session.add(post)
    session.commit()


def get_users_posts(user):
    posts_list = []
    if user is None:
        return None
    else:
        for post in user.posts:
            time = post.time_created
            sample = {'id': post.id,
                      'text': post.text,
                      'creator': post.creator,
                      'created data': time.strftime("%d/%m/%Y, %H:%M:%S"),
                      'liked by': f'{post.liked}'
                      }
            posts_list.append(sample)
    return posts_list


def get_all_posts():
    posts_list = []
    posts = session.query(Post).all()
    for post in posts:
        time = post.time_created
        sample = {'id': post.id,
                  'text': post.text,
                  'creator': post.creator,
                  'created data': time.strftime("%d/%m/%Y, %H:%M:%S"),
                  'liked by': f'{post.liked}'
                  }
        posts_list.append(sample)
    return posts_list


def add_new_user(nick, password):
    user = User(nickname=nick, password=password)
    session.add(user)
    session.commit()
    sample = {'id': user.id,
              'nick': user.nickname,
              'posts': len(user.posts),
              'likes': f'{user.likes}'
              }
    return sample


def get_all_users():
    user_list = []
    users = session.query(User).all()
    if users is None:
        return None
    else:
        for user in users:
            sample = {'id': user.id,
                      'nick': user.nickname,
                      'posts': len(user.posts),
                      'likes': f'{user.likes}'
                      }
            user_list.append(sample)
    return user_list
