from random import randrange
from time import sleep

from vk import Session, API

from app import db
from app.models import Like, Group


API_VERSION = 5.103
POST_TYPE = 'post'
LIKE_SLEEP_MIN = 1
LIKE_SLEEP_MAX = 5
MAX_POSTS_PER_REQUEST = 100
DEFAULT_POST_COUNT = 146


def delete_group_by_id(db_id):
    group = Group.query.filter_by(id=int(db_id)).first()
    if group:
        db.session.delete(group)
        db.session.commit()


class Bot:
    def __init__(self, token):
        self.token = token
        self.session = Session(access_token=self.token)
        self.api = API(self.session)

    def like(self, item_id, group, item_type=POST_TYPE):
        sleep(randrange(LIKE_SLEEP_MIN, LIKE_SLEEP_MAX+1))
        total_liked = self.api.likes.add(v=API_VERSION,
                                         type=item_type,
                                         item_id=item_id,
                                         owner_id=group.item_id)
        if not Like.query.filter_by(item_id=item_id,
                                     item_owner_id=group.id,
                                     item_owner=group).first():
            like = Like(item_id=item_id,
                        item_owner_id=group.id,
                        item_owner=group)
            db.session.add(like)
            db.session.commit()

        return total_liked

    def unlike(self, like, item_type=POST_TYPE):
        sleep(randrange(LIKE_SLEEP_MIN, LIKE_SLEEP_MAX+1))
        total_unliked = self.api.likes.delete(v=API_VERSION,
                                              type=item_type,
                                              item_id=like.item_id,
                                              owner_id=like.item_owner.item_id)
        db.session.delete(like)
        db.session.commit()

        return total_unliked

    def get_group_posts(self, owner_id, count=DEFAULT_POST_COUNT):
        result = []
        got_posts = 0
        while got_posts != count:
            new_posts = min(count - got_posts, MAX_POSTS_PER_REQUEST)
            result.extend(self.api.wall.get(v=API_VERSION, owner_id=owner_id, count=new_posts)['items'])
            got_posts += new_posts
        return result

    def process_group(self, group_id, count):
        posts = self.get_group_posts(group_id, count)

        if not Group.query.filter_by(item_id=group_id).first():
            group = Group(item_id=group_id)
            db.session.add(group)
            db.session.commit()

        current_group = Group.query.filter_by(item_id=group_id).first()
        for post in posts:
            self.like(post['id'], current_group)

    def unprocess_group(self, group_id, count):
        group = Group.query.filter_by(item_id=group_id).first()
        if group:
            likes = group.likes.all()[:count] if count > 0 else group.likes.all()
            for like in likes:
                self.unlike(like)

            if len(group.likes.all()) == 0:
                delete_group_by_id(group.id)
