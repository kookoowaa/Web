# 컨텐츠 수정

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
else:
  pageId = 'WEB'
  update_link = ''

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
  <h2>{title}</h2>
  <p>{desc}</p>


</body>

'''.format(title=pageId, desc = description, list = listStr, update = update_link))
```

update.py

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
  <form action='process_update.py' method="post">
    <input type="hidden" name="pageId" value ="{form_default_title}">
    <p><input type ='text' name='title' placeholder='title' value="{form_default_title}"></p>
    <p><textarea rows = '4' name='description' placeholder='description'>{form_default_desc}</textarea></p>
    <p><input type='submit'></p>
  </form>


</body>


'''.format(title=pageId, desc = description, list = listStr, form_default_title = pageId, form_default_desc=description))
```

process_update.py

```python
#!/usr/bin/python3

import cgi, os

form = cgi.FieldStorage()
pageId = form['pageId'].value
title = form["title"].value
desc = form['description'].value

openedFile = open('data/'+pageId, 'w')
openedFile.write(desc)
openedFile.close()

os.rename('data/'+pageId, 'data/'+title)

#Redirection
print("Location: index.py?id="+title)
print()
```

- 사용자에 의해서 컨텐츠 수정이 이루어 지는 과정은 `포스트 기능(form)`에서 진행한 절차와 유사하며 다음과 같음:
  1. 컨텐츠 수정 페이지 생성
  2. 수정될 컨텐츠 값 입력
  3. 파일 호출 및 컨텐츠 수정

___

## 1. 컨텐츠 수정 페이지 생성

- 컨텐츠 수정 페이지는 `update.py`를 생성하고 이를 통해 입력 프로세스를 진행

- `포스트 기능(form)`때 처럼 `<a href="update.py">` 링크를 추가:

  ```html
  <a href = "update.py">update</a>
  ```

- 단, 상위 페이지의 description을 수정하는 것은 문제가 될 수 있기 때문에, 상위 페이지에서는 위 링크를 보여주지 않음

- 이를 위해서 `?id=''`쿼리를 활용하여 `index.py`를 수정:

  ```python
  form = cgi.FieldStorage()
  if 'id' in form:
    update_link = '<a href = "update.py?id={}">update</a>'.format(pageId)
  else:
    update_link = ''
  
  print('''
  <!doctype html>
  
  <body>
    <a href = "create.py">create</a>
    {update}
  
  </body>
  
  '''.format(update = update_link))
  ```

___

## 2. 수정될 컨텐츠 값 입력

- `update.py`는 `create.py`와 매우 유사한 형태를 띔

- `title`과 `description`을 기반으로 `data`폴더 내 데이터의 수정이 이루어 지는 프로세스를 수행

- 이 때, 주의할 점이 하나 있는데, `title`명이 원 `title`과 다를 시 파일 수정이 아닌 생성이 이루어지게 됨

- 따라서 `create.py`와는 다르게 `<form type=hidden>`을 추가로 생성하여 `pageId`, 즉 원 파일명을 별도의 객체 값으로 가져가도록 함:

  ```html
  <form action='process_update.py' method="post">
      // 이하 추가 된 부분
      <input type="hidden" name="pageId" value ="{form_default_title}">
      //
      <p><input type ='text' name='title' placeholder='title' value="{form_default_title}"></p>
      <p><textarea rows = '4' name='description' placeholder='description'>{form_default_desc}</textarea></p>
      <p><input type='submit'></p>
    </form>
  ```

___

## 3. 파일 호출 및 컨텐츠 수정

- `update.py`에서는 form을 `process_update.py` 메서드로 처리

- `process_update.py`는 새로운 인자인 `pageId`로 파일을 열고:

    ```python
    form = cgi.FieldStorage()
    pageId = form['pageId'].value
    title = form["title"].value
    desc = form['description'].value
    
    openedFile = open('data/'+pageId, 'w')
    ```

-  `description`으로 파일을 업데이트 한 후:

    ```python
    openedFile.write(desc)
    openedFile.close()
    ```

-  파일명을 `title`로 수정

    ```python
    import os
    
    os.rename('data/'+pageId, 'data/'+title)
    ```

  

