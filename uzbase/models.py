from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(50), nullable=False, default='Full-time')
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    author = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Housing(db.Model):
    __tablename__ = 'housing'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    available_from = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    author = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ForumTopic(db.Model):
    __tablename__ = 'forum_topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False, default='Anonymous')
    upvotes = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    replies = db.relationship('ForumReply', backref='topic', lazy=True, cascade='all, delete-orphan')

class ForumReply(db.Model):
    __tablename__ = 'forum_replies'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('forum_topics.id'), nullable=False)
    author = db.Column(db.String(80), nullable=False, default='Anonymous')
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WikiCategory(db.Model):
    __tablename__ = 'wiki_categories'
    id = db.Column(db.Integer, primary_key=True)
    name_uz = db.Column(db.String(120), unique=True, nullable=False)
    name_de = db.Column(db.String(120), nullable=False)
    name_ru = db.Column(db.String(120), nullable=False)

    @property
    def name(self):
        from flask import session
        lang = session.get('lang', 'uz')
        if lang == 'de':
            return self.name_de or self.name_uz
        elif lang == 'ru':
            return self.name_ru or self.name_uz
        return self.name_uz

class WikiItem(db.Model):
    __tablename__ = 'wiki_items'
    id = db.Column(db.Integer, primary_key=True)
    title_uz = db.Column(db.String(120), nullable=False)
    title_de = db.Column(db.String(120), nullable=False)
    title_ru = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('wiki_categories.id', ondelete='CASCADE'), nullable=False)
    content_uz = db.Column(db.Text, nullable=False)
    content_de = db.Column(db.Text, nullable=False)
    content_ru = db.Column(db.Text, nullable=False)

    category = db.relationship('WikiCategory', backref=db.backref('items', lazy=True, cascade="all, delete-orphan"))

    @property
    def title(self):
        from flask import session
        lang = session.get('lang', 'uz')
        if lang == 'de':
            return self.title_de or self.title_uz
        elif lang == 'ru':
            return self.title_ru or self.title_uz
        return self.title_uz

    @property
    def content(self):
        from flask import session
        lang = session.get('lang', 'uz')
        if lang == 'de':
            return self.content_de or self.content_uz
        elif lang == 'ru':
            return self.content_ru or self.content_uz
        return self.content_uz

class PageVisit(db.Model):
    __tablename__ = 'page_visits'
    path = db.Column(db.String(120), primary_key=True)
    count = db.Column(db.Integer, default=0, nullable=False)

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.String(80), nullable=False)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('users.username', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    topic_id = db.Column(db.Integer, nullable=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('users.username', ondelete='CASCADE'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('forum_topics.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint('username', 'topic_id', name='_user_topic_uc'),)
