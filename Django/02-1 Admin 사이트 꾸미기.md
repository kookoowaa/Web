# Admin 사이트 꾸미기

- 장고의 Admin 기능은 1) 데이터 관리 및 2) UI 를 관리
- 프로세스의 상태 조회, 기동 및 정지 등 프로세스 관리 기능은 제공하지 않음

## 데이터의 C.R.U.D. 기능

### 1. 데이터 입력 및 수정

- Admin 사이트에 접속하게 되면, 장고에서 기본적으로 제공해주는 Users, Groups 정보와, 하단에 `polls` 어플리케이션에서 사용하는 `Questions`, `Choices` DB 정보를 확인할 수 있음
- 여기서 [DB이름(Questions)], [Add], 혹은 [Change] 버튼을 클릭하면 데이터를 입력 및 수정할 수 있음
- 질문을 클릭하면 레코드의 상세 페이지가 나타나면, 이는 사전에 `models.py`에서 정의한 테이블 모델을 기초로 장고가 자동으로 생성해 주게 됨

  ![](figs/Question_table.png)

- Question 테이블은 다음과 같이 설정되어 있음

  ```python
  class Question(models.Model):
      question_text = models.CharField(max_length=200)
      pub_date = models.DateTimeField("date published")
  
      def __str__(self):
          return self.question_text
  ```

  