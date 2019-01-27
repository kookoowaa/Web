#!/usr/bin/python3

print("content-type: text/html; charset=utf-8")
print()

import cgi

form = cgi.FieldStorage()
title = form["title"].value
desc = form['description'].value

print(title)
print(desc)

openedFile = open('data/'+title, 'w')
openedFile.write(desc)

#Redirection
print("Location: index.py?id="+title)