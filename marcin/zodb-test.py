#!/usr/bin/python
# -*- coding: utf-8 -*-

import transaction

from ZODB import FileStorage, DB
storage = FileStorage.FileStorage('mydatabase.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

root['employees'] = ['Mary', 'Jo', 'Bob']
transaction.commit()

connection.close()

storage = FileStorage.FileStorage('mydatabase.fs')
db = DB(storage)
connection = db.open()
root = connection.root()
print root.items()
