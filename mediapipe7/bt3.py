#Đọc webcam
#Dùng MediaPipe detect landmark bàn tay
#Vẽ các điểm landmark lên ảnh
#Hiển thị video kết quả lên màn hình
import cv2
import mediapipe as mp

mph = mp.solutions.hands
mpd = mp.solutions.drawing_utils

hand = mph.Hands(static_image_mode=False, max_num_hands=2)
cap = cv2.VideoCapture(0)
while True:
    ret, frame= cap.read()
    if not ret: break
    frame=cv2.flip(frame,1)
    cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(cframe)
    kq = results.multi_hand_landmarks
    if kq:
        for hand_landmarks in kq:
            mpd.draw_landmarks(frame, hand_landmarks, mph.HAND_CONNECTIONS)
    cv2.imshow("Ketqua",frame)
    if cv2.waitKey(1)==ord("q"):break

cap.release()
cv2.destroyAllWindows()