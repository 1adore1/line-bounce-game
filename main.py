import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6)
mp_draw = mp.solutions.drawing_utils

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

    cv2.imshow('vid', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
