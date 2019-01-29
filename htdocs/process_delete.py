#!/usr/bin/python3

import cgi

form = cgi.FieldStorage()
title = form["title"].value
desc = form['description'].value

openedFile = open('data/'+title, 'w')
openedFile.write(desc)
openedFile.close()

#Redirection
print("Location: index.py?id="+title)
print()