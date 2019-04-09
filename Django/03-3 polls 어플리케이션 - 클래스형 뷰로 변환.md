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

  