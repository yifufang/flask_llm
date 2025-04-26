from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Messages(db.Model):
    """ 聊天记录 """
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'recipient': self.recipient,
            'content': self.content,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }
    

class BabySettings(db.Model):
    """ 宝宝的设定 """
    __tablename__ = 'baby_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    birthdate = db.Column(db.DateTime, nullable=True)
    hobbies = db.Column(db.String(200), nullable=True)
    history = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'birthdate': self.birthdate.strftime('%Y-%m-%d') if self.birthdate else None,
            'hobbies': self.hobbies,
            'history': self.history
        }
    

class Summary(db.Model):
    """ AI聊天总结 """
    __tablename__ = 'summary'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    summary = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'summary': self.summary,    
            'updated_at': self.updated_at       
        }
    


