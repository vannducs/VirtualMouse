import cv2, pyautogui, time
import mediapipe as mp
import numpy as np

mph  = mp.solutions.hands
mpd  = mp.solutions.drawing_utils
hand = mph.Hands(static_image_mode=False, max_num_hands=1)

screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE  = False
time_clicked        = 0
time_scrolled       = 0

def process(frame):
    global time_clicked, time_scrolled

    h, w    = frame.shape[:2]
    cframe  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(cframe)
    kq      = results.multi_hand_landmarks

    data = {
        "found": False,
        "mode":  "WAITING",
        "lm4x":  0, "lm4y": 0,
        "lm8x":  0, "lm8y": 0,
        "dist":  0
    }

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
            cv2.line(frame, (lm8x,lm8y),  (lm4x,lm4y),   (0,255,0), 2)
            cv2.line(frame, (lm4x,lm4y),  (lm20x,lm20y), (0,255,0), 2)
            cv2.line(frame, (lm8x,lm8y),  (lm12x,lm12y), (0,255,0), 2)

            dist_cai_tro  = ((lm8x-lm4x)**2  + (lm8y-lm4y)**2)**0.5
            dist_cai_ut   = ((lm20x-lm4x)**2 + (lm20y-lm4y)**2)**0.5
            dist_tro_giua = ((lm12x-lm8x)**2 + (lm12y-lm8y)**2)**0.5

            if dist_cai_tro < 30:
                if time.time()-time_clicked > 0.5:
                    pyautogui.leftClick()
                    time_clicked = time.time()
                mode = "LEFT CLICK"

            elif dist_cai_ut < 30:
                if time.time()-time_clicked > 0.5:
                    pyautogui.rightClick()
                    time_clicked = time.time()
                mode = "RIGHT CLICK"

            elif dist_tro_giua < 20:
                if time.time()-time_scrolled > 0.1:
                    if lm8y < h // 2:
                        pyautogui.scroll(10)
                        mode = "SCROLL UP"
                    else:
                        pyautogui.scroll(-10)
                        mode = "SCROLL DOWN"
                    time_scrolled = time.time()
                else:
                    mode = "SCROLL UP" if lm8y < h//2 else "SCROLL DOWN"

            else:
                sx = int(np.interp(lm8x, [0,w], [0,screen_w]))
                sy = int(np.interp(lm8y, [0,h], [0,screen_h]))
                pyautogui.moveTo(sx, sy, duration=0.05)
                mode = "MOVING"

            data = {
                "found": True,
                "mode":  mode,
                "lm4x":  lm4x, "lm4y": lm4y,
                "lm8x":  lm8x, "lm8y": lm8y,
                "dist":  int(dist_cai_tro)
            }

    return frame, data