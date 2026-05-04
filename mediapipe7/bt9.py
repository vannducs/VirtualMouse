#Đọc webcam
#Dùng MediaPipe detect landmark bàn tay
#Vẽ các điểm landmark lên ảnh, vẽ màu tím cho ngón trỏ và ngón cái
#In fps web cam góc dưới phải
#điều khiển chuột máy tính bằng ngón trỏ
#click khi ngón trỏ chạm ngón cái, khi click thì ko di chuyển chuột,
#scroll lên khi like, scroll xuống khi dislike
#click chuột phải khi ngón trỏ chạm ngón út
#Hiển thị video kết quả lên màn hình, cố định cửa sổ bằng cv2.setWindowProperty
import cv2, pyautogui, time
import mediapipe as mp
import numpy as np

mph = mp.solutions.hands
mpd = mp.solutions.drawing_utils

hand = mph.Hands(static_image_mode=False, max_num_hands=1)

time_clicked = 0
screen_w, screen_h= pyautogui.size()
pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)
cv2.namedWindow("Webcam")
cv2.setWindowProperty("Webcam",cv2.WND_PROP_TOPMOST, 1)
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    h, w =frame.shape[:2]
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

            cv2.circle(frame, (lm4x,lm4y), 10, (255,0,255), -1)
            cv2.circle(frame, (lm8x,lm8y), 10, (255,0,255), -1)
            cv2.circle(frame, (lm20x,lm20y), 10, (255,0,255), -1)

            def gap(tip, pip):
                return hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y
            
            tro_gap = gap(8,6)
            giua_gap = gap(12,10)
            aput_gap = gap(16,14)
            ut_gap = gap(20,18)
            bon_ngon_gap = tro_gap and giua_gap and aput_gap and ut_gap
            like = lm4.y < hand_landmarks.landmark[2].y
            dislike = lm4.y > hand_landmarks.landmark[2].y

            dist_cai_tro = ((lm8x-lm4x)**2 + (lm8y-lm4y)**2)**0.5
            dist_cai_ut = ((lm20x-lm4x)**2 + (lm20y-lm4y)**2)**0.5

            if dist_cai_tro <30:
                if time.time()-time_clicked >0.5:
                    pyautogui.leftClick()
                    time_clicked = time.time()
                    cv2.putText(frame, "LEFTCLICK", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
            
            if dist_cai_ut <30:
                if time.time()-time_clicked >0.5:
                    pyautogui.rightClick()
                    time_clicked = time.time()
                    cv2.putText(frame, "RIGHTCLICK", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)

            if bon_ngon_gap  and like:
                pyautogui.scroll(5)
                cv2.putText(frame, "SCROLLUP", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)

            if bon_ngon_gap and dislike:
                pyautogui.scroll(-5)
                cv2.putText(frame, "SCROllDOWN", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)

            else:
                if not tro_gap:
                    screen_8x = int(np.interp(lm8x, [0,w],[0, screen_w]))
                    screen_8y = int(np.interp(lm8y, [0,h],[0, screen_h]))
                    pyautogui.moveTo(screen_8x, screen_8y, duration=0.05)
                    cv2.putText(frame, "MOVING", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
        
    cv2.putText(frame,f"fps: {fps}",(w-150,h-50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
    cv2.imshow("Webcam",frame)
    if cv2.waitKey(1)==ord("q"):break

cap.release()
cv2.destroyAllWindows()