# 03-3 polls 어플리케이션 - 클래스형 뷰로 변환

- 앞서 작성한 `polls` 어플리케이션은 개발 초기 단계에 이해하기 쉬운 함수형 뷰로 코딩
- 이번에는 기 작성된 함수형 뷰를 클래스형 뷰로 전환

___

## 1. URLconf 코딩하기

- 모델 코딩은 제외, 바로 URLconf부터 시작

  | URL 패턴          | 기존 뷰 이름(함수) | 새로운 뷰 이름(클래스) | 변경사항                            |
  | ----------------- | ------------------ | ---------------------- | ----------------------------------- |
  | /polls/           | index()            | IndexView              | 뷰와 템플릿 모두 변경(index.html)   |
  | /polls/99/        | detail()           | DetailView             | 뷰와 템플릿 모두 변경(detail.html)  |
  | /polls/99/results | results()          | ResultsView            | 뷰와 템플릿 모두 변경(results.html) |
  | /polls/99/votes   | vote()             | vote()                 | 뷰와 템플릿 모두 변경사항 없음      |

- `polls/url.py` 파일은 다음과 같이 수정:

  ```python
  # polls/url.py
  
  from django.urls import path
  from . import views
  
  app_name='polls'
  urlpatterns = [
      # /polls/
      #path('', views.index, name = 'index'),
      path('', views.IndexView.as_view(), name ='index'),
  
      #/polls/99/
      #path('<int:question_id>/', views.detail, name='detail'),
      path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  
      #/polls/99/results/
      #path('<int:question_id>/results', views.results, name='results'),
      path('<int:pk>/results', views.ResultsView.as_view(), name='results'),
  
      #/polls/99/detail/
      path('<int:question_id>/vote/', views.vote, name='vote'),   
  ]
  ```

  > 1. 뷰 이름이 클래스형 뷰로 변경됨
  > 2. URL 패턴의 파라미터 이름이 `question_id`에서 `pk`로 변경되었고, 이는 제네릭뷰의 동작 방식 때문임 (제네릭뷰는 특정 레코드를 조회하는 경우 pk로 검색)

## 2. View 코딩하기

