import cv2, pyautogui, time
import mediapipe as mp
import numpy as np

mph = mp.solutions.hands
mpd = mp.solutions.drawing_utils

hand = mph.Hands(static_image_mode=False, max_num_hands=1)

screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE=False
time_clicked=0

cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)
while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame,1)
    h, w=frame.shape[:2]
    cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(cframe)
    kq = results.multi_hand_landmarks
    if kq:
        for hand_landmarks in kq:
            mpd.draw_landmarks(frame, hand_landmarks, mph.HAND_CONNECTIONS)
            lm4 = hand_landmarks.landmark[4]
            lm8 = hand_landmarks.landmark[8]
            lm4x, lm4y = int(lm4.x*w), int(lm4.y*h)
            lm8x, lm8y = int(lm8.x*w), int(lm8.y*h)

            cv2.circle(frame, (lm4x,lm4y),5,(255,0,255),-1)
            cv2.circle(frame, (lm8x,lm8y),5,(255,0,255),-1)
            cv2.line(frame, (lm8x, lm8y), (lm4x, lm4y), (0,255,0), 2)
            
            dist = ((lm8x-lm4x)**2 + (lm8y-lm4y)**2)**0.5
            if dist <30:
                if time.time()-time_clicked > 0.5:
                    pyautogui.click()
                    cv2.putText(frame, "CLICK!",(w//2,h//2),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    time_clicked = time.time()
            else:
                screen_8x= int(np.interp(lm8x, [0,w],[0,screen_w]))
                screen_8y= int(np.interp(lm8y, [0,h],[0,screen_h]))
                pyautogui.moveTo(screen_8x, screen_8y, duration=0.05)

    cv2.putText(frame,f"fps: {fps}",(w-150,h-50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
    cv2.imshow("Webcam",frame)
    if cv2.waitKey(1)==ord("q"):break

cap.release()
cv2.destroyAllWindows()
