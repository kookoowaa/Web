# ch 3-1

1. Table books/publisher not found (비슷한 에러 메세지)
   - db 마이그레이션 여부 재확인
   - `python manage.py makemigration, python manage.py migrate`로 문제 해결
2. `NoReverseMatch at /books/`, "Reverse for 'publisher_list' not found" (index.html 접근 시)
   - NoReverseMatch 에러는장고가 적절한 url 패턴을 찾지 못하였을 시 발생
   - 본 경우는 `/ch5/books/urls.py`에서 `path('publisher/', views.PublisherList.as_view(), name='publisher_lsit')`로 잘못 표기되어 에러가 발생
   - 다시 얘기하면 타겟 url 뿐 아니라 어플리케이션 내 url 중 하나가 잘못 매핑 되어도 에러 발생

# ch 3-2

1. 프로젝트 첫페이지에 접속은 가능하나, 아무 어플도 뜨지 않는 상태
   - View 파일 내 오타 없는 지 확인
   - 특히 View 코드 내 `context['컨텍스트 변수명']` 부분과 템플릿 코드 내 `{% for appname in 컨텍스트 변수명` %}이 일치하는 지 재차 확인 필요

