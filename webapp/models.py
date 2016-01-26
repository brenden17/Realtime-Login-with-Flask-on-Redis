from datetime import datetime

from sqlalchemy import event
from mongoengine import signals

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager, UserMixin


db = SQLAlchemy()
mongo = MongoEngine()
login_manager = LoginManager()

class QueryableMixin(object):
    @classmethod
    def all(cls, **kwargs):
        if cls._is_sql():
            return cls.get_by_sql(**kwargs)
        return cls.get_by_nosql(**kwargs)

    @classmethod
    def get(cls, **kwargs):
        if cls._is_sql():
            return cls.query.filter(**kwargs)
        return cls.objects(**kwargs).first()

    @classmethod
    def get_by_sql(cls, **kwargs):
        return cls.query.all()
    
    @classmethod
    def get_by_nosql(cls, **kwargs):
        return cls.objects.all()

    @classmethod
    def _is_sql(cls):
        if cls.__class__.__base__.__name__ == 'DeclarativeMeta':
            return True
        return False

    def _is_sql_self(self):
        if self.__class__.__base__.__name__ == 'Document':
            return False
        return True

    def save(self):
        if self._is_sql_self():
            db.session.add(self)
            db.session.commit()

    def delete(self):
        if self._is_sql_self():
            db.session.delete(self)
            db.session.commit()


class User(db.Model, UserMixin, QueryableMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def __str__(self):
        return '<User %r>' % (self.username)

    def get_friends(self):
        friend = Friend.objects(my_id=self.id).first()
        if friend:
            return friend.names
        return None

    def add_friend(self, username):
        friend = Friend.objects(my_id=self.id).first()
        if not username in friend.names:
            friend.update(push__names=username)
            return True
        return False

    def save(self):
        super(User, self).save()
        Friend(my_id=self.id).save()
        
    def delete(self):
        friend = Friend.objects(my_id=self.id).first()
        if friend:
            friend.delete()
        super(User, self).delete()
        

class Friend(mongo.Document, QueryableMixin):
    my_id = mongo.IntField(required=True, unique=True)
    names = mongo.ListField(mongo.StringField(max_length=255))

    def __repr__(self):
        return '<Friend {}, {}>'.format(self.my_id, self.names)

    def __str__(self):
        return '<Friend {}, {}>'.format(self.my_id, self.names)