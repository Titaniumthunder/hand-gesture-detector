import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Tip landmark indexes (excluding thumb)
finger_tips = [8, 12, 16, 20]

# Start webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow("Two-Hand Gesture Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Two-Hand Gesture Detection", 720, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Flip label because of camera flip
            raw_label = handedness.classification[0].label  # 'Left' or 'Right'
            hand_label = "Right" if raw_label == "Left" else "Left"

            lm_list = []
            h, w, _ = frame.shape
            for lm in hand_landmarks.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            fingers_up = 0
            if lm_list:
                # --- Thumb ---
                thumb_tip = lm_list[4]
                thumb_ip = lm_list[3]
                if hand_label == "Right":
                    if thumb_tip[0] > thumb_ip[0]:
                        fingers_up += 1
                else:  # Left
                    if thumb_tip[0] < thumb_ip[0]:
                        fingers_up += 1

                # --- Other Fingers ---
                for tip in finger_tips:
                    if lm_list[tip][1] < lm_list[tip - 2][1]:
                        fingers_up += 1

                # --- Label above hand ---
                top_y = min([pt[1] for pt in lm_list])
                label_pos = (lm_list[0][0] - 60, top_y - 20)

                cv2.putText(frame, f"{hand_label} hand: {fingers_up} finger(s)",
                            label_pos,
                            cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

            # Draw landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show frame
    cv2.imshow("Two-Hand Gesture Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
