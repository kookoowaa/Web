#!/usr/bin/python3

print("content-type: text/html; charset=utf-8")
print()
import cgi, os, module

cgi_data = module.classification()

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
  {create}
  {update}
  {delete}
  <h2>{title}</h2>
  <p>{desc}</p>

</body>
'''.format(title = cgi_data['pageId'], desc = cgi_data['desc'], 
           list = module.getList(), create = cgi_data['create'],
           update = cgi_data['update'], delete = cgi_data['delete']))
