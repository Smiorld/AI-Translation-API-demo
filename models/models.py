from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Translation(db.Model):
    __tablename__ = 'translation'
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    target_lang = db.Column(db.String(10), nullable=False)
    translated_text = db.Column(db.Text, nullable=False)
    proofread_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    crawled_text_id = db.Column(db.Integer, db.ForeignKey('crawled_text.id'), nullable=True)

class CrawledText(db.Model):
    __tablename__ = 'crawled_text'
    
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="new")  # new / processing / done
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    translation = db.relationship("Translation", backref="crawled", uselist=False) # backref