# GCP 내 리눅스 웹서버 및 GUI 구축

## 설치 순서

>  ### GCP 세팅
>
> 1. VM 생성: Ubuntu 16.04 LTS , 30기가 
> 2. 외부 고정 IP 설정: VPC 네트워크 > 외부 IP 주소
> 3. VNC-Server firewall 설정: 방화벽 규칙 > 소스필터 IP 범위 0.0.0.0/0, tcp:5901 프로토콜

> ### Desktop 설치
>
> 1. 시스템 셋업
> 2. Ubuntu-desktop 설치
> 3. VNCserver 구축
> 4. Apache2 설치

1. 시스템 setup

   ```shell
   sudo apt-get update
   sudo apt-get upgrade
   ```

   

2. desktop 설치

   ```shell
   sudo apt-get install ubuntu-desktop gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal autocutsel -y
   ```

   

3. vnc server 설치

   ```shell
   //sudo apt-get install vnc4server
   sudo apt-get -y install tightvncserver
   touch ~/.Xresources
   ```

   

4. vnc server config

   ```shell
   ## backup 만들어 두기
   cp ~/.vnc/xstartup ~/.vnc/xstartup_backup
   
   ## config 열기
   nano ~/.vnc/xstartup
   ```

   

5. vnc config 안의 내용은 다음과 같음 (https://www.youtube.com/watch?v=sT9JUL7q2uM)

   ```
   #!/bin/sh
   autocutsel -fork
   xrdb $HOME/.Xresources
   xsetroot -solid grey
   export XKL_XMODMAP_DISABLE=1
   export XDG_CURRENT_DESKTOP="GNOME-Flashback:Unity"
   export XDG_MENU_PREFIX="gnome-flashback-"
   unset DBUS_SESSION_BUS_ADDRESS
   gnome-session --session=gnome-flashback-metacity --disable-acceleration-check --debug &
   ```

   ```shell
   
   ```

6.  유저 권한 부여

   ```shell
   su -a -G
   ```

   

7. vnc 실행

   ```shell
   ## vnc 서버 실행
   vncserver -geometry 1024x640
   
   ## vnc 서버 종료
   vncserver -kill :1
   ```




7. Apache 설치

   ```shell
   
   ```

8. Git repo clone 및 Apache default 폴더 수정

   ```she
   
   ```

   

기타 세팅

1. 필수 프로그램 세팅

   ```shell
   ## 파이썬3를 기본으로 세팅
   alias python=python3
   
   ## sublime 설치
   wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
   sudo apt-get install apt-transport-https
   echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
   sudo apt-get update
   sudo apt-get install sublime-text
   
   ## Adapta theme
   
   ```

   





참조1: https://www.youtube.com/watch?v=sT9JUL7q2uM

참조2: https://www.smarthomebeginner.com/setup-vnc-server-on-ubuntu-linux/



