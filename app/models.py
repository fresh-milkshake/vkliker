from app import db


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)
    item_owner_id = db.Column(db.Integer, db.ForeignKey('group.id', ondelete='CASCADE'))
    item_owner = db.relationship('Group', backref=db.backref('likes', lazy='dynamic'))

    def __str__(self):
        return f'{self.item_id}, {self.item_owner_id}'


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'{self.item_id}'
