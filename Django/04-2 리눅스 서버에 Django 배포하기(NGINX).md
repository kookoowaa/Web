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

