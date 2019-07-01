# 기본 환경 셋업

> 본 프로젝트는 Django Girls의 블로그 만들기 튜토리얼을 참조

## 1. 프로젝트 디렉토리 설정

- 프로젝트를 진행 할 디렉토리 선정
- 본 경우는 `Git\Web\Django-Girls`를 사용

## 2. 가상환경 사용하기

- 위의 디렉토리로 이동해서 `djangogirls`라는 가상환경을 설정

  ```shell
  ~Django-Girls> python -m venv djangogirls
  ```

- 위의 커맨드 실행 시 기본적인 패키지로 구성된 가상환경이 설정됨:

  | Package    | Version |
  | ---------- | ------- |
  | pip        | 10.0.1  |
  | setuptools | 39.0.1  |

- 가상환경은 셸에서 다음 커맨드를 실행하여 불러옴: 

  ```shell
  ~Django-Girls> djangogirls\Scripts\activate
  ```

- 2019년 7월 기준으로 `pip`의 최신 버전은 19.1.1이며 업데이트가 필요

  ```shell
  (djangogirls) ~Django-Girls> python -m pip install -U pip
  ```

## 3.  장고 설치하기

- `pip`가 업데이트 된 상황에서는 가상환경에서 다음 커맨드만 실행하면 `Django`가 자동으로 설치됨

  ```shell
  (djangogirls) ~Django-Girls> pip install django~=2.0.0
  ```

  