# 어플리케이션 개발하기

- 모델 작업은 데이터베이스에 테이블을 생성하는 작업으로 다음 순서를 따름:

  ```
  > notepad models.py					// 테이블 정의
  > notepad admins.py					// 정의된 테이블을 Admin 화면에 제공
  > python manage.py makemigrations	 // db에 변경이 필요한 사항을 추출
  > python manage.py migrate			// db에 변경 사항을 반영
  > python manage.py runserver		// 개발용 웹서버로 진행사항 확인
  ```

___

## 1. 테이블 정의

- `polls` 어플리케이션은 Question과 Choice 두 개의 테이블이 필요하며 이는 `models.py`파일에 정의

  ```python
  from django.db import models
  
  
  class Question(models.Model):
      question_text = models.CharField(max_length=200)
      pub_date = models.DateTimeField("date published")
  
      def __str__(self):
          return self.question_text
  
  
  class Choice(models.Model):
      question = models.ForeignKey(Question, on_delete = models.CASCADE)
      choice_text  = models.CharField(max_length=200)
      votes = models.IntegerField(default = 0)
  
      def __str__(self):
          return self.choice_text
  ```

- Django에서 "테이블은 하나의 클래스"로, "컬럼은 클래스의 변수"로 정의하여 매핑

- 위 정의에서 Question 테이블 정의한 내용을 살펴보면 다음과 같음:

  | 컬럼          | 컬럼타입     | 장고의 클래스변수 | 장고의 필드클래스                      |
  | ------------- | ------------ | ----------------- | -------------------------------------- |
  | id            | integer      | (id)              | (PK는 자동생성)                        |
  | question_text | varchar(200) | question_text     | models.CharField(max_length=200)       |
  | pub_date      | datetime     | pub_date          | models.DateTimeField('date published') |

  > - PK는 클래스에 지정하지 않아도 항상 No Null 및 Autoincrement, 이름은 id로 자동 생성
  > - `models.DateTimeField('date published')`에서 'date published'는 레이블 문구

- Choice 테이블 정의한 내용을 살펴보면 다음과 같음:

  | 컬럼        | 타입         | 장고의 클래스변수 | 장고의 필드클래스                |
  | ----------- | ------------ | ----------------- | -------------------------------- |
  | id          | integer      | (id)              | (PK는 장고에서 자동 생성)        |
  | choice_text | varchar(200) | choice_text       | models.CharField(max_length=200) |
  | votes       | integer      | votes             | models.IntegerField(default=0)   |
  | question_id | integer      | question          | models.ForeignKey(Question)      |

  > - FK는 항상 다른 테이블의 PK에 연결되므로, Question클래스의 id 변수까지 지정할 필요는 없음
  > - FK로 지정된 컬럼은 '_id' 접미사가 붙게 됨
  > - `__str__()` 메소드는 객체를 문자열로 표현할 때 사용하는 함수 (Admin 사이트나 장고 쉘)

  

___

## 2. Admin 사이트에 테이블 반영

- 아직까지는 Admin 사이트에 접속해 보면 'Users', 'Groups' 테이블만 확인 가능

- `admin.py`파일에 위에서 만든 테이블(class)를 등록하여 Admin 사이트에서도 볼 수 있도록 함

  ```python
  from django.contrib import admin
  
  # Register your models here.
  
  from polls.models import Question, Choice
  
  admin.site.register(Question)
  admin.site.register(Choice)
  ```

  - `models.py`모듈에서 정의한 Question, Choice 클래스를 임포트
  - `admin.site.register()`함수를 사용하여 임포트한 클래스를 admin 사이트에 등록

- 위와 같이 테이블을 만들 때에는 `models.py`와 `admin.py` 두개의 파일을 함께 수정해야 함



___

## 3. 데이터베이스 변경사항 반영

- 위 단계까지는 클래스로 테이블 정으만 변경한 상태

- 테이블의 신규 생성, 정의변경 등 db에 변경이 필요한 사항이 있으면, 이를 db에 실제로 반영해주어야 함

- 아래 명령으로 변경사항을 db에 반영

  ```
  ~Django\ch3> python manage.py makemigrations
  ~Django\ch3> python manage.py migrate
  ```

- `makemigrations`명령으로 polls/migrations 디렉토리 하위에 마이그레이션 파일 생성 (본 예제에서는 `0001_initial.py`)

- 위 마이그레이션 파일을 이용해 `migrate`명령으로 db에 테이블 생성

- 변경 작업 에 대한 sql 로그는 아래 명령으로 확인 가능

  ```
  ~Django\ch3> python manage.py sqlmigrate polls 0001
  ```

  

___

## 4. 작업 확인하기

- 개발용 웹서버로 변경사항을 확인하면 (Admin 사이트), Users, Groups 이외에 Questions와 Choice 테이블 확인 가능



