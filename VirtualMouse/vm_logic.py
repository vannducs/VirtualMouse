import cv2, pyautogui, time
import mediapipe as mp
import numpy as np

mph  = mp.solutions.hands
mpd  = mp.solutions.drawing_utils
hand = mph.Hands(static_image_mode=False, max_num_hands=1)

screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE  = False
time_clicked        = 0

def gap(hand_landmarks, tip, pip):
    return hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y

def process(frame):
    global time_clicked

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
            lm20 = hand_landmarks.landmark[20]

            lm4x,  lm4y  = int(lm4.x*w),  int(lm4.y*h)
            lm8x,  lm8y  = int(lm8.x*w),  int(lm8.y*h)
            lm20x, lm20y = int(lm20.x*w), int(lm20.y*h)

            cv2.circle(frame, (lm4x,  lm4y),  10, (255,0,255), -1)
            cv2.circle(frame, (lm8x,  lm8y),  10, (255,0,255), -1)
            cv2.circle(frame, (lm20x, lm20y), 10, (255,0,255), -1)
            cv2.line(frame, (lm8x,lm8y), (lm4x,lm4y), (0,255,0), 2)

            tro_gap      = gap(hand_landmarks, 8,  6)
            giua_gap     = gap(hand_landmarks, 12, 10)
            aput_gap     = gap(hand_landmarks, 16, 14)
            ut_gap       = gap(hand_landmarks, 20, 18)
            bon_ngon_gap = tro_gap and giua_gap and aput_gap and ut_gap

            like    = lm4.y < hand_landmarks.landmark[2].y
            dislike = lm4.y > hand_landmarks.landmark[2].y

            dist_cai_tro = ((lm8x-lm4x)**2  + (lm8y-lm4y)**2)**0.5
            dist_tro_ut  = ((lm20x-lm8x)**2 + (lm20y-lm8y)**2)**0.5

            if dist_cai_tro < 30:
                if time.time()-time_clicked > 0.5:
                    pyautogui.leftClick()
                    time_clicked = time.time()
                mode = "LEFT CLICK"

            elif dist_tro_ut < 30:
                if time.time()-time_clicked > 0.5:
                    pyautogui.rightClick()
                    time_clicked = time.time()
                mode = "RIGHT CLICK"

            elif bon_ngon_gap and like:
                pyautogui.scroll(5)
                mode = "SCROLL UP"

            elif bon_ngon_gap and dislike:
                pyautogui.scroll(-5)
                mode = "SCROLL DOWN"

            else:
                if not tro_gap:
                    sx = int(np.interp(lm8x, [0,w], [0,screen_w]))
                    sy = int(np.interp(lm8y, [0,h], [0,screen_h]))
                    pyautogui.moveTo(sx, sy, duration=0.05)
                mode = "DI CHUYEN"

            data = {
                "found": True,
                "mode":  mode,
                "lm4x":  lm4x, "lm4y": lm4y,
                "lm8x":  lm8x, "lm8y": lm8y,
                "dist":  int(dist_cai_tro)
            }
    return frame, data