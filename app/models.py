from app import db


class Tournament(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return '<Tournament(name={})>'.format(self.name)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'uid': self.uid,
            'name': self.name
        }


class Team(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    flag = db.Column(db.String(128))

    def __repr__(self):
        return '<Team(name={})>'.format(self.name)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'flag': self.flag
        }
