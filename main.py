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
        # save coordinates of index finger tips
        finger_positions = []
        for hand_landmarks in landmarks.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x, y = int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)

            finger_positions.append((x, y))

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        if len(finger_positions) == 2:
            # line between fingers
            cv2.line(frame, finger_positions[0], finger_positions[1], (0, 255, 0), 5)

            x1, y1 = finger_positions[0]
            x2, y2 = finger_positions[1]

            # phisics for ball collision
            line_vec = np.array([x2 - x1, y2 - y1])
            line_length = np.linalg.norm(line_vec)
            ball_to_line = np.array([ball_x - x1, ball_y - y1])
            projection_length = np.dot(ball_to_line, line_vec / line_length)
            close_line_point = np.array([x1, y1]) + projection_length * (line_vec / line_length)
            if 0 <= projection_length <= line_length:
                dist = np.linalg.norm(np.array([ball_x, ball_y]) - close_line_point)
                if dist < ball_radius:
                    score += 1
                    normal = np.array([ball_x, ball_y]) - close_line_point
                    normal /= np.linalg.norm(normal)
                    ball_vel = ball_vel - 2 * np.dot(normal, ball_vel) * normal

                    # margin after collision, so ball doesn't get stuck
                    ball_x += normal[0] * (ball_radius - dist + 1)
                    ball_y += normal[1] * (ball_radius - dist + 1)

    ball_x += ball_vel[0]
    ball_y += ball_vel[1]

    # ball collisions with walls
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= frame_width: 
        ball_vel[0] *= -1
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= frame_height:
        ball_vel[1] *= -1

    # update ball position 
    cv2.circle(frame, (int(ball_x), int(ball_y)), ball_radius, (0, 0, 255), -1)

    # update score tab
    cv2.putText(frame, f'Score: {score}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('vid', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
