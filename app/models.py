from app import db


class Tournament(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return '<Tournament(name={})>'.format(self.name)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.uid,
            'name': self.name
        }
