# 컨텐츠 삭제

index.py

```python
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
  '''.format(pageId)
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
```

process_delete.py

```python
#!/usr/bin/python3

import cgi, os

form = cgi.FieldStorage()
pageId = form["pageId"].value

os.remove('data/'+pageId)

#Redirection
print("Location: index.py")
print()
```

- 컨텐츠 삭제 역시 `<form>` 안에서 이루어지며 절차는 다음과 같음:
  1. 삭제 버튼 생성 (단, WEB 같이 최상위 폴더는 제외)
  2. 삭제 기능 구현

___

## 삭제 버튼 생성

- `index.py`를 수정하여 삭제기능을 부여하되, id 값이 주어진 경우만 (WEB) 삭제 버튼을 생성

- post 메서드를 지닌 `<form>`으로 `process_delete.py`라는 삭제기능을 호출:

  ```python
  if 'id' in form:
    delete_action = '''
      <form action="process_delete.py" method="post">
        <input type="hidden" name="pageId" value="{}">
        <input type="submit" value="delete">
      </form>
    '''.format(pageId)
  else:
    delete_action = ''
  ```

- 본문에 `delete_action` 삽입:

  ```python
  print('''
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
  ```

___

## 삭제 기능 구현

- 위 `<form>`에서 `process_delete.py`를 호출하여 삭제 기능을 실행

- `process_delete.py`는 `index.py`로부터 POST 된 `pageId` 값을 이용하여 삭제

- `pageId`는 `data/`의 파일명과 동일하므로 `os`라이브러리를 호출하여 삭제 수행:

  ```python
  import cgi, os
  form = cgi.FieldStorage()
  pageId = form["pageId"].value
  os.remove('data/'+pageId)
  ```

- 삭제 후에는 최상위 폴더로 redirect:

  ```python
  #Redirection
  print("Location: index.py")
  print()
  ```