import cv2, pyautogui, time
import mediapipe as mp
import numpy as np

mph = mp.solutions.hands
mpd = mp.solutions.drawing_utils
hand = mph.Hands(static_image_mode=False, max_num_hands=1)

time_clicked = 0
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)
cv2.namedWindow("Webcam")
cv2.setWindowProperty("Webcam", cv2.WND_PROP_TOPMOST, 1)

while True:
    ret, frame = cap.read()
    if not ret: break  
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    cframe  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(cframe)
    kq      = results.multi_hand_landmarks

    if kq:
        for hand_landmarks in kq:
            mpd.draw_landmarks(frame, hand_landmarks, mph.HAND_CONNECTIONS)

            lm4  = hand_landmarks.landmark[4]
            lm8  = hand_landmarks.landmark[8]
            lm12 = hand_landmarks.landmark[12]
            lm20 = hand_landmarks.landmark[20]

            lm4x,  lm4y  = int(lm4.x*w),  int(lm4.y*h)
            lm8x,  lm8y  = int(lm8.x*w),  int(lm8.y*h)
            lm12x, lm12y = int(lm12.x*w), int(lm12.y*h)
            lm20x, lm20y = int(lm20.x*w), int(lm20.y*h)

            cv2.circle(frame, (lm4x,  lm4y),  10, (255,0,255), -1)
            cv2.circle(frame, (lm8x,  lm8y),  10, (255,0,255), -1)
            cv2.circle(frame, (lm12x, lm12y), 10, (255,0,255), -1)
            cv2.circle(frame, (lm20x, lm20y), 10, (255,0,255), -1)

            dist_cai_tro = ((lm8x-lm4x)**2  + (lm8y-lm4y)**2)**0.5
            dist_cai_ut  = ((lm20x-lm4x)**2 + (lm20y-lm4y)**2)**0.5 
            dist_tro_giua = ((lm12x-lm8x)**2 + (lm12y-lm8y)**2)**0.5

            if dist_cai_tro < 30:  
                if time.time()-time_clicked > 0.5:
                    pyautogui.leftClick()
                    time_clicked = time.time()
                cv2.putText(frame, "LEFT CLICK", (10,30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

            elif dist_cai_ut < 30:  
                if time.time()-time_clicked > 0.5:
                    pyautogui.rightClick()
                    time_clicked = time.time()
                cv2.putText(frame, "RIGHT CLICK", (10,30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,165,255), 2)
                
            elif dist_tro_giua < 20:
                if lm8y and lm4y < h//2:
                    pyautogui.scroll(10)
                    cv2.putText(frame, "SCROLL UP", (10,30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                if lm8y and lm4y > h//2:
                    pyautogui.scroll(-10)
                    cv2.putText(frame, "SCROLL DOWN", (10,30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            else:  
                sx = int(np.interp(lm8x, [0,w], [0,screen_w]))
                sy = int(np.interp(lm8y, [0,h], [0,screen_h]))
                pyautogui.moveTo(sx, sy, duration=0.05)
                cv2.putText(frame, "MOVING", (10,30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.putText(frame, f"fps: {fps}", (w-150,h-50),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) == ord("q"): break

cap.release()
cv2.destroyAllWindows()