from .db import db

class Level(db.EmbeddedDocument):
    title = db.StringField(required=True)
    content = db.StringField(required=True)
    video_link = db.StringField(required=True)
    video_image = db.StringField(required=True)

class NewsLevels(db.Document):
    meta = {'collection': 'english_in_levels'}
    level_1 = db.EmbeddedDocumentListField(Level)
    level_2 = db.EmbeddedDocumentListField(Level)
    level_3 = db.EmbeddedDocumentListField(Level)

class Contact(db.Document):
    name = db.StringField(required=True)
    surname = db.StringField(required=True)



