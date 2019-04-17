# 04-2  리눅스 서버에 Django 배포하기 (NGINX)

- **NGINX**는 Apache 웹서버의 단점으로 지적된 동시 처리 능력을 높이고 메모리를 적게 사용하는 방향으로 설계된 무료 오픈소스 웹 서버
- Apache<sup>httpd</sup>도 전 세계에서 운영중인 웹사이트의 50% 이상이 사용할 정도로 인기있는 웹 서버이나, 새로 구축하는 사이트는 NGINX를 더 많이 사용하는 추세 (단순 + 확장 용이)

___

## 1. 장고 설정 변경하기

- 운영 환경에서 웹서버와 Django를 연동하기 위해서는 아래와 같이 장고의 설정을 몇가지 변경해야 함:

  > 0. 파이썬 3.x 버전을 사용하는 가상환경 구축
  > 1. `settings.py` 파일의 DEBUG 변경
  > 2. `settings.py` 파일의 ALLOWED_HOSTS 변경
  > 3. `settings.py` 파일의 STATIC_ROOT 추가
  > 4. `collectstatic` 명령 실행 (가상환경에서)
  > 5. `vi www_dir/secret_key.txt` 파일 생성 및 `SECRET_KEY` 저장
  > 6. `settings.py` 파일의 `SECRET_KEY` 변경
  > 7. `db.sqlite3` 파일의 위치 및 권한 변경
  > 8. 로그 파일의 권한 변경

  

___

## 2. NGINX 설치

