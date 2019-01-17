다음 이미지 사용 Ubuntu 18.04 LTS



참조1: https://www.youtube.com/watch?v=sT9JUL7q2uM

참조2: https://www.smarthomebeginner.com/setup-vnc-server-on-ubuntu-linux/



설치 순서

GCP 세팅

1. VM 생성
2. 외부 고정 IP 설정
3. VNC-Server firewall 설정

Desktop 설치

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

6. vnc 실행

   ```shell
   ## vnc 서버 실행
   vncserver -geometry 1024x640
   
   ## vnc 서버 종료
   vncserver -kill :1
   ```

   



touch ~/.Xresources

