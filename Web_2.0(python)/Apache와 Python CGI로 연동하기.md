# Apache와 Python CGI로 연동하기

### Nano Editor 설치

- Apache2의 config 파일 수정을 위해 Nano Editor 설치 (Vim 대체 가능)

  ```shell
  sudo apt-get update
  sudo apt-get install nano
  ```

### Config 파일 수정

- config 파일이 위치한 폴더는 다음과 같음: `etc/apache2/sites-enabled/`

- 다음 명령어로 config 파일 호출

  ```shell
  sudo nano /etc/apache2/sites-enabled/000-default.conf
  ```

- Config 파일을 아래와 같이 수정

  ```
  <VirtualHost *:80 *:3000>
          ServerAdmin webmaster@localhost
          DocumentRoot /home/cabox/workspace
          
          //이하 내용 추가
          // <Directory> 내 폴더에 한해 옵션 적용
          <Directory /home/cabox/workspace>
          		//  AddHandler로 html/img외 어플리케이션으로 시행되어야 할 파일 임을 지정
          		// .py 파일은 CGI 표준 사용
                  AddHandler cgi-script .py
                  // 위 경로에 있는 파일은 CGI로써 실행 허용
                  Options ExecCGI
          </Directory>
          
          //이상 내용 추가
          
          ErrorLog ${APACHE_LOG_DIR}/error.log
          CustomLog ${APACHE_LOG_DIR}/access.log combined
  </VirtualHost>
  ```

- 아직까지는 `helloworld.py` 실행 시 python 문서가 출력

### Apache2 옵션 설정

- CGI 옵션은 기본적으로 꺼져 있는 상태로 옵션을 킬 필요가 있음

  ```shell
  sudo a2enmod cgi
  sudo service apache2 restart
  ```

- CGI 옵션을 활성화 시킨 후 서버 재시작

- `helloworld.py` 실행 시 Internal Server Error 발생

  > - helloworld.py를 어플리케이션으로 실행
  > - header가 없어서 에러 반환

### 헤더 설정

- 헤더는 다음과 같은 내용으로 py 파일 첫번째 줄에 위치

  ```python
  #!/usr/bin/python3
  
  ## 아래 헤더 추가
  print("content-type:text/html; charset=UTF-8\n")
  
  print("Hello World")
  print()
  print(1+300)
  ```

  

## Troubleshoot

- `sudo a2enmod cgi` 실행 시 다음과 같은 문구가 반환 되는 경우가 있음

  ```shell
  sudo a2enmod cgi
  
  Your MPM seems to be threaded. Selecting cgid instead of cgi.
  Enabling module cgid.
  To activate the new configuration, you need to run:
  service apache2 restart
  ```

- 정상적으로 실행된다면 다행이지만 CGI 옵션이 실행되지 않고 py 스크립트만 반복 반환 되는 경우가 있음

- 아래 코드를 통해 mpm을 죽이고 CGI를 활성화 하여 문제 해결

  ```shell
  sudo a2dismod mpm_event
  sudo a2enmod mpm_prefork
  sudo service apache2 restart
  
  sudo a2enmod cgi
  
  Enabling module cgi.
  To activate the new configuration, you need to run:
  service apache2 restart
  ```

- reference to https://ubuntuforums.org/showthread.php?t=2258746

  > Apache has more than one way to split itself into multiple handlers for connections. Those are called MPM (Multi Processing Mo dule). You are using a thread based MPM. The cgi module can't work with that, so an equivalent module - cgid - gets activated.  