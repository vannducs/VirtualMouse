import cv2
import mediapipe as mp

mph = mp.solutions.hands
mpd = mp.solutions.drawing_utils

anh = cv2.imread(r"C:\Users\DELL\Downloads\tay.jpg")
img = cv2.cvtColor(anh, cv2.COLOR_BGR2RGB)

hand = mph.Hands(static_image_mode=True, max_num_hands=1)
result = hand.process(img)
kq = result.multi_hand_landmarks
if kq:
    for hand_landmarks in kq:
        mpd.draw_landmarks(anh,hand_landmarks,mph.HAND_CONNECTIONS)
    print("Thanh cong")
else:
    print("That bai")

cv2.imshow("Ketqua",anh)
cv2.waitKey(0)
cv2.destroyAllWindows()