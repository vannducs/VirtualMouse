#Đọc webcam
#Dùng MediaPipe detect landmark bàn tay
#Vẽ các điểm landmark lên ảnh, vẽ màu tím cho ngón trỏ và ngón cái
#In tọa độ hiện thời của ngón trỏ, ngón cái lên góc trái video kết quả
#In fps web cam góc dưới phải
#điều khiển chuột máy tính bằng ngón trỏ
#click khi ngón trỏ chạm ngón cái, khi click thì ko di chuyển chuột,
#scroll lên khi like, scroll xuống khi dislike
#click chuột phải khi ngón trỏ chạm ngón út
#Hiển thị video kết quả lên màn hình
import cv2, pyautogui, time
import mediapipe as mp
import numpy as np

mph = mp.solutions.hands
mpd = mp.solutions.drawing_utils

hand = mph.Hands(static_image_mode=False, max_num_hands=1)

time_clicked =0
pyautogui.FAILSAFE=False
screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame,1)
    h,w=frame.shape[:2]
    cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(cframe)
    kq = results.multi_hand_landmarks
    if kq:
        for hand_landmarks in kq:
            mpd.draw_landmarks(frame, hand_landmarks, mph.HAND_CONNECTIONS)
            lm4 = hand_landmarks.landmark[4]
            lm8 = hand_landmarks.landmark[8]
            lm20 = hand_landmarks.landmark[20]

            lm4x, lm4y = int(lm4.x*w), int(lm4.y*h)
            lm8x, lm8y = int(lm8.x*w), int(lm8.y*h)
            lm20x, lm20y = int(lm20.x*w), int(lm20.y*h)
            #xử lý gập ngón
            lm12y = hand_landmarks.landmark[12].y*h
            lm16y = hand_landmarks.landmark[16].y*h
            lm20y = hand_landmarks.landmark[20].y*h
            gap_8_12  = abs(lm8y - lm12y)
            gap_12_16 = abs(lm12y - lm16y)
            gap_16_20 = abs(lm16y - lm20y)
            bon_ngon_gap = gap_8_12 < 30 and gap_12_16 < 30 and gap_16_20 < 30
            # Like → ngón cái cao nhất
            like = lm4y < lm8y and bon_ngon_gap
            # Dislike → ngón cái thấp nhất
            dislike = lm4y > lm8y and bon_ngon_gap

            cv2.circle(frame, (lm4x,lm4y),7, (255,0,255),-1)
            cv2.circle(frame, (lm8x,lm8y),7,(255,0,255),-1)
            cv2.line(frame,(lm4x,lm4y),(lm8x,lm8y),(0,0,255),2)
            cv2.putText(frame,f"Cai: ({lm4x},{lm4y})",(100,100),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            cv2.putText(frame,f"Tro: ({lm8x},{lm8y})",(100,130),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            
            dist_4_8 = ((lm8x-lm4x)**2 + (lm8y-lm4y)**2)**0.5
            dist_4_20 = ((lm20x-lm4x)**2 + (lm20y-lm4y)**2)**0.5
            if dist_4_8<30:
                if time.time()-time_clicked > 0.5:
                    pyautogui.leftClick()
                    cv2.putText(frame, "LEFTCLICK!",(w//2,h//2),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    time_clicked=time.time()
            
            if dist_4_20<30:
                if time.time()-time_clicked >0.5:
                    pyautogui.rightClick()
                    cv2.putText(frame, "RIGHTCLICK!",(w//2,h//2),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    time_clicked=time.time()

            elif like:
                pyautogui.scroll(5)
                cv2.putText(frame, "SCROLL UP", (10,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            elif dislike:
                pyautogui.scroll(-5)
                cv2.putText(frame, "SCROLL DOWN", (10,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2) 
            else:
                screen_8x = int(np.interp(lm8x,[0,w],[0,screen_w]))
                screen_8y = int(np.interp(lm8y,[0,h],[0,screen_h]))
                pyautogui.moveTo(screen_8x, screen_8y, duration=0.05)
            
    cv2.putText(frame,f"fps: {fps}",(w-150,h-50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
    cv2.imshow("Webcam",frame)
    if cv2.waitKey(1)==ord("q"):break

cap.release()
cv2.destroyAllWindows()

