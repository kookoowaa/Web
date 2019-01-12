# Code Anywhere

- [Codeanywhere](https://codeanywhere.com)는 가상의 컴퓨터를 대여해주는 서비스(5대 무료)
- File > New Connection > Container로 들어가면 다양한 linux 기반 서비스를 제공 받을 수 있음
- HTML로 container 생성 시 외부에서 접속 가능 한 주소도 제공
- HTML로 container 생성 시 python2, python3도 깔려 있는 상태



# Basic Linux

- 위에서 만든 container에 `index.html`을 생성하면 외부에서 웹페이지 접속/활용 가능

- `helloworld.py`를 아래와 같이 생성, shell에서 `python3 helloworld.py`로 python 파일 실행 가능

  ```python
  print("Hello World")
  >> Hello World
  ```

- 만약 shell에서 `python3` 명령어 없이 반복 실행하려면 1) 권한을 부여하고 2) python으로 실행토록 사전 정보를 제공해야 함

  ```shell
  cabox@web2-python:~/workspace$ ./helloworld.py
  -bash: ./helloworld.py: Permission denied
  ```

  - 위와 같이 실행 시 권한이 없다고 에러 반환

  ```shell
  cabox@web2-python:~/workspace$ sudo chmod a+x helloworld.py
  cabox@web2-python:~/workspace$ ls -l
  total 8
  -rwxr-xr-x 1 cabox www-data 21 Jan 12 09:04 helloworld.py
  -rw-r--r-- 1 cabox www-data 32 Jan 12 08:56 index.html
  cabox@web2-python:~/workspace$ ./helloworld.py
  ./helloworld.py: line 1: syntax error near unexpected token `"Hello World"'
  ./helloworld.py: line 1: `print("Hello World")'
  ```

  - `sudo chmod a+x helloworld.py`로 실행 권한을 부여
  - 하지만 파일을 어떤 언어로 실행할지 아직 모르는 상태

  ```shell
  cabox@web2-python:~/workspace$ type python3
  python3 is hashed (/usr/bin/python3)
  ```

  - `type python3`로 python3가 설치된 경로 확인
  - 위 경로를 `helloworld.py` 첫줄에 입력하여 프로그램 언어 명기

  ```python
  #!/usr/bin/python3
  print("hello world")
  ```

  