# URL Query String 활용하기

## URL의 query string을 입력값으로 웹 애플리케이션 끌어오기

```python
import cgi
form = cgi.FieldStorate()
pageId = form['id'].value

print('''
<!doctype html>
<html>
<head>
  <title>WEB1 - Welcome</title>
  <meta charset="utf-8">
</head>

<body>
  <h1><a href="index.html?id=WEB">WEB</a></h1>
  <ol>
    <li><a href="index.py?id=HTML">HTML</a></li>
    <li><a href="indesx.py?id=CSS">CSS</a></li>
    <li><a href="index.py?id=JavaSctipt">JavaScript</a></li>
  </ol>

  <h2>{title}</h2>
  <p>
    The World Wide Web, also known as the WWW and the Web, is an information space where documents and other web resources are identified by Uniform Resource Locators (URLs), interlinked by hypertext links, and accessible via the Internet.[1] English scientist Tim Berners-Lee invented the World Wide Web in 1989. He wrote the first web browser in 1990 while employed at CERN near Geneva, Switzerland.[2][3] The browser was released outside CERN in 1991, first to other research institutions starting in January 1991 and to the general public on the Internet in August 1991.

  The World Wide Web has been central to the development of the Information Age and is the primary tool billions of people use to interact on the Internet.[4][5][6] Web pages are primarily text documents formatted and annotated with Hypertext Markup Language (HTML).[7] In addition to formatted text, web pages may contain images, video, audio, and software components that are rendered in the user's web browser as coherent pages of multimedia content.

  Embedded hyperlinks permit users to navigate between web pages. Multiple web pages with a common theme, a common domain name, or both, make up a website. Website content can largely be provided by the publisher, or interactively where users contribute content or the content depends upon the users or their actions. Websites may be mostly informative, primarily for entertainment, or largely for commercial, governmental, or non-governmental organisational purpose.
  </p>


</body>

'''.format(title=pageId))
```



- 본 예제에서 변경한 사항은 크게 2가지임
  1. cgi를 활용하여 `?id=`로 웹페이지 호출
  2. 포매팅을 활용하여 타이틀 자동 변경

1. CGI 활용

   - 다음 페이지 참조 https://docs.python.org/2/library/cgi.html

   - cgi 라이브러리를 활용하면 웹 페이지 내 query로 웹페이지 호출 가능

     ```python
     import cgi
     form = cgi.FieldStorate()
     pageId = form['id'].value
     ```

   - `Body` 영역을 보면 `href`에 id query 값을 같는 것을 확인 할 수 있음

     ```html
      <h1><a href="index.html?id=WEB">WEB</a></h1>
       <ol>
         <li><a href="index.py?id=HTML">HTML</a></li>
         <li><a href="indesx.py?id=CSS">CSS</a></li>
         <li><a href="index.py?id=JavaSctipt">JavaScript</a></li>
       </ol>
     ```

2. 포매팅 활용하여 타이틀 자동 변경

   - 본문을 확인하면 포매팅을 활용하여 중간 타이틀을 쿼리 값에 따라 변경되게 수정한 것을 확인 가능

     ```python
     print('''
       <h2>{title}</h2>
       <p>
     	...
     	...
     	...
       </p>
     '''.format(title=pageId))
     ```