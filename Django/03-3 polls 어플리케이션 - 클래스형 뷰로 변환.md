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

- 변경된 코드는 아래와 같음:

  ```python
  # polls/urls.py
  
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

  > 1. 뷰 이름을 클래스형 뷰로 변경
  > 2. url 패턴의 파라미터 이름이 `<int:question_id>` 에서 `<int:pk>`로 변경 (DetailView에서 테이블의 특정 레코드를 조회하는 경우 pk로 검색을 수행)



## 2. View 코딩하기

- 함수형 뷰에서 클래스형 뷰로 변경하는 과정은 실제로 View 코딩이 대부분을 차지

- 다만,  클래스형 제네릭뷰를 상속받을 것인 만큼 코딩량 자체는 오히려 줄어들 예정

- 본 어플리케이션의 로직은 분석해 보면, 아래의 표와 같은 제네릭 뷰를 사용하는 것이 가장 효율적이고 적절할 것

  | URL 패턴           | 기존 뷰 이름 | 신규 뷰 이름  | 제네릭 뷰 선택                                               |
  | ------------------ | ------------ | ------------- | ------------------------------------------------------------ |
  | /polls/            | `index()`    | `IndexView`   | 질문 리스트를 보여주는 로직이므로 `ListView`를 사용 (*테이블에서 복수의 레코드를 수집*) |
  | /polls/99/         | `detail()`   | `DetailView`  | 질문 하나에 대한 세부 정보를 보여주는 로직이므로 `DetailView`를 사용(*테이블에서 특정 레코드를 수집*) |
  | /polls/99/results/ | `results()`  | `ResultsView` | 위와 동일한 로직이므로 `DetailView`를 사용                   |
  | /polls/99/vote/    | `vote()`     | `vote()`      | 뷰와 템플릿 모두 변경사항 없음                               |

- 변경된 코드는 아래와 같음:

  ```python
  # polls/views.py
  
  from django.shortcuts import get_object_or_404, render
  from django.http import HttpResponseRedirect, HttpResponse
  from django.urls import reverse
  from django.views import generic
  
  from polls.models import Question, Choice
  
  
  #-- Class-based GenericView
  class IndexView(generic.ListView):
      template_name = 'polls/index.html'
      context_object_name = 'latest_question_list'
      def get_queryset(self):
          """최근 생성된 질문 5개를 반환함"""
          return Question.objects.order_by('-pub_date')[:5]
  
  class DetailView(generic.DetailView):
      model = Question
      template_name = 'polls/detail.html'
  
  class ResultsView(generic.DetailView):
      model = Question
      template_name = 'polls/results.html'
  
  
  #-- Function-based View
  def vote(request, question_id):
      question = get_object_or_404(Question, pk=question_id)
      try:
          selected_choice = question.choice_set.get(pk=request.POST['choice'])
      except(KeyError, Choice.DoesNotExist):
          ## 설문 투표 폼을 다시 보여준다
          return render(request, 'polls/detail.html', {
              'question': question,
              'error_message': "You did not select a choice"
          })
      else:
          selected_choice.votes += 1
          selected_choice.save()
          ## POST를 정상적으로 처리하였으면, 항상 리다이렉션 처리
          return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
  ```

  > 1. 클래스형 제네릭뷰를 사용하기 위해 `generic` 모듈 호출
  > 2. `IndexView`에서 사용한 `generic.ListView`는 테이블에 들어있는 모든 레코드를 가져와 구성하는 경우에는 테이블명(모델 클래스명)만 지정해 주면 되지만, 본 경우에는 `get_queryset()` 메소드를 오버라이딩으로 정의하여 원하는 리스트를 직접 구성
  > 3. 또한, 컨텍스트 변수명을 디폴트인 `object_list`대신 지정하여 사용
  > 4. `generic.DetailView`를 상속받는 경우는 테이블명(모델 클래스명)만 지정해줄 경우 자동으로 pk로 조회하여 시스템에 넘겨주게되며, pk 값은 URLconf에서 `pk` 파라미터 이름으로 넘겨 받아 자동으로 사용
  > 5. `ResultsView`에서도 `Choice`가 아닌 `Question` 테이블을 객체로 넘겨 받는데, 이는 로직이 1) `Question` 객체를 구한다, 2) ForeignKey로 연결된 `Choice`객체를 구한다 로 연결되기 때문임 (템플릿 파일에서 `question.choice_set.all()` 구문으로 구현)

## 3. Template 코딩하기

- 템플릿의 경우 기존에 사용하지 않았던 상속 기능을 추가

- 각 템플릿은 `base_polls.html`을 상속 받고, `base_polls.html`은 `base.html`을 상속 받음

- `base_polls.html`은 `~/templates/` 폴더에, 각 템플릿은 `~/polls/templates/polls/` 폴더에 각각 위치

- 먼저 `base_polls.html`은 아래와 같이 변경

  ```django
  {% extends "base.html" %}
  
  <title>{% block title %}Polls Application Site{% endblock %}</title>
  
  {% block sidebar %}
  {{ block.super }}
  <ul>
      <li><a href="/polls/">Polls_Home</a></li>
  </ul>
  {% endblock %}
  ```

  > - 타이틀, 링크 정도만 직접 변경

- `polls/index.html` 템플릿 파일은 다음과 같이 변경

  ```django
  {% extends "base_polls.html" %}
  
  {% block content %}
  
  <h2>Polls Question List</h2>
  
  {% if latest_question_list %}
  <ul>
      {% for question in latest_question_list %}
      <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
      {% endfor %}
  </ul>
  
  {% else %}
  <p>
      No polls are available.
  </p>
  
  {% endif %}
  {% endblock content %}
  ```

  > - 상속, content블록 정의, 제목 추가 정도 외에 기존 소스와 크게 달라진 점은 없음

- `polls/detail.html` 템플릿 파일은 다음과 같이 변경

  ```django
  {% extends "base_polls.html" %}
  
  {% block content %}
  
  <h1>{{ question.question_text }}</h1>
  
  {% if error_message %}<p>
      <strong>{{ error_message }}</strong>
  </p>{% endif %}
  
  <form action="{% url 'polls:vote' question.id %}" method="post">
      {% csrf_token %}
      {% for choice in question.choice_set.all %}
      <input type="radio" name="choice" id="choice{{ forloop.counter }}" value = "{{ choice.id }}" />
      <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
      {% endfor %}
      <input type="submit" value="Vote" />
  </form>
  
  {% endblock content %}
  ```

- `polls/results.html` 템플릿 파일은 다음과 같이 변경

  ```django
  {% extends "base_polls.html" %}
  
  {% block content %}
  
  <h1>{{ question.question_text }}</h1>
  
  <ul>
      {% for choice in question.choice_set.all %}
      <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
      {% endfor %}
  </ul>
  
  <a href="{% url 'polls:detail' question.id %}">Vote again?</a>
  
  {% endblock content %}
  ```


## 4. 로그 추가하기

- 앞장에서 생략했었지만, `settings.py` 설정을 조정하고 원하는 곳에서 로거의 메소드를 호출하는 것으로 로깅 시스템 적용 가능

- 우선 `settings.py`의 끝에 다음과 같이 내용 추가:

  ```python
  # mysite/settings.py
  
  STATIC_URL = '/static/'
  # 위의 내용 동일
  
  #-- Logging
  # 장고의 디폴트 설정을 유지하면서 로깅 설정
  LOGGING = {
      'version': 1,
      'disable_existing_loggers': False,
      'formatters':{
          'verbose': {
              'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
              'datefmt': "%d/%b/%Y %H:%M:%S"
          },
      },
      'handlers': {
          'file': {
              'level': 'DEBUG',
              'class': 'logging.FileHandler',
              'filename': os.path.join(BASE_DIR, 'logs', 'mysite.log'),
              'formatter': 'verbose'
          },
      },
      'loggers': {
          'polls': {
              'handlers': ['file'],
              'level': 'DEBUG',
          },
      },
  }
  ```

  > - 위 코드는 장고의 디폴트 설정 그대로 로거를 사용
  > - 이름이 `mysite` 대신 `polls`로 되어 있는 것은 다음 `view.py`에서 `__name__`변수로 로거를 취득하기 위함

- `views.py`도 다음과 같이 내용 추가:

  ```python
  # polls/views.py
  
  from polls.models import Choice, Question
  # 위의 내용 동일
  #-- logging 추가
  import logging
  logger = logging.getLogger(__name__)
  
  # 중간 내용 생략
  
  #-- Function-based View
  def vote(request, question_id):
      logger.debug("vote().question_id: %s" % question_id)    # logger 추가
      question = get_object_or_404(Question, pk=question_id)
  
  # 이하 내용 동일
  ```

  > - `__name__`변수를 사용하여 polls 로거에서 메시지를 기록
  > - `debug()` 메소드를 호출하여 DEBUG 수준으로 로그 레코드를 생성

- `/ch5/` 에 logs 디렉토리 생성 필요하며, 정상적으로 작동시, 아래와 같은 로그 생성:

  ```
  # /logs/mysite.log
  
  [15/Apr/2019 08:24:47] DEBUG [polls.views:30] vote().question_id: 5
  ```

  

# Troubleshoting

> 1. 함수형 뷰를 클래스형 뷰로 전환 후 URLconf 쪽에 문제 발생:
>
>    ```
>    File "C:\Git\Web\Django\ch5\polls\urls.py", line 21, in <module>
>    	path('', views.index, name = 'index'),
>    AttributeError: module 'polls.views' has no attribute 'index'
>    ```
>
>    - `urls.py` 확인 결과 업데이트 내용이 저장되지 않은 상태에서 서버 테스트
>    - 변경된 코드 적용 후 실행 시 문제 없음