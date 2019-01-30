import os

def getList():
  files = os.listdir('data/')
  listStr = ''
  for item in files:
    if item != 'WEB':
      listStr = listStr + '<li><a href="index.py?id={id}">{id}</a></li>'.format(id=item)
  return listStr