# Admin 사이트 꾸미기

- 장고의 Admin 기능은 1) 데이터 관리 및 2) UI 를 관리
- 프로세스의 상태 조회, 기동 및 정지 등 프로세스 관리 기능은 제공하지 않음

## 데이터의 C.R.U.D. 기능

### 1. 데이터 입력 및 수정

- Admin 사이트에 접속하게 되면, 장고에서 기본적으로 제공해주는 Users, Groups 정보와, 하단에 `polls` 어플리케이션에서 사용하는 `Questions`, `Choices` DB 정보를 확인할 수 있음

- 여기서 [DB이름(Questions)], [Add], 혹은 [Change] 버튼을 클릭하면 데이터를 입력 및 수정할 수 있음

- 질문을 클릭하면 레코드의 상세 페이지가 나타나면, 이는 사전에 `models.py`에서 정의한 테이블 모델을 기초로 장고가 자동으로 UI를 생성해 주게 됨

  ![](figs/02_question01.png)

- Question 테이블은 다음과 같이 설정되어 있음

  ```python
  ### polls/models.py
  
  class Question(models.Model):
      question_text = models.CharField(max_length=200)
      pub_date = models.DateTimeField("date published")
  
      def __str__(self):
          return self.question_text
  ```

- Admin 사이트에서는 테이블 각 필드의 값을 수정하는 것이 가능

- 우측 상단의 HISTORY 탭에서는 객체의 변경사항에 대한 이력을 확인 가능

### 2. 필드 순서 변경하기

- 테이블을 보여주는 UI 양식을 변경하려면, `polls/admin.py` 파일을 변경하면 됨

  ```python
  class QuestionAdmin(admin.ModelAdmin):
  	fields = ['pub_date', 'question_text'] # 필드 순서 변경
  
  admin.site.register(Question, QuestionAdmin)
  admin.site.register(Choice)
  ```

- `admin.ModelAdmin` 클래스를 상속받아 새로운 클래스를 정의하고, 이를 `admin.site.register()` 함수의 두번째 인자로 등록 시 필드 순서를 변경 가능

### 3. 각 필드 분리하기 (접기)

- `polls/admin.py` 파일을 수정하면 각 필드를 분리하거나 접는 기능을 구현할 수 있음

  ```python
  class QuestionAdmin(admin.ModelAdmin):
      fieldsets = [
          ('Question statement', {'fields': ['question_text']}),
          ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']})
      ]
  ```

![](figs/02_question02.png)

### 4. 외래키 관계 화면

- Admin에서 [Choices]의 레코드 입력화면으로 이동하면, Question 테이블의 질문을 선택하는 항목이 같이 보임 (Question과 Choice 모델 클래스는 1:N 관계)

- 즉, 외래키 정의가 Admin UI에서 선택박스 위젯으로 보여지는 형식

  ![](figs/02_choice01.png)

- Choice 테이블의 각 레코드는 독립적으로 생성이 불가능하며, Question 테이블의 특정 레코드에 외래키로 연결 되어야 함

### 6. Question 및 Choice를 한 화면에서 변경하기

- 위와 같은 방식에서 여러개의 Choice 레코드를 추가하는 것은 동일 작업을 반복해야됨에 따라 번거로운 작업이 될 수 있음

- 아래 예제처럼 `polls/admin.py`를 수정하면 Question 레코드를 기준으로 여러개의 Choice 를 함께 보면서 편집이 가능해짐 (*Question 레코드 기준으로 Choice 레코드가 연결되는 것이므로 QeustionAdmin 클래스를 수정*)

  ```python
  ### polls/admin.py
  
  class ChoiceInline(admin.StackedInline):
      model = Choice
      extra = 2
      
  class QuestionAdmin(admin.ModelAdmin):
      fieldsets = [
          (none, {'fields': ['question_text']}),
          ('Date Information', {'fields':['pub_date'], 'classes':['collapse']}),
      ]
      inlines = [ChoiceInline]
      
   admin.site.register(Question, QuestionAdmin)
  ```

  ![](figs/02_question03.png)

### 6. 테이블 형식으로 보여주기

- 위와 같은 화면은 기존 방식에 비해 반복작업이 용이하기는 하지만, 항목이 많아질 경우 한화면에서 확인하기 불편할 수 있음

- 이를 아래와 같이 보기 편하도록 테이블 형식으로 표현 가능:

  ```python
  ### polls/admin.py
  
  
  class ChoiceInline(admin.TabularInline):
      ...
  ```

  ![](figs/02_multiple_choice01.png)

### 7. 레코드 리스트 컬럼 지정하기

- Admin 사이트의 첫 페이지에서 테이블명을 클릭하면, 테이블 리스트를 반환

- 여기서 테이블 리스트의 column 값은 `models.py`에서 정의한 `__str__()` 메소드의 리턴값을 레코드의 제목으로 사용

  ![](figs/02_question_list01.png)

- 마찬가지로 `polls/admin.py`를 수정하여 컬럼 항목을 지정 가능

  ```python
  ### polls/admin.py
  
  inlines = [ChoiceInline]	# Choice 모델 클래스 같이 보기
  list_display = ('question_text', 'pub_date')	# 레코드 리스트 컬럼 지정
  ```

  ![](figs/02_question_list02.png)

### 8. list_filter 필터

- `polls/admin.py`에 `list_filter` 속성을 추가하면, UI 화면 우측에 필터 사이드바를 붙일 수도 있음

  ```python
  ### polls/admin.py
  
  inlines = [ChoiceInline]
  list_display = ('question_text', 'pub_date')
  list_filter = ['pub_date']
  ```

  ![](figs/02_filter_list.png)

- [FILTER]에는 필터에 사용된 기준 필드 타입에 따라, 장고가 적절한 항목들을 반환
- 위 예제에서는 `pub_date`가 기준 필드로, 'Today', 'Past 7 days' 같은 옵션을 제공

### 9. search_fields

- 필요에 따라 검색박스를 표시하는 기능도 제공

  ```python
  ### polls/admin.py
  
  inlines = [ChoiceInline]
  list_display = ('question_text', 'pub_date')
  list_filter = ['pub_date']
  search_fields = ['question_text']
  ```

  ![](figs/02_search_field.png)

- 검색박스에 단어를 입력하면, 장고는 LIKE 쿼리로 question_text(지정한) 필드를 검색
- 여러개의 필드를 지정 시 모든 필드에서 입력된 단어를 검색

### 10. polls/admin.py 변경 내역 정리

- 최종적으로 변경된 `polls/admin.py`는 아래와 같음

  ```python
  ### polls/admin.py
  
  from django.contrib import admin
  from polls.models import Question, Choice
  
  #class ChoiceInline(admin.StackedInline):									# 1
  class ChoiceInline(admin.TabularInline):									# 2
      model = Choice
      extra = 2
      
  class QuestionAdmin(admin.ModelAdmin):
      #fields = ['pub_date', 'question_text']									# 3
      fieldsets = [														  # 4
          (None, {'fields': ['question_text']}),
          #('Date Information', {'fields':['pub_date']}),
          ('Date Information', {'fields':['pub_date'], 'classes':['collapse']}), # 5
      ]
      inlines = [ChoiceInline]
      list_display = ('question_text', 'pub_date')							# 6
      list_filter = ['pub_date']											   # 7
      search_fields = ['question_text']									   # 8
  
  admin.site.register(Question, QuestionAdmin)
  admin.site.register(Choice)
  ```

  > 1. Choice 레이블 Question 테이블에 연동하여(FK) 한화면에서 변경하기
  > 2. 테이블 형식으로 전환
  > 3. 필드 순서 변경
  > 4. 각 필드 분리하여 보여주기 (각 칼럼 분리)
  > 5. 필드 접기 기능
  > 6. 레코드 컬럼 지정
  > 7. 필터 기능
  > 8. 검색박스 기능

### 11. Admin 사이트 템플릿 수정

- Admin 사이트의 템플릿도 개발자 취향에 맞게 수정 가능

- 이 경우 장고의 기본 Admin 템플릿을 프로젝트로 복사한 후 변경

  ```
  Django> mkdir ch4
  Django> mkdir ch4\templates
  Django> mkdir ch4\templates\admin
  Django> copy C:\Programming\Anaconda3\Lib\site-packages\django\contrib\admin\templates\admin\base_site.html ch4\templates\admin
  Django> notepad mysite\settings.py
  
  ```

  

