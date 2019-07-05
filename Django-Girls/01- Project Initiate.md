# 프로젝트 시작하기

## 1. 뼈대 세우기

- `Django-admin.py`를 통해 프로젝트의 기본적인 디렉토리와 파일을 생성

  ```shell
  (djangogirls) ~Django-Girls> django-admin.py startproject mysite .
  
  # 위 커맨드가 실행되지 않는다면, venv 상의 django-admin.py를 찾아서 직접 실행
  (djangogirls) ~Django-Girls> python djangogirls/Scripts/django-admin.py startproject mysite .
  ```

- 스크립트 실행 후에는 아래와 같은 디렉토리 구조를 확인 가능

  ```shell
  djangogirls
  ├───manage.py
  └───mysite
          settings.py
          urls.py
          wsgi.py
          __init__.py
  ```

- 주요 파일은 아래와 같은 기능을 수행

  | 파일명        | 기능                                     |
  | ------------- | ---------------------------------------- |
  | `manage.py`   | 스크립트로 사이트 관리를 보조            |
  | `settings.py` | 웹사이트 설정이 있는 파일                |
  | `urls.py`     | `urlresolver`가 사용하는 패턴목록을 포함 |

## 2. 설정 변경

- `mysite\settings.py`파일에서 시간, 정적파일 경로, 호스트 정도만 우선적으로 설정

- 시간은 정확한 시간을 확인하기 위해 `'UTC'`에서 `'Asia/Seoul'`로 변경

  ```python
  # mysite/settings.py ln]108
  
  TIME_ZONE = 'Asia/Seoul'
  ```

- 정적파일은 제일 하단의 `STATIC_URL` 밑에 `STATIC_ROOT` 항목을 추가

  ```python
  #mysite/settings.py ln]120
  
  STATIC_URL = '/static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'static')
  ```

- 마지막으로 `ALLOWED_HOSTS`에 어플리케이션을 배포할 호스트를 추가

  ```python
  #mysite/settings.py ln]28
  
  ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']
  ```

- 기존에 `ALLOWED_HOSTS`는 비어있는데, 이 경우 `['localhost', '127.0.0.1', '[::1]']`에 대해서 유효

## 3. 데이터베이스 설정하기

- 가장 기본적인 데이터베이스로 sqlite3를 사용 (`startproject` 명령어로 이미 sqlite3가 설치되어 있음)

- 블로그에 데이터베이스를 생성하기 위해서 콘솔 창에서 아래 코드를 실행:
```shell
(djangogirls) ~Django-Girls> python manage.py migrate
```

## 4. 작동 여부 확인
- 서버는 콘솔 명령을 통해 실행
```shell
(djangogirls) ~Django-Girls> python manage.py runserver
```
- 서버 작동 여부는 http://127.0.0.1:8000/ 에서 확인 가능
