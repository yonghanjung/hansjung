from google.appengine.ext import db
from operator import itemgetter

class Database(db.Model):
    def __init__(self):
        self.database= [

            {
                'id': 1,
                'title': "Start!",
                'content': "Start! Example",
                'likecount' : 0,
                'check' : 0,
                'photo' : None
            }]
            # Dictionary

    def newid(self):
        return self.maxid() + 1

    def maxid(self):
        _id = -1
        for item in self.database:
            if _id < item['id']:
                _id = item['id']
        return _id

    def put(self, storage):
        self.database.append(storage)


    ## It is model so that we don't want to put like 

    def select(self, _id):
        for idx, value in enumerate(self.database):
            if str(value['id']) == _id:
                return value

    def update(self, _id, item):
        for idx, value in enumerate(self.database):
            if str(value['id']) == _id:
                self.database[idx] = item
                break
    # For Like+1 ==> it is okay just to add likecounter button
    # However, this is general button for adding 1 for every case 
    # becase it is MODEL 


    def delete(self, _id):

        # for item in self.database:
        # We don't code like that because, we want to access to
        # the data directly.

        for idx, value in enumerate(self.database):
            if str(value['id']) == _id:
                self.database.pop(idx)
                break

    def out(self):
        self.database = sorted(self.database, key=itemgetter('likecount'),reverse = True) 
        return self.database

    def get_entries_10(self):
        return self.database[:10]
