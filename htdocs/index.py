#!/usr/bin/python3

print("content-type: text/html; charset=utf-8")
print()
import cgi, os, module

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

'''.format(title = module.classification()['pageId'], desc = module.classification()['desc'], 
           list = module.getList(), create = module.classification()['create'],
           update = module.classification()['update'], delete = module.classification()['delete']))
