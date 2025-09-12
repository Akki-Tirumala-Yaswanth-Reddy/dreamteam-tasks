from mongoengine import *
import datetime

class ReadingList(Document):
    name = StringField(required= True)
    user = ReferenceField('User')
    books = ListField(ReferenceField('Book'))

class Comment(EmbeddedDocument):
    content = StringField(required= True)
    user = ReferenceField('User')
    date = DateField(default=datetime.date.today)

class User(Document):
    username = StringField(required= True, unique= True)
    password = StringField(required= True)
    email = StringField(required= True)
    friends = ListField(ReferenceField('User'))

class Book(Document):
    google_id = StringField(required= True)
    title = StringField()
    ratings = ListField(IntField())
    reviews = ListField(ReferenceField('Review'))
    comments = ListField(EmbeddedDocumentField(Comment))

class Review(Document):
    user = ReferenceField('User')
    book = ReferenceField('Book')
    content = StringField(required= True)
    comments = ListField(EmbeddedDocumentField(Comment))
    likes = ListField(ReferenceField('User'))
    dislikes = ListField(ReferenceField('User'))
    date = DateField(default= datetime.datetime.today)