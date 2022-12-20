# ✅ capstone-design-img2code

# 개요

딥러닝을 이용하여 스크린 샷 이미지를 html코드로 변환하는 프로젝트

# 개발내용

## 1. 데이터 생성기

dsl 자동 생성기 제작 및 html생성, 자동 캡쳐 프로그램 제작을 통해 데이터 셋 자동 생성

### 데이터 복잡성 증가를 위해 추가한 규칙
#### 크기
- 태그 내 텍스트를 고정된 문구에서 랜덤길이의 문자열로 변경
#### 위치
- 행 내부의 컨테이너 수를 기존의 1, 2, 4개에서 3개(triple)을 추가
- 기존 데이터의 버튼, 소제목, 내용 간 고정된 배치 순서를 제거
#### 색상
- 기존에 사용되던 색상에 보라색과 노랑색을 추가


## 2. 기존 모델 확장 내용

- lstm을 gru로 변경
- cnn에 context정보 추가

![Screenshot 2022-12-21 053330](https://user-images.githubusercontent.com/48210134/208761119-9b608cc9-90b7-466b-be88-81cf246c094a.jpg)

빨간 선 부분 추가


## 3. 클라이언트 프로그램


![Screenshot 2022-12-21 053148](https://user-images.githubusercontent.com/48210134/208760864-e7e8d14c-741c-47f2-a155-d420608328b1.jpg)

웹페이지에 접속하여 이미지 업로드 시 분석가능

# Setup

## 1. conda & cuda install

최신 버전의 conda와 cuda 11.2버전 설치

### 2. 파이썬 패키지 설치

~~~
$ pip install -r requirements.txt
~~~

### 3. flask 서버 실행

다운 받은 모델 경로와 모델 이름 설정

~~~
$ python app.py --modelPath=** --modelName=**
~~~

### 4. 클라이언트 프로그램 접속

실행한 PC의 80번 포트로 접속 후 이미지 업로드


# 프로젝트 결과

- 기존 pix2code모델 보다 정확도가 증가

![Screenshot 2022-12-21 053501](https://user-images.githubusercontent.com/48210134/208761328-51bda2f1-e79a-464e-95f3-52038f807c57.jpg)

- 학습시간 단축

![image](https://user-images.githubusercontent.com/48210134/208761395-aff11a84-cc7c-4d45-bce1-5a0dbd7e12fa.png)

- 표본 복잡도 감소

![image](https://user-images.githubusercontent.com/48210134/208761501-bbe72746-02ec-4ea6-bf30-2faab94f53ea.png)


# TEAM `CAPSLOCK`

- 하이현([@hyh1016](https://github.com/hyh1016))
- 김병현 ([@sidereumare](https://github.com/sidereumare))
- 이서영 ([@weadione](https://github.com/weadione))
