### server available at "source/RedBook/ch2-test-server/manage.py runserver"

### ex1 - urlopen() GET 요청
from urllib.request import urlopen
f = urlopen("http://www.example.com")
print(f.read(500).decode('utf-8'))


### ex2 - urlopen() POST 요청
data = "language=python&framework=django"
f = urlopen("http://127.0.0.1:8000", bytes(data, encoding='utf-8'))
print(f.read(500).decode('utf-8'))


### ex3 - urlopen() Request 클래스로 헤더 지정
from urllib.request import Request
from urllib.parse import urlencode

url = 'http://127.0.0.1:8000'
data = {
    "name": "김석훈",
    "email": "shkim@naver.com",
    "url": "http://www.naver.com"
}
encData = urlencode(data)
postData = bytes(encData, encoding='utf-8')
req = Request(url, data=postData)
req.add_header("content-Type", "application/x-www-form-urlencoded")
f = urlopen(req)
print(f.info())
print(f.read(500).decode('utf-8'))


### ex4 - urlopen() HTTPBasicAuthHandler 클래스로 인증 요청
from urllib.request import HTTPBasicAuthHandler, build_opener

auth_handler = HTTPBasicAuthHandler()
auth_handler.add_password(realm='ksh', user='shkim', passwd='shkimadmin', uri='http://127.0.0.1:8000/auth/')
opener = build_opener(auth_handler)
resp = opener.open('http://127.0.0.1:8000/auth/')
print(resp.read().decode('utf-8'))


### ex5 - urlopen() HTTPCookieProcessor 클래스로 쿠키 데이터를 포함하여 요청
from urllib.request import HTTPCookieProcessor

url = 'http://127.0.0.1:8000/cookie'
# GET request first with cookie handler
cookie_handler = HTTPCookieProcessor()
opener = build_opener(cookie_handler)
req = Request(url)
res = opener.open(req)
print(res.info())
print(res.read().decode('utf-8'))

# POST request
data='language=python&framework=django'
encData = bytes(data, encoding='utf-8')
req = Request(url, encData)
res = opener.open(req)
print(res.info())
print(res.read().decode('utf-8'))


### ex6 - urlopen() ProxyHandler 및 ProxyBasicAuthHandler 클래스로 프록시 처리
import urllib.request

url = 'http://www.example.com'
proxyServer = 'http://www.proxy.com:3218'

# proxy 서버를 통해 웹 서버로 요청 전송
proxy_handler = urllib.request.ProxyHandler({'http': proxyServer})
# proxy 서버 설정 무시하고 웹 서버로 요청 전송
# proxy_handler = urllib.request.ProxyHandler({})

# proxy 서버 인증 처리
proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
proxy_auth_handler.add_password('realm', 'host', 'username', 'password')

# 2개의 handler를 opener에 등록
opener = urllib.request.build_opner(proxy_handler, proxy_auth_handler)

# 디폴트 오프너로 지정하고 urlopen() 함수로 요청 전송
urllib.request.install_opener(opener)

# opener.open() 대신 urlopen() 사용
f = urllib.request.urlopen(url)

print("geturl():", f.geturl())
print(f.read(300).decode('utf-8'))


### ex7 - urllib.request 모듈 예제
from urllib.request import urlopen
from html.parser import HTMLParser

class ImageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        if not hasattr(self, 'result'):
            self.result = []
        for name, value in attrs:
            if name =='src':
                self.result.append(value)

def parse_image(data):
    parser = ImageParser()
    parser.feed(data)
    dataSet = set(x for x in parser.result)
    return dataSet

def main():
    url = 'http://www.google.co.kr'

    with urlopen(url) as f:
        charset = f.info().get_param('charset')
        data = f.read().decode(charset)
    
    dataSet = parse_image(data)

    print('\n>>>>>>>> Fetch Imanges from ', url)
    print('\n'.join(sorted(dataSet)))

if __name__ =='__main__':
    main()


### ex8 - http.client 모듈 GET 방식 요청
from http.client import HTTPConnection

host = 'www.example.com'
conn = HTTPConnection(host)
conn.request("GET", '/')
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()
conn.close()


### ex9 - http.client 모듈 HEAD 방식 요청

conn = HTTPConnection("www.example.com")
conn.request("HEAD", '/')
resp = conn.getresponse()
print(resp.status, resp.reason)
data = resp.read()
print(len(data))
print(data==b'')


### ex10- http.client 모듈 POST 방식 요청

host = '127.0.0.1:8000'
params = urlencode({
    'language': 'python',
    'name': '김석훈',
    'email': 'shkim@naver.com'
})
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain'
}

conn = HTTPConnection(host)
conn.request('POST', '', params, headers)
resp = conn.getresponse()
print(resp.status, resp.reason)

data = resp.read()
print(data.decode('utf-8'))

conn.close()


### ex11- http.client 모듈 PUT 방식 요청

host = '127.0.0.1:8000'
params = urlencode({
    'language': 'python',
    'name': '김석훈',
    'email': 'shkim@naver.com'
})
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain'
}

conn = HTTPConnection(host)
conn.request('PUT', '', params, headers)
resp = conn.getresponse()
print(resp.status, resp.reason)

data = resp.read()
print(data.decode('utf-8'))

conn.close()


### ex12- http.client 모듈 예제

import os
from http.client import HTTPConnection
from urllib.parse import urljoin, urlunparse
from urllib.request import urlretrieve
from html.parser import HTMLParser

class ImageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        if not hasattr(self, 'result'):
            self.result = []
        for name, value in attrs:
            if name== 'src':
                self.result.append(value)

def download_image(url, data):
    if not os.path.exists("DOWNLOAD"):
        os.makedirs("DOWNLOAD")
    parser = ImageParser()
    parser.feed(data)
    dataSet = set(x for x in parser.result)

    for x in sorted(dataSet):
        imageUrl = urljoin(url, x)
        basename = os.path.basename(imageUrl)
        targetFile = os.path.join("DOWNLOAD", basename)

        print("Downloading...", imageUrl)
        urlretrieve(imageUrl, targetFile)

def main():
    host = 'www.google.co.kr'

    conn = HTTPConnection(host)
    conn.request("GET", '')
    resp = conn.getresponse()

    charset = resp.msg.get_param("charset")
    data = resp.read().decode(charset)
    conn.close()

    print('\n>>>>>>>>>>>> Download Images from ', host)
    url = urlunparse(('http', host, '', '', '', ''))
    download_image(url, data)

if __name__ =='__main__':
    main()

### ex13- 웹서버

from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response_only(200, 'OK')
        self.send_header("content-Type", 'text/plain')
        self.end_headers()
        self.wfile.write(b"Hello World")

if __name__ == '__main__':
    server = HTTPServer(('',8888), MyHandler)
    print("Started WebServer on port 8888....")
    print("Press ^C to quit server")
    server.serve_forever()

# 별도의 위 과정 없이도 내부 클래스 만으로 서버 구현이 가능 
# > python -m http.server 8888


### ex14- CGI 웹서버 시험용 스크립트
# Django\RedBook\ch2\cgi-server 폴더에서 서버 구현
# > python -m http.server 8888 --cgi

import cgi

form = cgi.FieldStorage()
name = form.getvalue('name')
email = form.getvalue('email')
url = form.getvalue('url')

print("Content-Type: text/plain")
print()

print("Welcome.. CGI Script")
print("name is", name)
print("email is", email)
print('url is', url)

### ex15- CGI 웹서버 시험용 클라이언트

from urllib.request import urlopen
from urllib.parse import urlencode


url = "http://127.0.0.1:8888/cgi-bin/script.py"
data = {
    'name': '김석훈',
    'email': 'shkim@naver.com',
    'url': 'http://www.naver.com',
}
encData = urlencode(data)
postData = encData.encode('ascii')

f = urlopen(url, postData)   # POST
print(f.read().decode('cp949'))

### ex16- WSGI 서버