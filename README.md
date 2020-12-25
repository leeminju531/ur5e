# COBOT (UR5E) PROJECT

### 문제 시나리오 : 
컨베이어 벨트 위의 비타500 상자는 초음파 센서를 이용하여 벨트가 멈춘다. 벨트가 멈춘 상황을 센싱하여 제작한 그리퍼를 부착한
ur5e 로봇팔을 이용해 비타500병을 상자의 위치로 옮겨 컨베이어 벨트를 동작시킴으로써 주어진 자동화 공정을 완성하라

### Click on the image to view the Frame video.
[![Video Label](https://user-images.githubusercontent.com/70446214/103127102-dc1f1380-46d3-11eb-82c4-7050ef76ddd3.png)](https://www.youtube.com/watch?v=LEFCSSzv_UU)


### 문제 해결 전략 
  -lidar를 사용하여 지정된 범위 안의 박스를 인식한다.
  -박스 윗 부분의 카메라를 이용하여 박스 안의 병의 갯수를 인식해 그 값을 기반으로 TargetFrame을 형성한다.
  -UR의 BaseFrame(imaginaryFrame) 과 TargetFrame 간의 위치와 각도를 계산하여 moveit을 기반으로 ur5e 로봇팔이 TargerFrame위로 병을 적재한다.


### Frame 형성 

1. UR의BaseFrame 과 라이다의 LaserFrame간의 관계를 정의한다. 이때, UR BaseFrame 과 LaseFrame은 
각각 제공된 Frame이 이미 부모 자식 관계가 정의되어 있어, 새로운 관계를 정의하기에 문제가 있었는데,
두 Frame 간의 관계는 항상 fix 한 경우이기 때문에, UR 의 BASE를 IMAGINARY 한 가상의 Frame으로 대체하여 
Frame간의 관계를 구축했다.

![image](https://user-images.githubusercontent.com/70446214/102933634-f1cee600-44e5-11eb-9bf6-dcb3d7d2ae70.png)

2. lidar에 의해 극좌표로 들어오는 센싱값을 LaseFrame 위의 좌표정보로 변환하여, 현재,이전,대과거 의 센싱값으로
박스의 끝부분을 추출해 BoxFrame을 형성했다.

![image](https://user-images.githubusercontent.com/70446214/102933703-15922c00-44e6-11eb-9dbe-8603c879cb39.png)


3. Box와 설계된 Glipper의 Hardware Offset을 고려해 BoxFrame과 TargetFrame간의 관계를 형성했다.

![image](https://user-images.githubusercontent.com/70446214/102933744-2d69b000-44e6-11eb-845a-6e1cadb4209f.png)

(data 의 경우, Cam_node에서 병의 갯수를 인식하여 TargetFrame을 형성하기 위한 data를 전송시켜준다.)


4. ImaginaryFrame 에서 바라본 TargetFrame에 대한 정보를 MoveIt에서 subsciribe 하여 지정된 위치로 이동할 수 있도록 
제어한다. (QuaternionFromEuler(Roll,Pitch,Yaw)를 이용)

![image](https://user-images.githubusercontent.com/70446214/102933814-59853100-44e6-11eb-8974-9eda45052785.png)


