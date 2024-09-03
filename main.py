import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6)
mp_draw = mp.solutions.drawing_utils

ball_x = 16
ball_y = 16
ball_vel = np.array([5, 5], dtype=np.float64)
ball_radius = 15
ball_min_speed = 2.0 
score = 0

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    landmarks = hands.process(frame)
    
    frame_height, frame_width, _ = frame.shape

    if landmarks.multi_hand_landmarks:
        finger_positions = []
        for hand_landmarks in landmarks.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x, y = int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)

            finger_positions.append((x, y))

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        if len(finger_positions) == 2:
            cv2.line(frame, finger_positions[0], finger_positions[1], (0, 255, 0), 5)

    ball_x += ball_vel[0]
    ball_y += ball_vel[1]

    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= frame_width: 
        ball_vel[0] *= -1
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= frame_height:
        ball_vel[1] *= -1

    cv2.circle(frame, (int(ball_x), int(ball_y)), ball_radius, (0, 0, 255), -1)
    
    cv2.imshow('vid', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
