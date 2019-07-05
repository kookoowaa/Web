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
