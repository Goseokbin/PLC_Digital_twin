# PLC를 이용한 Digital-Twin System 설계 및 구현
__2019 충북대학교 캡스톤 디자인 프로젝트__<br>
PLC의 물리적인 동작환경을 시뮬레이션하고, PLC기기에서 발생하는 명령어 데이터와 PLC기기에 부착되어있는 센서 데이터를 이용하여 실시간으로 공정과정을 모니터링 할 수 있는 가상의 __Digital-Twin System__ 구현

## 사용 언어/프레임 워크
- 언어
  - Python
    - PySerial
      - PLC와 Web간의 Serial 통신부
    - Plotly
      - Arduino 데이터 그래프 시각화
  - C#
    - PLC 3D 모델 동작 구현
  - Javascript
    - AJAX
      - Web과 Arduino 통신부
      - Server에서 얻어온 PLC 명령어 데이터와 실제 하드웨어 전송간 비동기 처리 구현
  - MySQL

- 프레임워크
  - Unity3D
    - PLC 3D modeling
  - Django
    - Web Page 구축
  
- 하드웨어
  - LS산전 PLC
  - Arduino 센서( 온도, 습도 )
  
## 구현 화면
<div>
<img margin-right="60" width="350" height="300" src="https://user-images.githubusercontent.com/37431938/72971741-9136b500-3e0d-11ea-81da-bcbfaa58b4d6.png">
<img width="350" height="300" src="https://user-images.githubusercontent.com/37431938/72971739-909e1e80-3e0d-11ea-8efa-c14b0f80e079.png">
</div>

## Credits
충북대학교 소프트웨어학과 고석빈
충북대학교 소프트웨어학과 김재훈
