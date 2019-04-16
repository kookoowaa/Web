# 04-1 Cloud 서버에 Django 배포하기

> - 다양한 클라우드 서비스가 존재하나 본 경우는 PythonAnywhere를 사용할 예정



## 1. Python Anywhere 사이트에 가입하기

- 특별히 언급할만한 내용은 없음
- http://www.pythonanywhere.com 에서 계정 등록하고 컨펌하여 클라우드 서비스 이용 가능
- 무료로 사용하는데는 제약 사항이 있으나 본 케이스에는 크게 문제 없음



## 2. 장고 소스 가져오기

- 지금까지 사용해온 장고 소스를 `~/ch5/`에서 `~/ch7/`으로 복사
- 윈도우 환경에서  PythonAnywhere 서버로 업로드가 가능하나 Git을 사용하여 소스 코드 가져오기
- 수정된 작업 환경은 `/home/아이디/web/Django/ch7/`이 됨



## 3. 가상 환경 만들기

- 파이썬 프로그램 및 라이브러리 사용을 통일시키고 충돌을 방지하기 위해서 가상 환경 하에 프로젝트 진행

- 리눅스 상 파이썬 3.6 가상환경은 아래와 같이 생성 가능:

  ```bash
  # 가상 환경을 모아 둘 디렉토리 VENV를 만들고 이동
  $ cd /home/사용자명/
  $ mkdir VENV
  $ cd VENV
  
  # 파이썬 3.6을 사용하는 가상환경 v3pybook 생성 > 3.7 버전 사용
  # $ virtualenv --python python3.6 v3pybook
  $ virtualenv --python python3.7 v3pybook
  
  # v3pybook 가상환경 안으로 진입
  $ source /home/kookoowaa/VENV/v3pybook/bin/activate
  
  # 가상 환경 내에 있다는 것을 알려주기 위해 프롬프트 상에 (v3pybook)이 표시됨
  # 파이썬 버전 확인
  (v3pybook) $ python -V
  
  # 가상환경에서 빠져나오기
  (v3pybook) $ deactivate
  ```

- 가상환경을 만들었으니 이후 작업은 가상환경 내에서 실행

- 우선 Django(및 기타 라이브러리) 부터 설치:

  ```bash
  # 가상환경 진입
  $ source /home/kookoowaa/VENV/v3pybook/bin/activate
  
  # 장고 2.0 설치 > 2.2 설치
  # (v3pybook) $ pip install Django==2.0
  (v3pybook) $ pip install Django
  
  # v3pybook 가상환경에 설치된 패키지 리스트 확인
  (v3pybook) $ pip list
  
  package		  version
  -----------	  -----------
  Django        2.2
  pip           19.0.3
  pytz          2019.1
  setuptools    41.0.0
  sqlparse      0.3.0
  wheel         0.33.1
  ```



## 4. PythonAnywhere 서버에서 장고 설정 변경하기

- 기존의 개발용 서버와는 다르게 웹서버에서 장고 프로그램을 실행하기 위해서는 일부 설정을 변경해야 함

- 여기서는 PythonAnywhere 서버가 에러없이 동작할 정도로 장고 설정을 2부분만 변경하나, 향후 보안을 고려하면 제대로 이해하고 넘어갈 필요가 있음:

  ```python
  # /ch7/mysite/settings.py
  
  ...
  ALLOWED_HOSTS = ['사용자명.pythonanywhere.com', 'localhost', '127.0.0.1']    # 추가
  ...
  
  ...
  STATIC_URL = '/static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'www_dir', 'static')    # 추가
  ...
  ```

- 설정 파일을 변경한 후에는 정적 파일을 모으기 위해 `collectstatic` 명령을 실행

  ```bash
  # ~Web/Django/ch7/
  (v3pybook) $ python manage.py collectstatic
  ```



## 5. PythonAnywhere 웹 서버 설정하기

- 서버 H/W에서 웹 서버를  인식하기 위해서 웹 서버의 설정을 변경해야 하며, 우선적으로 Web app을 생성해야 함 (도메인명은 `사용자명.pythonanywhere.com`이 됨)
- 설정 마법사를 따라 가면 되며, 본 경우와 같이 가상환경을 사용하는 경우 Manual configuration으로 진행하면 됨
- 이 단계부터 기동되는 PythonAnywhere 웹서버에 개발한 장고 프로그램을 실행하기 위해서는 **Code, Virtualenv, Static files** 3개 섹션의 내용을 프로젝트에 맞추어 수정해 주어야 함

> ### Code
>
> - Code 섹션에서는 **WSGI configuration file**(`사용자명_pythonanywhere_com_wsgi.py`)의 내용을 수정해야 함
>
>   ```python
>   import os
>   import sys
>   
>   # project root directory
>   path = '/home/사용자명/web/Django/ch7'
>   if path not in sys.path:
>       sys.path.append(path)
>   
>   os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
>   
>   from django.core.wsgi import get_wsgi_application
>   application = get_wsgi_application()
>   ```

	> ### Virtualenv
	>
	> - Virtualenv 섹션에서는 앞서 만든 가상 환경을 등록
	> - 여기서는 `v3pybook` 가상환경의 루트 디렉토리인 `/home/사용자명/VENV/v3pybook/`을 등록

	> ### Static files
	>
	> - Static files 섹션에서는 `settings.py`에서 정의한 내용을 그대로 기입
	>
	> - URL에는 `STATIC_URL` 값을, Directory에는 `STATIC_ROOT` 값을 등록
	>
	>   ```python
	>   # /ch7/mysite/settings.py
	>   
	>   ...
	>   STATIC_URL = '/static/'
	>   STATIC_ROOT = os.path.join(BASE_DIR, 'www_dir', 'static')
	>   ```

- 여기까지 완료하였으면 reload 하였을 시 정상적으로 홈페이지를 반환

