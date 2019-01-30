#!/usr/bin/python3

print("content-type: text/html; charset=utf-8")
print()

import cgi, os, module

form = cgi.FieldStorage()
if 'id' in form:
  pageId = form['id'].value
else:
  pageId = 'WEB'

description = open('data/'+pageId, 'r', encoding='utf-8').read()


print('''
<!doctype html>
<html>
<head>
  <title>WEB1 - Welcome</title>
  <meta charset="utf-8">
</head>

<body>
  <h1><a href="index.py">WEB</a></h1>
  <ol>{list}</ol>
  <a href = "create.py">create</a>
  <form action='process_create.py' method="post">
    <p><input type ='text' name='title' placeholder='title'></p>
    <p><textarea rows = '4' name='description' placeholder='description'></textarea></p>
    <p><input type='submit'></p>
  </form>


</body>


'''.format(title=pageId, desc = description, list = module.getList()))
