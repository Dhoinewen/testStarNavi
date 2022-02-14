from models import session, User, Post


def get_posts_filter_by_date(date_from, date_to):
    posts_list = []
    posts = session.query(Post).filter(Post.time_created.between(date_from, date_to)).all()
    for post in posts:
        time = post.time_created
        sample = {'id': post.id,
                  'text': post.text,
                  'creator': post.creator,
                  'created data': time.strftime("%d/%m/%Y, %H:%M:%S"),
                  'liked by': post.liked
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


def get_users_posts(user_id):
    posts_list = []
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    else:
        for post in user.posts:
            time = post.time_created
            sample = {'id': post.id,
                      'text': post.text,
                      'creator': post.creator,
                      'created data': time.strftime("%d/%m/%Y, %H:%M:%S"),
                      'liked by': post.liked
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
                  'liked by': post.liked
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
              'likes': user.likes
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
                      'likes': user.likes
                      }
            user_list.append(sample)
    return user_list
