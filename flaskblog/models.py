from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db,login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer,
        primary_key = True)
    
    username = db.Column(db.String(20),
        unique = True,
        nullable = False)
    
    email = db.Column(db.String(50),
        unique = True,
        nullable = False)

    user_image = db.Column(db.String(20),
        nullable = False,
        default = 'default.jpg')
    
    password = db.Column(db.String(50),
        nullable = False)

    # about = db.Column(db.String(50),
    #     nullable = False) 

    posts = db.relationship("Post",
        backref= "author",
        lazy = True)


    def get_reset_token(self,expire_sec = 900):
        s = Serializer(current_app.config["SECRET_KEY"],expire_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")
    
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']    
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User ({self.id} ,{self.username} ,{self.email} ,{self.user_image})"

class Post(db.Model,UserMixin):

    id = db.Column(db.Integer,
    primary_key = True)
    
    title = db.Column(db.String(50),
        nullable = False)

    date_posted = db.Column(db.DateTime,
        nullable = False,
        default = datetime.now)
    
    content = db.Column(db.Text,
        nullable = False)

    long_post = db.Column(db.Boolean,
        nullable = False)

    user_id = db.Column(db.Integer,
        db.ForeignKey('user.id'),
        nullable = False)

    def __repr___(self):
        return f"Post({self.id},{self.title},{self.date_posted})"