# 3. Django 관리자

- 장고의 관리자 화면을 한국어로 변경하기 위해서 아래와 같이 `settings.py` 수정
```python
#mysite/settings.py ln 107]

LANGUAGE_CODE = 'ko'
```

- 웹 서버를 실행하려면 `djangogirls` 가상환경으로 들어가 아래와 같이 콘솔 명령어 실행:
```shell
~Django-Girls> djangogirls\Scripts\activate
(djangogirls) ~Django-Girls> python manage.py runserver

Performing system checks...

System check identified no issues (0 silenced).
July 30, 2019 - 01:30:24
Django version 2.0.13, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
- 실행하게 되면 아래와 같이 서버가 작동되는 것을 확인

- 서버는 http://127.0.0.1:8000/ 에서 확인이 가능하며, 관리자 페이지는 http://127.0.0.1:8000/admin/ 에서 확인 가능
- 단, superuser를 생성해야 로그인이 가능한데, 이는 가상환경에서 아래 커맨드를 입력하여 생성 가능
```shell
(djangogirls) ~Django-Girls> python manage.py createsuperuser
Username (leave blank to use 'pablo'): !@#$%^&*
Email address: !@#$$%^&@gmail.com
Password:
Password (again):
Superuser created successfully.
```
- 위에서 지정한 superuser로 접속하게 되면 아래와 같은 화면에 접속이 가능
![](md_src/django_admin.png)
