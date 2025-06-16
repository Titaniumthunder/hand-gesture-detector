import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Finger tip landmarks
finger_tips = [8, 12, 16, 20]

# Start webcam
cap = cv2.VideoCapture(0)

# Create named window that is resizable
cv2.namedWindow("Hand Gesture Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Gesture Detection", 720, 720)  # Set initial size

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and convert to RGB
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            lm_list = []
            for i, lm in enumerate(hand.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            # Count raised fingers
            fingers_up = 0
            if lm_list:
                # Thumb (basic right-hand logic)
                if lm_list[4][0] > lm_list[3][0]:
                    fingers_up += 1

                # Other fingers
                for tip in finger_tips:
                    if lm_list[tip][1] < lm_list[tip - 2][1]:
                        fingers_up += 1

            # Display number of fingers
            cv2.putText(frame, f'Fingers: {fingers_up}', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    # Show the frame
    cv2.imshow("Hand Gesture Detection", frame)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
