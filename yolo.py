import numpy as np
import cv2
import imagezmq

from datetime import datetime


class Yolo:
    def __init__(self, args):
        # 객체를 탐지할 확률
        self.args = args

        # YOLO 모델이 학습된 coco 클래스 레이블
        with open(self.args.label, "r") as f:
            self.LABELS = [line.strip() for line in f.readlines()]

        # 객체를 표시할 bounding box와 text의 랜덤 색상
        self.COLORS = np.random.uniform(0, 255, size=(len(self.LABELS), 3))

        # COCO 데이터 세트(80 개 클래스)에서 훈련된 YOLO 객체 감지기 load
        self.net = cv2.dnn.readNet(self.args.weights, self.args.configure)

        # YOLO에서 필요한 output 레이어 이름
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    # Video stream frame을 생성하고 웹으로 전송함.
    def gen_frames(self):
        # 프레임 크기
        (H, W) = (None, None)

        if self.args.input == "pi":
            image_hub = imagezmq.ImageHub()
        elif self.args.input == "0":
            vs = cv2.VideoCapture(0)
        else:
            vs = cv2.VideoCapture(self.args.input)

        is_detected = False

        # 촬영된 이미지를 웹으로 송출
        while True:
            detected = False

            # 이미지 가져오기
            if self.args.input == "pi":
                _, frame = image_hub.recv_image()
            else:
                _, frame = vs.read()

            height, width, _ = frame.shape

            # 프레임 크기
            if W is None or H is None:
                (H, W) = frame.shape[:2]

            # blob 이미지 생성
            blob = cv2.dnn.blobFromImage(
                frame,
                scalefactor=0.00392,
                size=(320, 320),
                mean=(0, 0, 0),
                swapRB=True,
                crop=False,
            )

            # 객체 인식
            self.net.setInput(blob)
            layer_outputs = self.net.forward(self.ln)

            # bounding box, 확률 및 클래스 ID 목록 초기화
            class_ids = []
            confidences = []
            boxes = []

            # counting 수 초기
            object_count = 0

            # layer_outputs 반복
            for output in layer_outputs:
                # 각 클래스 레이블마다 인식된 객체 수 만큼 반복
                for detection in output:
                    # 인식된 객체의 클래스 ID 및 확률 추출
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    # 객체 확률이 최소 확률보다 큰 경우
                    if confidence > self.args.confidence:
                        detected = True

                        # bounding box 위치 계산
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype(
                            "int"
                        )  # (중심 좌표 X, 중심 좌표 Y, 너비(가로), 높이(세로))

                        # bounding box 왼쪽 위 좌표
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        # bounding box, 확률 및 클래스 ID 목록 추가
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # 탐지 -> 비탐지, 비탐지 -> 탐지로 변할 때 콘솔에 출력
            if is_detected != detected:
                print(f"now :{datetime.now():}, detected: {detected}")
                is_detected = detected

            # bounding box가 겹치는 것을 방지(임계값 적용)
            indexes = cv2.dnn.NMSBoxes(
                boxes, confidences, self.args.confidence, self.args.threshold
            )

            # 화면에 출력
            for i in range(len(boxes)):
                if i in indexes:
                    # counting 수 증가
                    object_count += 1

                    # bounding box 좌표 추출
                    x, y, w, h = boxes[i]

                    # 클래스 ID 및 확률
                    label_confidence = int(confidences[i] * 100)
                    text = f"{self.LABELS[class_ids[i]]} {label_confidence}%"

                    # 색상
                    color = self.COLORS[class_ids[i]]

                    # bounding box 출력
                    cv2.rectangle(
                        frame,
                        pt1=(x, y),
                        pt2=(x + w, y + h),
                        thickness=2,
                        color=color,
                        lineType=cv2.LINE_AA,
                    )

                    # text 출력
                    cv2.putText(
                        frame,
                        text=text,
                        org=(x, y - 10),
                        fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=3,
                        color=color,
                        thickness=2,
                        lineType=cv2.LINE_AA,
                    )

            # counting 결과 출력
            counting_text = f"People Counting : {object_count}"
            cv2.putText(
                frame,
                text=counting_text,
                org=(10, frame.shape[0] - 25),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.85,
                color=(255, 255, 255),
                thickness=2,
                lineType=cv2.LINE_AA,
            )

            _, buffer = cv2.imencode(".jpg", frame)

            frame = buffer.tobytes()

            # pi에서 영상을 받을 경우, pi에게 OK sign을 준다.
            if self.args.input == "pi":
                image_hub.send_reply(b"OK")

            # concat frame one by one and show result
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
