# Django 웹 프레임워크

## Django에서의 어플리케이션 개발 방식

- 웹을 개발할 때 가장 먼저 해야 할 일은 프로그램이 해야 할 일을 적당한 크기로 나누어서 **모듈화 하는 것**
- 이 때 전체 프로그램 또는 모듈화된 단위 프로그램을 어플리케이션이라고 함
- Django에서는 전체 프로그램을 **프로젝트<sup>Project</sup>**, 모듈화된 단위 프로그램을 **어플리케이션<sup>Application</sup>**으로 명명
- 또 하나 알아둘 것은 **MVC<sup>Model-View-Controller</sup>**패턴으로 데이터<sup>Model, </sup>사용자 인터페이스<sup>View</sup>, 데이터를 처리하는 로직<sup>Controller</sup>을 구분해서 한 요소가 다른 요소들에 영향을 주지 않도록 설계하는 방식
- Django에서는 동일한 개념을 MVT<sup>Model-View-Template</sup>로 명명하며, 템플렛<sup>Template</sup>은 사용자에게 보여지는 UI 부분을, 뷰<sup>View</sup>는 실질적으로 프로그램 로직이 동작하고 결과를 템플릿에 전달하는 역할을 수행

추후 업데이트 예정

___

## 어플리케이션 설계하기

- 위에서 한차례 언급한 바와 같이 파이썬을 활용한 웹개발은 프로젝트와 프로젝트를 몇 개의 기능 그룹으로 나눈 어플리케이션으로 구분할 수 있음
- 결국 어플리케이션을 개발하고, 이들을 모아서 프로젝트 개발을 완성
- 이런 개념은 하나의 어플리케이션이 여러 개의 프로젝트에 포함될 수 있기 때문에 생산성 측면에서 의미가 있음

<br>

- 본 예제에서 개발하게 될 어플리케이션의 내용은 1) 설문에 해당하는 질문을 보여준 후 2) 질문에 포함되어 있는 답변 항목에 투표하면 3) 그 결과를 알려주는 예제임

- 총 3개의 페이지 개발이 필요할 것으로 설계:

  > - index.html: 최근에 실시하고 있는 질문 리스트를 보여줌
  > - detail.html: 질문에 대한 답변 리스트를 폼으로 보여줌
  > - result.html: 질문에 따른 투표 결과를 보여줌

- 위 요구사항에 따라 2종의 데이터 테이블 설계가 필요:

  > **Question table**: 질문을 저장하는 테이블
  >
  > | 컬럼명        | 타입         | 제약조건                   | 설명           |
  > | ------------- | ------------ | -------------------------- | -------------- |
  > | id            | integer      | NotNull, PK, AutoIncrement | Primary Key    |
  > | question_text | varchar(200) | NotNull                    | 질문 문장      |
  > | pub_date      | datetime     | NotNull                    | 질문 생성 시각 |
  >
  > 
  >
  > **Choice table**: 질문 별 선택용 답변 항목을 저장하는 테이블
  >
  > | 컬럼명      | 타입         | 제약조건                         | 설명           |
  > | ----------- | ------------ | -------------------------------- | -------------- |
  > | id          | integer      | NotNull, PK, AutoINcrement       | Primary Key    |
  > | choice_text | varchar(200) | NotNull                          | 답변 항목 문구 |
  > | votes       | integer      | NotNull                          | 투표 카운트    |
  > | question    | integer      | NotNull, FK (Question.id), index | Foreign Key    |
  >
  > - PK는 자동 증가 속성으로 지정
  > - Choice table의 question 칼럼은 Question table과 FK 관계로 연결 (+index 생성)

  ___

  ## 프로젝트 뼈대 만들기

  - 코딩은 프로젝트 뼈대를 만드는 것부터 시작. 즉, 디렉토리 및 파일을 구성하고 설정 파일을 세팅
  - 그 외에 기본 테이블을 생성하고, 관리자 계정인 슈퍼유저를 생성
  - 하위 어플리케이션 디렉토리 및 파일까지 구성
  - 뼈대가 완성된 후의 디렉토리 체계는 아래와 같음

  | 프로젝트 | 파일 및 어플리케이션(1) | 어플리케이션(2) 및 어플리케이션 파일(1) | 어플리케이션 파일(2) |
  | -------- | ----------------------- | --------------------------------------- | -------------------- |
  | ch3      | `db.sqlite3`            |                                         |                      |
  |          | `manage.py`             |                                         |                      |
  |          | mysite                  | `__init__.py`                           |                      |
  |          |                         | `settings.py`                           |                      |
  |          |                         | `urls.py`                               |                      |
  |          |                         | `wsgi.py`                               |                      |
  |          | polls                   | `__init__.py`                           |                      |
  |          |                         | `admin.py`                              |                      |
  |          |                         | `apps.py`                               |                      |
  |          |                         | migrations                              | `__init__.py`        |
  |          |                         | `models.py`                             |                      |
  |          |                         | `tests.py`                              |                      |
  |          |                         | `views.py`                              |                      |

  - 위의 디렉토리는 뼈대에 해당하는 것으로, 완성 후 templates, static, log 등의 디렉토리가 추가로 필요
  - 위 뼈대의 객체 별 설명은 다음과 같음

  | 항목명          | 구분         | 설명                                                         |
  | --------------- | ------------ | ------------------------------------------------------------ |
  | **ch3**         | **디렉토리** | 프로젝트 관련 디렉토리 및 파일을 모아주는 최상위 루트 디렉토리<br />보통 `settings.py`파일의 BASE_DIR 항목으로 지정 |
  | db.sqlite3      | 파일         | SQLite3 데이터베이스 파일로 테이블이 존재                    |
  | manage.py       | 파일         | Django의 명령어를 처리하는 파일                              |
  | **mysite**      | **디렉토리** | 프로젝트명으로 만들어진 디렉토리로 프로젝트 관련 파일들이 위치 |
  | \_\_init\_\_.py | 파일         | 디렉토리에 이 파일이 있으면 파이썬 패키지로 인식             |
  | settings.py     | 파일         | 프로젝트 설정 파일                                           |
  | urls.py         | 파일         | 프로젝트 레벨의 URL 패턴을 정의하는 최상위 URLconf<br />보통은 어플리케이션 레벨마다 하위 urls.py 파일 존재 |
  | wsgi.py         | 파일         | Apache와 같은 웹 서버와 WSGI 규격으로 연동하기 위한 파일     |
  | **polls**       | **디렉토리** | 어플리케이션명으로 만들어진 어플리케이션 디렉토리<br />해당 어플리케이션 관련 파일 위치 |
  | \_\_init\_\_.py | 파일         | 디렉토리에 이 파일이 있으면 파이썬 패키지로 인식             |
  | admin.py        | 파일         | Admin  사이트에 모델 클래스를 등록                           |
  | apps.py         | 파일         | 어플리케이션 설정 클래스를 정의하는 파일                     |
  | **migrations**  | **디렉토리** | db 변경사항을 관리하기 위한 디렉토리<br />db에 추가, 삭제, 변경 등이 발생하면 변경 내역을 기록 |
  | models.py       | 파일         | db 모델 클래스를 정의하는 파일                               |
  | tests.py        | 파일         | 단위 테스트용 파일                                           |
  | views.py        | 파일         | 뷰 함수를 정의하는 파일 (함수형 뷰 및 클래스형 뷰)           |
  | **templates**   | **디렉토리** | 프로젝트를 진행하면서 추가<br />템플릿 파일이 위치<br />프로젝트 레벨과 어플리케이션 레벨의 템플릿으로 구분하여 별도 생성 |
  | **static**      | **디렉토리** | 프로젝트를 진행하면서 추가<br />CSS, Image, JavaScript 파일등이 위치<br />프로젝트 레벨과 어플리케이션 레벨로 구분하여 별도 생성 |
  | **logs**        | **디렉토리** | 프로젝트를 진행하면서 추가<br />로그파일이 위치<br />로그 파일의 위치는 settings.py 파일의 LOGGING 항목으로 지정 |

  - 위와 같은 뼈대 구축을 위해 다음 순서로 명령을 실행

    ```shell
    >django-admin startproject mysite		// mysite라는 프로젝트 생성
    >python manage.py startapp polls	    // polls라는 어플리케이션 생성
    >notepad settings.py				   // 설정파일을 확인 및 수정
    >python manage.py migrate			   // db에 기본 테이블을 생성
    >python manage.py runserver			   // 현재까지 작업을 개발용 웹 서버로 확인
    ```

  ___

  ### 1. 프로젝트 생성

  - 아래 명령어로 프로젝트 생성

    ```
    ~Git\Web\Django> Django-admin startproject mysite
    ```

  - 실행 결과 mysite라는 디렉토리와, 그 안에 필요한 디렉토리 및 파일을 생성

  - 하위에도 **mysite**라는 디렉토리가 하나 있는데 이는 프로젝트 디렉토리이며, 상위 디렉토리는 프로젝트 관련 디렉토리/파일을 모으는 역할로, mysite에서 ch3라는 이름으로 변경하여 혼선을 방지

    ```
    ~Git\Web\Django> move mysite ch3
    ```

  ___

  ### 2. 어플리케이션 생성

  - 새롭게 생성한 `ch3` 프로젝트 루트 디렉토리로 이동해서 **polls**라는 어플리케이션 생성

    ```
    ~Git\Web\Django\ch3> python manage.py startapp polls
    ```

  - 새롭게 생성된 `polls` 어플리케이션 디렉토리를 보면 Django에서 어플리케이션 개발에 반드시 필요한 파일을 자동으로 생성

  ___

  ### 3. 프로젝트 설정파일 변경

  - 프로젝트에 필요한 설정값은 `settings.py`에 저장되어 있으며, 해당 파일은 프로젝트 디렉토리(`mysite`)에서 확인 가능

  - `setting.py`는 전반적인 프로젝트 사항들을 설정해주며, 루트 디렉토리를 포함한 각종 디렉토리의 위치, 로그의 형식, 어플리케이션 명칭 등이 지정되어 있음

  - 본 예제에서는 크게 4종의 설정 사항을 확인

    ___

    > #### 1) 접속 주소
    >
    > - `DEBUG = True`이면 개발모드로, `DEBUG = False`면 운영모드로 인식
    > - 개발모드에서는 별도 지정 없이도 ['localhost', '127.0.0.1']로 접속 가능
    > - 운영모드에서는 `ALLOWED_HOSTS` 항목을 적절하게 지정할 필요가 있음
    > - 예를들어 장고의 runserver를 기동할 서버의 IP가 `127.0.0.1`외에 `192.168.56.101`일수도 있다면 아래와 같이 지정
    >
    > ```
    > ALLOWED_HOSTS = ['192.168.56.101', 'localhost', '127.0.0.1']
    > ```

    > #### 2) 어플리케이션 등록
    >
    > - 프로젝트에 포함되는 어플리케이션들은 모두 설정 파일에 드옥되어야 함
    > - 간단하게 `polls`만 등록해도 되지만, 어플리케이션의 설정 클래스로 등록하는 것이 더 정확한 방법 (`start app` 명령시 자동 생성된 `app.py` 파일에 정의)
    >
    > ```
    > INSTALLED_APPS = [
    >     'django.contrib.admin',
    >     'django.contrib.auth',
    >     'django.contrib.contenttypes',
    >     'django.contrib.sessions',
    >     'django.contrib.messages',
    >     'django.contrib.staticfiles',
    >     'polls.apps.PollsConfig'
    > ]
    > ```

    > #### 3) db엔진 설정
    >
    > - Django는 디폴트로 **SQLite3**엔진을 사용하도록 설정
    > - 다른 db엔진을 사용하려면 변경가능하며, 본 예제에서는 확인만 하고 넘어감
    >
    > ```
    > DATABASES = {
    >     'default': {
    >         'ENGINE': 'django.db.backends.sqlite3',
    >         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    >     }
    > }
    > ```

    > #### 4) 타임존 지정
    >
    > - 디폴트는 세계표준시(UTC)로 되어 있으며, 한국시간으로 변경
    > - `USE_TZ = True`로 설정 시 장고에서 알아서 시간대를 조정해 주나, 이는 db에는 UTC, 폼처리 및 출력시에는 `TIME_ZONE` 시간대를 반영하는 방식
    > - Django에서는 `USE_TZ = True`를 권장하나, 썸머타임이 없는 한국에서는 이를 `False`로 설정하는게 좀 더 편리
    >
    > ```
    > #TIME_ZONE = 'UTC'
    > TIME_ZONE = 'Asia/Seoul'
    > ```

    ___

    ### 4. 기본 테이블 생성

    -  비록 db 작업 전이지만 기본 테이블 생성을 위하여 아래 명령을 실행

      ```
      ~Git\Web\Django\ch3> python manage.py migrate
      ```

    - Django는 웹 개발 시 반드시 사용자와 그룹테이블 등이 필요하다고 판단하고, 프로젝트 개발 시작 시점에 이명령을 실행토록 함
    - `migrate` 명령에 따라 로그를 확인 가능하고, `db.sqlite3`파일이 생성된 것을 확인 가능

    ___

    ### 5. 작업 확인하기

    - 기본작업 후 `runserver`명령을 통해 간단한 테스트용 웹서버 실행 가능

      ```
      ~Git\Web\Django\ch3> python manage.py runserver 0.0.0.0:8000 // 또는 0:8000
      
      ~Git\Web\Django\ch3> python manage.py runserver              // 127.0.0.1:8000 사용
      ~Git\Web\Django\ch3> python manage.py runserver 8888         // 127.0.0.1:8888 사용
      $ python manage.py runserver 0.0.0.0:8000 &                  // 백그라운드에서 실행(리눅스)
      ```

    - `0.0.0.0`이란 IP 주소의 의미는 현재 명령을 실행중인 서버의 IP 주소가 무엇으로 설정되어 있더라도 그와 무관하게 웹 접속 요청을 받겠다는 의미
    - 
