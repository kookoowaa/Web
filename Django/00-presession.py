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

### ex5 - urlopen() HTTPCookieProcessor 클래스로 쿠키 데이터를 포함하여 요청

### ex6 - urlopen() ProxyHandler 및 ProxyBasicAuthHandler 클래스로 프록시 처리

### ex7 - urllib.request 모듈 예제

### ex8 - http.client 모듈 GET 방식 요청

### ex9 - http.client 모듈 HEAD 방식 요청

### ex10- http.client 모듈 POST 방식 요청

### ex11- http.client 모듈 PUT 방식 요청

### ex12- http.client 모듈 예제

### ex13- 웹서버

### ex14- CGI 웹서버 시험용 스크립트

### ex15- CGI 웹서버 시험용 클라이언트

### ex16- WSGI 서버