import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

"""Models for Blogly."""
default_img_url = "https://cdn.vectorstock.com/i/preview-1x/61/88/user-icon-human-person-symbol-avatar-login-sign-vector-28996188.jpg"

class User(db.Model):
    """User."""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=True)
    image_url = db.Column(db.String,
                          nullable=False)

    # Add the 'cascade' option to automatically delete associated posts
    post = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    def greet(self):
        return f"Hi My first_name is {self.first_name} and my last name is {self.last_name}"

class Post(db.Model):
    """Post."""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String,
                      nullable=False)
    content = db.Column(db.String,
                        nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)

    def __repr__(self):
        return f"Post title: {self.title} and post content: {self.content}"
    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class Tag(db.Model):
    """Tag."""
    __tablename__= "tags"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)
    
    post_tag = db.relationship('PostTag', backref= 'tag')
    posts = db.relationship('Post',secondary="posts_tags",
        cascade="all,delete",
        backref="tags")
    def __repr__(self):
        return f"Tag: {self.id} and tag name: {self.name}"

class PostTag(db.Model):
    """PostTag."""
    __tablename__= "posts_tags"
    post_id= db.Column(db.Integer,
                       db.ForeignKey('posts.id'),
                       primary_key = True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True)
    
    def __repr__(self):
        return f"Post id: {self.post_id} and tag id: {self.tag_id}"

