from random import randrange
from time import sleep

from vk import Session, API

from app import db
from app.models import Like, Group


def delete_group_by_id(db_id):
    print('deleting group with id', db_id)
    group = Group.query.filter_by(id=int(db_id)).first()
    try:
        for ilike in group.likes.all():
            db.session.delete(ilike)
    except Exception:
        pass
    db.session.delete(group)
    db.session.commit()


class Bot:
    def __init__(self, token):
        self.token = token

        self.session = Session(access_token=self.token)
        self.api = API(self.session)

    def like(self, item_id, group, item_type='post'):

        if randrange(0, 10) == 4:
            sleep(5)
        sleep(1)
        total_liked = self.api.likes.add(v=5.103,
                                         type=item_type,
                                         item_id=item_id,
                                         owner_id=group.item_id)

        duplicate = Like.query.filter_by(item_id=item_id,
                                         item_owner_id=group.id,
                                         item_owner=group).first()
        if not duplicate:
            like = Like(item_id=item_id,
                        item_owner_id=group.id,
                        item_owner=group)
            db.session.add(like)
            db.session.commit()

        return total_liked

    def unlike(self, like, item_type='post'):
        if randrange(0, 10) == 4:
            sleep(1)
        sleep(1)
        total_liked = self.api.likes.delete(v=5.103,
                                            type=item_type,
                                            item_id=like.item_id,
                                            owner_id=like.item_owner.item_id)
        db.session.delete(like)
        db.session.commit()

        return total_liked

    def get_group_posts(self, owner_id, count=146):
        result = []
        got_posts = 0
        while got_posts != count:
            new_posts = count - got_posts if count - got_posts < 100 else 100
            result.extend(self.api.wall.get(v=5.103, owner_id=owner_id, count=new_posts)['items'])
            got_posts += new_posts
        print(got_posts)
        return result

    def process_group(self, group_id, count):
        posts = self.get_group_posts(group_id, count)

        duplicate = Group.query.filter_by(item_id=group_id).first()
        if not duplicate:
            group = Group(item_id=group_id)
            db.session.add(group)
            db.session.commit()

        current_group = Group.query.filter_by(item_id=group_id).first()
        for post in posts:
            self.like(post['id'], current_group)

    def unprocess_group(self, group_id, count):
        group = Group.query.filter_by(item_id=group_id).first()
        likes = list(group.likes.all())

        if count == 0:
            for like in likes:
                self.unlike(like)
        elif count >= 1:
            for like in likes[0:count]:
                self.unlike(like)

        if len(group.likes.all()) == 0:
            delete_group_by_id(group.id)
