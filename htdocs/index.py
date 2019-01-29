#!/usr/bin/python3

print("content-type: text/html; charset=utf-8")
print()

import cgi, os

files = os.listdir('data/')
listStr = ''
for item in files:
  if item != 'WEB':
    listStr = listStr + '<li><a href="index.py?id={id}">{id}</a></li>'.format(id=item)


form = cgi.FieldStorage()
if 'id' in form:
  pageId = form['id'].value
  update_link = '<a href = "update.py?id={}">update</a>'.format(pageId)
  delete_action = '''
    <form action="process_delete.py" method="post">
      <input type="hidden" name="pageId" value="{}">
      <input type="submit" value="delete">
    </form>
  '''
else:
  pageId = 'WEB'
  update_link = ''
  delete_action = ''

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
  {update}
  {delete}
  <h2>{title}</h2>
  <p>{desc}</p>


</body>

'''.format(title=pageId, desc = description, list = listStr, update = update_link, delete=delete_action))
