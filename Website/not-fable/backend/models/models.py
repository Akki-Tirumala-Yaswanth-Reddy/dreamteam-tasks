from mongoengine import *
import datetime

class ReadingList(Document):
    '''
    name -> String(required)|
    user -> Reference|
    books -> [Reference - Book]
    '''
    name = StringField(required= True)
    user = ReferenceField('User')
    books = ListField(ReferenceField('Book'))

class Comment(EmbeddedDocument):
    '''
    content -> String(required)|
    user -> Reference - User|
    date -> Date(default)
    '''
    content = StringField(required= True)
    user = ReferenceField('User')
    date = DateField(default=datetime.date.today)

class User(Document):
    '''
    username -> String(required, unique)|
    password -> String(required)|
    email -> String(required)|
    friends -> [Reference - User]
    '''
    username = StringField(required= True, unique= True)
    password = StringField(required= True)
    email = StringField(required= True)
    friends = ListField(ReferenceField('User'))

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
    ratings = ListField(IntField())
    reviews = ListField(ReferenceField('Review'))
    comments = ListField(EmbeddedDocumentField(Comment))

class Review(Document):
    '''
    user -> Reference - User|
    book -> Reference - Book|
    content -> String|
    comments -> [Reference - Comment]|
    likes -> [Reference - User]|
    dislikes -> [Reference - User]|
    date -> Date(default) 
    '''
    user = ReferenceField('User')
    book = ReferenceField('Book')
    content = StringField(required= True)
    comments = ListField(EmbeddedDocumentField(Comment))
    likes = ListField(ReferenceField('User'))
    dislikes = ListField(ReferenceField('User'))
    date = DateField(default= datetime.datetime.today)