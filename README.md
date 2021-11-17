# Animal Detection using Raspberry Pi

https://github.com/jeffbass/imagezmq 사용하여 파이 카메라로 촬영된 영상을 PC 서버로 가져옴.

**`pi-server`**: **라즈베리파이에 다운로드**한다. 파이 카메라로부터 촬영된 영상을 직접 가져와 PC서버로 전송한다.
**`stream-server`**: **PC에 다운로드**한다. 라즈베리파이로부터 받은 영상을 웹에서 스트리밍하여 볼 수 있도록 한다.

# Gettting started

프로그램을 실행시키기 위하여 아래의 코드를 터미널에 입력하여 라이브러리들을 가져온다.

```Shell
pip3 install -r requirements.txt
```

# How to use

실행은 아래와 같이 한다.

## 1. Server

PC 혹은 개인 노트북에서 `먼저` 실행한다.

```Shell
python3 server.py
```

## 2. Raspberry Pi

```Shell
python3 cam.py --ip {server_ip}

e.g. python3 cam.py --ip 192.168.0.19
```

# Reference

> https://github.com/jeffbass/imagezmq  
> https://github.com/kairess/cctv_raspberrypi
