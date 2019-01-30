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
  <a href = "create.py">create</a>
  <form action='process_update.py' method="post">
    <input type="hidden" name="pageId" value ="{form_default_title}">
    <p><input type ='text' name='title' placeholder='title' value="{form_default_title}"></p>
    <p><textarea rows = '4' name='description' placeholder='description'>{form_default_desc}</textarea></p>
    <p><input type='submit'></p>
  </form>


</body>


'''.format(title=module.classification()['pageId'], desc = module.classification()['desc'], list = module.getList(), form_default_title = pageId, form_default_desc=description))
