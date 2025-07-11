import cv2
from datetime import datetime

cap = cv2.VideoCapture('videos/sample.mp4')  # Change file name if needed

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    motion = False

    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        motion = True
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Motion Detected", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if motion:
        with open("motion_log.txt", "a") as log:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log.write(f"Motion detected at {now}\n")

    cv2.imshow("LionGuard Surveillance", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()
    if not ret:
        break

    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()