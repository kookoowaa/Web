import cgi, os

def getList():
  files = os.listdir('data/')
  listStr = ''
  for item in files:
    if item != 'WEB':
      listStr = listStr + '<li><a href="index.py?id={id}">{id}</a></li>'.format(id=item)
  return listStr

def classification():
  form = cgi.FieldStorage()
  if 'id' in form:
    pageId = form['id'].value
    update_link = '<a href = "update.py?id={}">update</a>'.format(pageId)
    delete_action = '''
      <form action="process_delete.py" method="post">
        <input type="hidden" name="pageId" value="{}">
        <input type="submit" value="delete">
      </form>
    '''.format(pageId)
  else:
    pageId = 'WEB'
    update_link = ''
    delete_action = ''
  
  create_list = '<a href = "create.py">create</a>'
  description = open('data/'+pageId, 'r', encoding='utf-8').read()

  return {'pageId':pageId, 'update':update_link, 'delete':delete_action, 'create': create_list, 'desc': description}