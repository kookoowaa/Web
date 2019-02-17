# 어플리케이션 개발하기

- 모델 작업은 데이터베이스에 테이블을 생성하는 작업으로 다음 순서를 따름:

  ```
  > notepad models.py					// 테이블 정의
  > notepad admins.py					// 정의된 테이블을 Admin 화면에 제공
  > python manage.py makemigrations	// db에 변경이 필요한 사항을 추출
  > python manage.py migrate			// db에 변경 사항을 반영
  > python manage.py runserver		// 개발용 웹서버로 진행사항 확인
  ```

___

## 1. 테이블 정의

