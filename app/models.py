from app import db


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)
    item_owner_id = db.Column(db.Integer, db.ForeignKey('group.id', ondelete='CASCADE'))
    item_owner = db.relationship('Group', backref='likes', lazy=True)

    def __repr__(self):
        return f'Like({self.item_id}, {self.item_owner_id})'


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Group({self.item_id})'
