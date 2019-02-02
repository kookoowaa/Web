# 보안(XSS)

module.py (수동)

```python
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
  sanitizer = Sanitizer()

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
  description = description.replace('<', '&lt;')
  description = description.replace('>', '&gt;')

  return {'pageId':pageId, 'update':update_link, 'delete':delete_action, 'create': create_list, 'desc': description}
```

module.py(패키지)

```python
import cgi, os
from html_sanitizer import Sanitizer

def getList():
  files = os.listdir('data/')
  listStr = ''
  for item in files:
    if item != 'WEB':
      listStr = listStr + '<li><a href="index.py?id={id}">{id}</a></li>'.format(id=item)
  return listStr



def classification():
  
  form = cgi.FieldStorage()
  sanitizer = Sanitizer()

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
  description = sanitizer.sanitize(description)

  return {'pageId':pageId, 'update':update_link, 'delete':delete_action, 'create': create_list, 'desc': description}
```

- 보안 이슈의 한 예로, XSS(Cross Site Scripting)을 통해 다른 사이트로 납치되거나, 원치 않는 기능이 실행되는 수가 있음
- 본 예제 `index.py`에서는 create를 통해 `<script>`를 심어 위와 같은 문제가 발생할 수 있음
- XSS에 대응하기 위한 방법은 아래 두가지가 있음 (본 예제에서):
  1. 스크립트가 실행되는 대신, 스크립트가 출력되게 만듬
  2. html 세탁(sanitizer)를 통해 모든 태그를 html용 태그로 변환 (혹은 삭제)

___

## 스크립트 출력

- 데이터 내  ''`<`''와 ''`>`''를 문자로 인식하게 만들어 버림으로써 스크립트가 실행되는 대신 출력 가능하도록 만듬

- ''`<`''는 "`&lt;`"으로,  ''`>`''는 "`&gt;`"으로 변경하면 해당 기호가 문자로 인식되어 그래도 출력

- `module.py` 내 description 호출 후 해당 문자열 치환

  ```python
  description = open('data/'+pageId, 'r', encoding='utf-8').read()
  description = description.replace('<', '&lt;')
  description = description.replace('>', '&gt;')
  ```

___

## html 세탁

- `html-sanitizer` 패키지는 태그를 변환해 주는 기능을 제공

- 위 패키지에서 제공하는 기능의 예시를 보면 다음과 같음

  ```python
  >>> from html_sanitizer import Sanitizer
  >>> sanitizer = Sanitizer()  # default configuration
  >>> sanitizer.sanitize('<span style="font-weight:bold">some text</span>')
  '<strong>some text</strong>'
  ```

- 이를 `module.py`에 활용하면, 호출된 desciption에 다음과 같이 적용 가능

  ```python
  from html_sanitizer import Sanitizer
  
  sanitizer = Sanitizer()
      
  description = open('data/'+pageId, 'r', encoding='utf-8').read()
  description = sanitizer.sanitize(description)
  ```

- html 세탁 적용 후 `/index.py?id=HTML`의 스크립트 결과 값을 보면 다음과 같은 차이를 발견할 수 있음

  세탁 전

  ```html
  <p><a href="https://www.w3.org/TR/html5/" target="_blank" title="html5 specification">Hypertext Markup Language (HTML)</a>is the standard markup language for <strong>creating <u>web</u> pages</strong> and web applications.Web browsers receive HTML documents from a web server or from local storage and render them into multimedia web pages. HTML describes the structure of a web page semantically and originally included cues for the appearance of the document.<img src="coding.jpg" width="100%"></p>
  
  <p style="margin-top:45px;">HTML elements are the building blocks of HTML pages. With HTML constructs, images and other objects, such as interactive forms, may be embedded into the rendered page. It provides a means to create structured documents by denoting structural semantics for text such as headings, paragraphs, lists, links, quotes and other items. HTML elements are delineated by tags, written using angle brackets.</p>
  ```

  세탁 후

  ```html
  <p><a href="https://www.w3.org/TR/html5/" target="_blank" title="html5 specification" rel="noopener">Hypertext Markup Language (HTML)</a> is the standard markup language for <strong>creating web pages</strong> and web applications.Web browsers receive HTML documents from a web server or from local storage and render them into multimedia web pages. HTML describes the structure of a web page semantically and originally included cues for the appearance of the document.</p>
  
  <p>HTML elements are the building blocks of HTML pages. With HTML constructs, images and other objects, such as interactive forms, may be embedded into the rendered page. It provides a means to create structured documents by denoting structural semantics for text such as headings, paragraphs, lists, links, quotes and other items. HTML elements are delineated by tags, written using angle brackets.</p>
  ```

- html 세탁 결과 CSS나 image 같은 내용들이 변경된 것을 확인할 수 있음