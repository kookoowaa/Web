# Apache-Python CGI로 연동하기

- Apache의 환경설정 수정 필요 `C:/Bitnami/wampstack-7.1.15-0/apache2/conf/httpd.conf`
-  mod_cgi 혹은 mod_cgid 기능을 활성화 (하단의 행에서 # 제거)

```
 #LoadModule cgi_module modules/mod_cgi.so
```

- Document root에서 확장자가 py인 파일은 Python으로 실행하도록 정정

```
# 아래 주소를 참조하여 서버 운용 (root directory)
DocumnetRoot "C:/Bitnami/wampstack-7.1.15-0/apache2/htdocs"

# 이하 directory에 대한 config
# 주석 제외 아래 명령어는 실행 되어야 함
<Directory "C:/Bitnami/wampstack-7.1.15-0/apache2/htdocs">
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
    
    # 아래 내용 수정: 확장자가 py인 파일은 cgi로 실행
    <Files "*.py">
      Options ExecCGI
      AddHandler cgi-script .py
    </Files>
   
</Directory>
```

- 서버 재시작 후 py 파일 실행 시 Internal Server Error 발생
- apache/logs/error.log를 살펴보면 *.py is not executable이라는 에러 발생 확인 가능

```
[win32:error] [pid 17528:tid 1344] [client 192.168.4.63:65319] AH02102: C:/Bitnami/wampstack-7.1.25-0/apache2/htdocs/test.py is not executable; ensure interpreted scripts have "#!" or "'!" first line
```

- 해당 에러 해결을 위해 py 파일 첫번째 줄에 다음과 같이 첫줄 입력해서 python 언어로 파일을 실행

```
#!python
```

- 재실행 시 여전히 Internal Server Error 발생
- error.log를 살펴보면 Bad header: 1.0 확인 가능

```
[Fri Jan 11 08:47:25.860895 2019] [cgi:error] [pid 17528:tid 1344] [client 192.168.4.63:65365] malformed header from script 'test.py': Bad header: 1.0
```

- py 파일에 다음과 같은 헤더를 추가

```
print("content-type: text/html; charset=utf-8\n")
```

- 서버에서 py 파일 재실행 시 정상적으로 작동하는 것을 확인