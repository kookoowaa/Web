# 장고 모델
> - 장고 모델은 객체 지향 프로그래밍이며, 여기서 **객체는 속성<sup>property</sup>와 행동<sup>method</sup>**으로 구성
> - 예를 들어 **"블로그 글"이란 객체**는 **"제목", "내용", "글쓴이", "작성일"과 같은 속성**과 **"게시", "수정", "삭제"와 같은 행동**으로 구성

## 1. 어플리케이션 만들기
- 관리 편의성을 위해 프로젝트 내부에 별도의 어플리케이션을 만들어서 모델 관리
- 어플리케이션 생성은 아래 콘솔 명령어로 실행:
```shell
(djangogirls) ~Django-Girls> python manage.py startapp blog
```
- 이를 통해 생성된 디렉터리와 파일은 다음과 같은 트리를 보유:
```shell
djangogirls
├── mysite
|       __init__.py
|       settings.py
|       urls.py
|       wsgi.py
├── manage.py
└── blog
    ├── migrations
    |       __init__.py
    ├── __init__.py
    ├── admin.py
    ├── models.py
    ├── tests.py
    └── views.py
```
- 어플리케이션 생성 이후엔 `mysite/settings.py`에서 어플리케이션 사용을 추가할 필요가 있음
```python
#mysite/settings.py ln40]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]
```

## 2. 블로그 글 모델 만들기

- **모든 `model` 객체는 `blog/models.py`파일에 선언하여 모델을 생성**
- `blog/models.py`파일을 열어 모든 내용을 삭제한 후 아래 내용을 추가

```python
#blog/models.py

from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
```

> 1. `Post`는 `blog` 어플리케이션에서 정의하는 모델로, `models.Model`을 통해 `Post`가 장고 모델임을 정의하여 db에 저장되어야 함을 알려줌
> 2. `Post`에서 정의하는 속성<sup>property</sup>은 (`author`, `title`, `text`, `created_date`, `published_date`)가 있으며, `models.ForeignKey()`, `models.CharField()` 등등으로 데이터 타입을 정의
> 3. `Post`에서 정의하는 행동<sup>method</sup>은 `publish`와 `__str__`이 있음

## 3. 데이터베이스에 모델을 위한 테이블 만들기

- 데이터베이스에 `Post` 모델을 추가하기 위해 콘솔 명령을 통해 장고에 이를 선언할 필요가 있음:

```shell
~ djangogirls> python manage.py makemigrations blog
```

- 추가로 아래 명령을 통해 실제 데이터베이스에 모델 추가를 반영

```shell
~ djangogirls> python manage.py migrate blog
```

## 4. 모델 등록하기

- 위에서 정의한 모델들을 사용하려면 `blog/admin.py`에 작성한 모델들을 불러와야 함
```python
#blog/admin.py ln 3]

# Register your models here.
from .models import Post
admin.site.register(Post)
```
- 코드에서 알 수 있듯이 `Post` 모델을 `import` 명령어로 가져오고, `admin.site.register(Post)`로 모델을 등록
