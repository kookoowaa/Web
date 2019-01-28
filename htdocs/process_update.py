#!/usr/bin/python3

import cgi, os

form = cgi.FieldStorage()
pageId = form['pageId'].value
title = form["title"].value
desc = form['description'].value

openedFile = open('data/'+pageId, 'w')
openedFile.write(desc)
openedFile.close()

os.rename('data/'+pageId, 'data/'+title)

#Redirection
print("Location: index.py?id="+title)
print()