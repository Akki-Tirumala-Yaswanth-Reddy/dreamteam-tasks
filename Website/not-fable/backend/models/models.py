from mongoengine import *
from bson import ObjectId
import datetime

class ReadingList(Document):
    '''
    name -> String(required)|
    user -> Reference|
    books -> [Reference - Book]
    '''
    name = StringField(required= True, unique=True)
    user = ReferenceField('User')
    books = ListField(ReferenceField('Book'))

class Comment(EmbeddedDocument):
    '''
    content -> String(required)|
    user -> Reference - User|
    date -> Date(default)
    '''
    id = ObjectIdField(default=lambda: ObjectId()) # The backend code is easy if the id exists
    content = StringField(required= True)
    user = ReferenceField('User')
    date = DateField(default=datetime.date.today)

class User(Document):
    '''
    username -> String(required, unique)|
    password -> String(required)|
    email -> String(required)|
    '''
    username = StringField(required= True, unique= True)
    password = StringField(required= True)
    email = StringField(required= True)
    followers = ListField(ReferenceField('User'))
    following = ListField(ReferenceField('User'))
    reviews = ListField(ReferenceField('Review'))
    
    meta = {
        'strict': False  # This allows unknown fields in the database to be ignored
    } # I was getting some weird error
    # The fields \"{'friends'}\" do not exist on the document \"User\"

class Book(Document):
    '''
    google_id -> String(required)|
    title -> String|
    ratings -> [Integer]|
    reviews -> [Reference - Review]|
    comments -> [Reference - Comment]
    '''
    google_id = StringField(required= True)
    title = StringField()
    ratings = ListField(ReferenceField('Rating'))
    reviews = ListField(ReferenceField('Review'))

class Rating(Document):
    google_id = StringField(required=True)
    user = ReferenceField('User', required=True)
    rating = IntField(required=True)

class LikeDislike(EmbeddedDocument):
    value = IntField()
    user = ReferenceField('User')

class Review(Document):
    '''
    user -> Reference - User|
    book -> Reference - Book|
    content -> String|
    comments -> [Reference - Comment]|
    likes -> {Reference - User}|
    dislikes -> {Reference - User}|
    date -> Date(default) 
    '''
    user = ReferenceField('User')
    book = ReferenceField('Book')
    heading = StringField()
    rating = StringField()
    content = StringField(required= True)
    comments = ListField(EmbeddedDocumentField(Comment))
    likesDislikes = ListField(EmbeddedDocumentField(LikeDislike))
    date = DateField(default= datetime.datetime.today)

