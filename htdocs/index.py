#!/usr/bin/python3

print("content-type: text/html; charset=utf-8")
print()

import cgi
form = cgi.FieldStorage()
pageId = form['id'].value
print(pageId)

print('''
<!doctype html>
<html>
<head>
  <title>WEB1 - Welcome</title>
  <meta charset="utf-8">
</head>

<body>
  <h1><a href="index.py?id=WEB">WEB</a></h1>
  <ol>
    <li><a href="index.py?id=HTML">HTML</a></li>
    <li><a href="index.py?id=CSS">CSS</a></li>
    <li><a href="index.py?id=JavaScript">JavaScript</a></li>
  </ol>

  <h2>{title}</h2>
  <p>
    The World Wide Web, also known as the WWW and the Web, is an information space where documents and other web resources are identified by Uniform Resource Locators (URLs), interlinked by hypertext links, and accessible via the Internet.[1] English scientist Tim Berners-Lee invented the World Wide Web in 1989. He wrote the first web browser in 1990 while employed at CERN near Geneva, Switzerland.[2][3] The browser was released outside CERN in 1991, first to other research institutions starting in January 1991 and to the general public on the Internet in August 1991.

  The World Wide Web has been central to the development of the Information Age and is the primary tool billions of people use to interact on the Internet.[4][5][6] Web pages are primarily text documents formatted and annotated with Hypertext Markup Language (HTML).[7] In addition to formatted text, web pages may contain images, video, audio, and software components that are rendered in the user's web browser as coherent pages of multimedia content.

  Embedded hyperlinks permit users to navigate between web pages. Multiple web pages with a common theme, a common domain name, or both, make up a website. Website content can largely be provided by the publisher, or interactively where users contribute content or the content depends upon the users or their actions. Websites may be mostly informative, primarily for entertainment, or largely for commercial, governmental, or non-governmental organisational purpose.
  </p>


</body>

'''.format(title=pageId))