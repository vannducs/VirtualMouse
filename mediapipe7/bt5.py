#Đọc webcam
#Dùng MediaPipe detect landmark bàn tay
#Vẽ các điểm landmark lên ảnh, vẽ màu tím cho ngón trỏ và ngón cái
#In tọa độ hiện thời của ngón trỏ, ngón cái lên góc trái video kết quả
#In fps web cam góc dưới phải
#Hiển thị video kết quả lên màn hình
import cv2
import mediapipe as mp

mph = mp.solutions.hands
mpd = mp.solutions.drawing_utils
hand = mph.Hands(static_image_mode=False, max_num_hands=1)
cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)
while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame,1)
    h, w= frame.shape[:2]
    cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(cframe)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mpd.draw_landmarks(frame,hand_landmarks,mph.HAND_CONNECTIONS)
            lm4 = hand_landmarks.landmark[4]
            lm8 = hand_landmarks.landmark[8]
            lm4x, lm4y = int(lm4.x*w), int(lm4.y*h)
            lm8x, lm8y = int(lm8.x*w), int(lm8.y*h)
            cv2.circle(frame, (lm4x,lm4y),5,(255,0,255),-1)
            cv2.circle(frame, (lm8x, lm8y),5,(255,0,255),-1)
            cv2.putText(frame,f"Cai: ({lm4x},{lm4y})",(100,100),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            cv2.putText(frame,f"Tro: ({lm8x},{lm8y})",(100,130),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

    frame = cv2.putText(frame,f"pfs: {fps}",(w-150,h-50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
    cv2.imshow("Ketqua",frame)
    if cv2.waitKey(1)==ord("q"):break

cap.release()
cv2.destroyAllWindows()

        

