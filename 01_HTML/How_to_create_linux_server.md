# 리눅스에서 서버 설치하기(Apache)

<br>

- apt-get을 통해 손쉽게 Apache 설치 가능
```shell
sudo apt-get update
sudo apt-get install apache2
```

<br>

- 설치 후 확인 하려면 ip 주소를 알아야 하는데, 이는 아래 명령어로 확인 가능

```shell
hostname -I
```

<br>

- 위에서 알려준 ip 주소로 접속 시 아래와 같은 화면이 출력되면 성공적으로 설치

![](https://s3-ap-northeast-2.amazonaws.com/opentutorials-user-file/module/3135/7996.jpeg)

- 여기서 서버의 로컬 위치는 위 그림에서 빨간줄로 그어진 곳을 참조 `/var/www/html/`

<br>

- 앞선 예제에서 작업한 WEB이란 웹페이지를 로컬위치로 복사

```shell
# 디렉토리 이동
cd media/chrx/E664-061A/Web/Web_1.0\(HTML\)/
# 해당 디렉토리의(.) 모든 파일을(-R) 대상 디렉토리(/var/www....)로 복사
sudo cp -R . /var/www/html/web1
```

<br>

- 정상적으로 복사 된다면, \<ip\>/web1/index.html로 접속이 가능

