import datetime
from peewee import *

DATABASE = SqliteDatabase('sqlite-tweets.db')

class Message(Model):
    content = TextField()
    published_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Message], safe=True)
    DATABASE.close()
