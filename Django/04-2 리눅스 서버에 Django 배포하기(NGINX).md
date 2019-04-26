# 04-2  리눅스 서버에 Django 배포하기 (NGINX)

- **NGINX**는 Apache 웹서버의 단점으로 지적된 동시 처리 능력을 높이고 메모리를 적게 사용하는 방향으로 설계된 무료 오픈소스 웹 서버
- Apache<sup>httpd</sup>도 전 세계에서 운영중인 웹사이트의 50% 이상이 사용할 정도로 인기있는 웹 서버이나, 새로 구축하는 사이트는 NGINX를 더 많이 사용하는 추세 (단순 + 확장 용이)

___

## 1. 장고 설정 변경하기

- 운영 환경에서 웹서버와 Django를 연동하기 위해서는 아래와 같이 장고의 설정을 몇가지 변경해야 함:

  > 0. 파이썬 3.x 버전을 사용하는 가상환경 구축
  > 1. `settings.py` 파일의 DEBUG 변경
  > 2. `settings.py` 파일의 ALLOWED_HOSTS 변경
  > 3. `settings.py` 파일의 STATIC_ROOT 추가
  > 4. `collectstatic` 명령 실행 (가상환경에서)
  > 5. `vi www_dir/secret_key.txt` 파일 생성 및 `SECRET_KEY` 저장
  > 6. `settings.py` 파일의 `SECRET_KEY` 변경
  > 7. `db.sqlite3` 파일의 위치 및 권한 변경
  > 8. 로그 파일의 권한 변경


> 1~3. `settings.py` 파일의 DEBUG 변경
>
> - `settings.py` 파일의 3개 항목을 아래와 같이 수정:
>
>   ```python
>   # ch8/mysite/settings.py
>   
>   ...
>   DEBUG = False    # 변경
>   
>   ALLOWED_HOSTS = ['192.168.56.101', 'localhost', '127.0.0.1']    # 변경
>   
>   ....
>   
>   STATIC_URL = '/static/'    
>   STATIC_ROOT = os.path.join(BASE_DIR, 'www_dir', 'static')    # 추가
>   ....
>   ```
>
> 4. `collectstatic` 명령 실행
>
>    ```bash
>    $ source ~/VENV/v3pybook/bin/activate
>    (v3pybook) $ python manage.py collectstatic
>    ```
>
> - 위 명령의 결과로 `STATIC_ROOT`에서 정의된 `www_dir` 디렉토리도 생성
>
> 5~6. `SECRET_KEY`저장 및 변경
>
> - `SECRET_KEY`가 노출되지 않도록 별도의 파일에 저장
>
> - `settings.py` 파일에서 `SECRET_KEY` 문자열을 복사한 후 아래처럼 `/ch8/www_dir/secret_key.txt` 파일에 저장
>
>   ```python
>   # /ch8/www_dir/secret_key.txt
>   
>   0f78el..irxb...&!9itbzl3w...g3&6+e2_ywap&-sps(xs(r
>   ```
>
> - `settings.py` 파일에서 기존의 `SECRET_KEY` 라인을 삭제하고 `secret_key.txt`파일에서 읽어오는 코드를 추가
>
>   ```python
>   # mysite/settings.py
>   
>   # SECURITY WARNING: keey the secrey key used in production secret!
>   with open(os.path.join(BASE_DIR, 'www_dir', 'secret_key.txt')) as f:
>      SECRET_KEY = f.read().strip()
>   ```
>
> 7. SQLite3 파일의 위치 및 권한 변경
>
>    ```python
>    # mysite/settings.py
>    
>    DATABASE = {
>        ...
>        'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),		# 변경
>    }
>    ```
>
> - 이후 엑세스 권한을 아래처럼 변경
>
>   ```bash
>   $ cd ~/web/Django/ch8/
>   $ mkdir db
>   $ mv db.sqlite3 db/
>   $ chmod 777 db/
>   $ chmod 666 db/db.sqlite3
>   ```
>
> 8. 로그 파일의 액세스 권한 변경
>
>    ```bash
>    $ cd ~/web/Django/ch8/
>    $ chmod 777 logs/
>    $ chmod 666 logs/mysite.log
>    ```

___

## 2. NGINX 설치

- NGINX 공식 사이트에는 다양한 설치 방법이 나와 있으니 참조하여 설치

  ```bash
  $ sudo apt-get update
  $ sudo apt-get install nginx
  ```

- 공식 사이트는 https://docs.nginx.com 이며, **NGINX Plus> Admin Guide> Installing NGINX and NGINX Plus** 에서 상세정보 확인 가능

- 본 경우는 `NGINX Open Source`, `Stable 버전`, `Prebuilt(컴파일 완료)`, `UBUNTU(18.04 bionic)`을 사용

- NGINX 기동 및 확인은 아래와 같이 가능

  ```bash
  $ sudo nginx
  $ curl -I 127.0.0.1
  
  HTTP/1.1 200 OK
  Server: nginx/1.14.0
  .....
  ```

- 주요 NGINX 명령어는 다음과 같음

  | 명령어                   | 기능                   |
  | ------------------------ | ---------------------- |
  | `$ sudo nginx`           | NGINX  기동            |
  | `$ sudo nginx -s stop`   | NGINX 정지             |
  | `$ sudo nginx -s reload` | NGINX 재기동           |
  | `$ sudo nginx -t`        | NGINX 설정 파일 테스트 |
  | `$ sudo nginx -h`        | NGINX 도움말           |

___

## 3. NGINX 설정

- NGINX 프로그램이 정상적으로 설치되었다면 WSGI 규격에 따른 uWSGI 프로그램과의 연동을 위한 설정 작업이 필요

- 아래와 같이 설정파일을 생성하여 작성:

  ```
  # /etc/nginx/conf.d/ch9_nginx.conf
  
  server {
  	listen 8000;
  	server_name 127.0.0.1;
  	
  	# access_log /var/log/nginx/codejob.co.kr_access.log;
  	# error_log /var/log/nginx/codejob.co.kr_error.log;
  	
  	location = /favicon.ico { access_log off; log_not_found off; }
  	
  	location /static/ {
  		root /home/kookoowaa/web/Django/ch9/www_dir;
  		# alias /home/kookoowaa/web/Django/ch9/www_dir/static/;
  	}
  	
      location / {
          include /home/kookoowaa/web/Django/ch9/www_dir/uwsgi_params;
          uwsgi_pass 127.0.0.1:8001;
          # uwsgi_pass unix://home/kookoowaa/web/Django/ch9/www_dir/ch9.sock;
      }
  	
  }
  ```

  > 1. `server { }` 블록을 정의하여 가상 서버 생성
  > 2. 8000 포트를 리슨
  > 3. `server_name`에서 IP 주소 및 도메인을 지정 (`35.243.122.5 `)
  > 4. URL이 `/favicon.ico`인 경우 액세스 로그에 기록하지 않음
  > 5. URL이 `/static/`으로 시작하는 경우 정적 파일이 저장된 곳의 루트 디렉토리를 지정
  > 6. URL이 `/`로 시작하는 경우 (위의 경우들 이외에) uwsgi 서버에 넘겨줄 파라미터를 지정하고, nginx에 uwsgi 프로그램으로 처리 위임

- 위의 작업 완료 후 기존 `default.conf`사용 방지를 위해 이름을 변경

  ```bash
  $ sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
  ```

- 추가로 NGINX 설치 때 같이 생성된 `uwsgi_params` 파일은 장고 프로젝트 내 디렉토리로 복사

  ```bash
  $ cp /etc/uwsgi/nginx/uwsgi_params /home/kookoowaa/web/Django/ch9/www_dir/
  ```

___

## 4. uWSGI 설치

- uWSGI 설치는 다음과 같이 실행:

  ```bash
  $ sudo apt-get install python-devel
  $ sudo apt-get install python3-pip
  $ sudo pip3 install uwsgi
  $ sudo apt-get install uwsgi-core
  ```

___

## 5. uSWGI 설정

- 장고 프로젝트 별로 하나의 설정 파일이 필요하며 vassals는 자식프로젝트를 의미하는 uWSGI의 용어임

- 설정은 아래와 같이 진행:

  ```
  # /etc/uwsgi/vassals/ch8_uwsgi.ini
  
  [uwsgi]
  chdir = /home/kookoowaa/web/Django/ch8
  home = /home/kookoowaa/VENV/v3pybook
  module = mysite.wsgi:application
  socket = :8001
  # socket = /home/kookoowaa/web/Django/ch8/www_dir/ch8.sock
  # chmod-socket =666
  master = True
  processes = 5
  pidfile = /tmp/ch8-master.pid
  vacuum = True
  max-requests = 5000
  daemonize = /var/log/uwsgi/ch8.log
  ```

  > 상단부터 각 라인별 의미는 다음과 같음
  >
  > 1. `chdir`: 장고 프로젝트의 루트 디렉토리
  > 2. `home`: 가상환경 루트 디렉토리, 가상환경을 사용하지 않으면 생략
  > 3. `module`: `wsgi.py` 파일의 모듈경로 및 application 변수명 (`:application` 부분은 생략 가능)
  > 4. `socket`: 웹서버와 통신할 소켓의 포트번호를 지정하며 이는 nginx 설정 파일의 `uwsgi_pass`항목의 포트 번호와 동일
  > 5. `# socket`: 웹 서버와 유닉스 도메인 소켓을 사용할 경우의 소켓파일 경로
  > 6. `# chmod-socket`:  nginx 및 uwsgi 프로세스가 쓰기 할수 있도록 권한 부여
  > 7. `master`: 별도의 마스터 프로세스가 기동되도록 지정
  > 8. `processes`: uwsgi 기동 시 자식 프로세스 5개 생성
  > 9. `pidfile`: 마스터 프로세스 ID를 저장할 파일
  > 10. `vacuum`: 프로세스 종료 시 소켓 파일을 포함하여 환경변수를 클리어
  > 11. `max-requests`: 현 프로세스에서 처리할 최대 요청개수
  > 12. `daemonize`: 백그라운드에서 프로세스가 실행되도록 데몬화 (로그파일 경로 지정)

- 위와 같이 파일이 준비되면 설정 파일에서 지정한 로그 파일을 생성하고 권한 부여

  ```bash
  $ sudo mkdir /var/log/uwsgi
  $ sudo touch /var/log/uwsgi/ch8.log
  $ sudo chmod 666 /var/log/uwsgi/ch8.log
  ```

- uWSGI 서버는 옵션이 꽤 많은 편이므로 위의 기본설정부터 천천히 학습

___

## 6. 지금까지 작업 확인하기



# *리눅스 서버 필요, GCP에서 확인하기 어려움*



