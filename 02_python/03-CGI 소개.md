# CGI 소개

- Common Gateway Interface는 클라이언트의 요청을, 백엔드 프로그램의 결과가 컴파일되어 서버를 통해 반환되는 과정을 설명
- 오늘날에는 CGI의 한계점을 보완한 FSGI, WSGI 같은 기술을 사용
- 단, 서버에서 많은 프로그램을 수행하므로  무리를 주게 됨
- Query String으로 요청하면 백엔드에서 (python) 처리하고 결과를 서버를 통해 반환

___



- `cgi_env.py` 파일로 테스트 진행

```python
#!/usr/local/bin/python3
print("Content-Type: text/html")
print()
import cgi
cgi.test()
```

- 웹페이지에서 `~/cgi_env.py?id=HTML`을 실행 시 아래와 같은 결과 반환

```
Content-type: text/html
Current Working Directory:
/var/www/web/htdocs
Command Line Arguments:
['/var/www/web/htdocs/cgi_env.py']
Form Contents:
id: <class 'cgi.MiniFieldStorage'>
MiniFieldStorage('id', 'HTML')
Shell Environment:
CONTEXT_DOCUMENT_ROOT
/var/www/web/htdocs
CONTEXT_PREFIX
DOCUMENT_ROOT
/var/www/web/htdocs
GATEWAY_INTERFACE
CGI/1.1
HTTP_ACCEPT
text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
HTTP_ACCEPT_ENCODING
gzip, deflate
HTTP_ACCEPT_LANGUAGE
en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,zh-CN;q=0.6,zh;q=0.5
HTTP_CONNECTION
keep-alive
HTTP_HOST
35.200.49.94
HTTP_UPGRADE_INSECURE_REQUESTS
1
HTTP_USER_AGENT
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

QUERY_STRING
id=HTML

REMOTE_ADDR
210.183.222.238
REMOTE_PORT
52414
REQUEST_METHOD
GET
REQUEST_SCHEME
http
REQUEST_URI
/cgi_env.py?id=HTML
SCRIPT_FILENAME
/var/www/web/htdocs/cgi_env.py
SCRIPT_NAME
/cgi_env.py
SERVER_ADDR
10.146.0.28
SERVER_ADMIN
webmaster@localhost
SERVER_NAME
35.200.49.94
SERVER_PORT
80
SERVER_PROTOCOL
HTTP/1.1
SERVER_SIGNATURE
<address>Apache/2.4.18 (Ubuntu) Server at 35.200.49.94 Port 80</address>
SERVER_SOFTWARE
Apache/2.4.18 (Ubuntu)
```

- 주목할 점은 중간에 QUERY_STRING 부분이며, 요청한 정보를 Python에 전달하여 프로그램을 실행