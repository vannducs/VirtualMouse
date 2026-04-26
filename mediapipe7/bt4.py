#Đọc ảnh bằng OpenCV
#Dùng MediaPipe detect landmark bàn tay
#Vẽ các điểm landmark lên ảnh, 
#vẽ hình tròn và in ra tọa độ của ngón trỏ và ngón cái
#Hiển thị kết quả lên màn hình
import cv2
import mediapipe as mp

mph = mp.solutions.hands
mpd = mp.solutions.drawing_utils

hand = mph.Hands(static_image_mode=True, max_num_hands=1)

img = cv2.imread(r"C:\Users\DELL\Downloads\tay.jpg")
h,w = img.shape[:2]
cimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
results = hand.process(cimg)
kq = results.multi_hand_landmarks
if kq:
    for hand_landmarks in kq:
        mpd.draw_landmarks(img, hand_landmarks, mph.HAND_CONNECTIONS)
        lm4 = hand_landmarks.landmark[4]
        lm8 = hand_landmarks.landmark[8]
        lm4x, lm4y=int(lm4.x*w), int(lm4.y*h)
        lm8x, lm8y=int(lm8.x*w), int(lm8.y*h)
        ketqua = cv2.circle(img, (lm4x,lm4y), 10, (0,255,0),-1)
        ketqua = cv2.circle(ketqua, (lm8x, lm8y),10,(0,255,0),-1)
        print(f"Toa do ngon cai la ({lm4x},{lm4y})")
        print(f"Toa do ngon tro la ({lm8x},{lm8y})")
        
cv2.imshow("Ketqua",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
            