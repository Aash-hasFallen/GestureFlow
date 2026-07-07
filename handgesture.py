import cv2
import mediapipe as mp
import numpy as np
import time
import os
from collections import deque

def get_gesture(hand_landmarks):
    tips = [8, 12, 16, 20]
    mcp = [5, 9, 13, 17]
    fingers = []
    
    for i in range(4):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[mcp[i]].y:
            fingers.append(1)
        else:
            fingers.append(0)
            
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]
    thumb_mcp = hand_landmarks.landmark[2]
    
    thumb_up = thumb_tip.y < thumb_mcp.y and thumb_tip.y < thumb_ip.y
        
    if thumb_up and sum(fingers) == 0:
        return "thumbs_up"
        
    if sum(fingers) == 0:
        return "fist"
        
    if fingers == [1, 0, 0, 0]:
        return "index"
        
    if fingers == [1, 1, 0, 0]:
        return "peace"
        
    if fingers == [1, 1, 1, 0]:
        return "three"
        
    return "unknown"

def is_ok(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    dist = np.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
    
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[9].y
    ring_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[13].y
    pinky_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[17].y
    
    return dist < 0.05 and middle_up and ring_up and pinky_up

def stable_gesture(buffer):
    if not buffer:
        return None
    from collections import Counter
    counts = Counter(buffer)
    most_common, count = counts.most_common(1)[0]
    if count >= len(buffer) * 0.6:
        return most_common
    return None

def main():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    mode = "automation"
    gesture_buffer = deque(maxlen=10)
    
    thumbs_up_start = 0
    ok_start = 0
    last_action_time = 0
    
    draw_color = (255, 0, 0)
    drawing_points = []
    current_line = []

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(rgb_frame)
        
        current_gesture = None
        ok_detected = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                gesture = get_gesture(hand_landmarks)
                gesture_buffer.append(gesture)
                current_gesture = stable_gesture(gesture_buffer)
                
                if is_ok(hand_landmarks):
                    ok_detected = True
                
                index_x = int(hand_landmarks.landmark[8].x * w)
                index_y = int(hand_landmarks.landmark[8].y * h)
                
                if mode == "automation":
                    if time.time() - last_action_time > 3.0:
                        if current_gesture == "index":
                            os.system("open -a Spotify")
                            last_action_time = time.time()
                        elif current_gesture == "peace":
                            os.system("open https://www.youtube.com")
                            last_action_time = time.time()
                        elif current_gesture == "three":
                            os.system("open -a 'Google Chrome'")
                            last_action_time = time.time()
                        elif current_gesture == "fist":
                            os.system("pmset displaysleepnow")
                            last_action_time = time.time()
                
                elif mode == "draw":
                    if current_gesture == "index":
                        draw_color = (255, 0, 0)
                        current_line.append((index_x, index_y))
                    elif current_gesture == "peace":
                        draw_color = (0, 255, 0)
                        current_line.append((index_x, index_y))
                    elif current_gesture == "three":
                        draw_color = (0, 0, 255)
                        current_line.append((index_x, index_y))
                    else:
                        if current_line:
                            drawing_points.append((current_line, draw_color))
                            current_line = []
                            
                    if current_gesture == "fist":
                        drawing_points = []
                        current_line = []

        else:
            if current_line:
                drawing_points.append((current_line, draw_color))
                current_line = []
            gesture_buffer.clear()

        if current_gesture == "thumbs_up":
            if thumbs_up_start == 0:
                thumbs_up_start = time.time()
            elif time.time() - thumbs_up_start > 2.0:
                mode = "draw" if mode == "automation" else "automation"
                thumbs_up_start = 0
                gesture_buffer.clear()
        else:
            thumbs_up_start = 0

        if ok_detected:
            if ok_start == 0:
                ok_start = time.time()
            elif time.time() - ok_start > 3.0:
                break
        else:
            ok_start = 0

        for line, color in drawing_points:
            for i in range(1, len(line)):
                cv2.line(frame, line[i-1], line[i], color, 5)
        if current_line:
            for i in range(1, len(current_line)):
                cv2.line(frame, current_line[i-1], current_line[i], draw_color, 5)

        cv2.putText(frame, f"Mode: {mode.upper()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        y_pos = 60
        instructions = [
            "Thumbs Up Hold 2s: Toggle Mode",
            "OK Sign Hold 3s: Exit",
            "Auto: Index=Spotify, Peace=YT, Three=Chrome, Fist=Lock",
            "Draw: Index=Blue, Peace=Green, Three=Red, Fist=Clear"
        ]
        for inst in instructions:
            cv2.putText(frame, inst, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            y_pos += 25

        cv2.imshow('Hand Gesture System', frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()