import cv2
import numpy as np

# Define the color ranges
color_ranges = [
    ([0, 150, 150], [3, 255, 255]),  # Red
    ([50, 80, 80], [70, 255, 255]),  # Green
    ([110, 80, 80], [120, 255, 255])  # Blue
]

# Print the predefined color ranges
print("Predefined Color Ranges:")
for i, (lower, upper) in enumerate(color_ranges, 1):
    color_name = ""
    if i == 1:
        color_name = "Red"
    elif i == 2:
        color_name = "Green"
    elif i == 3:
        color_name = "Blue"

    print(f"Color {i}: {color_name} - Lower = {lower}, Upper = {upper}")

# Open the camera
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_EXPOSURE, -1)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

cv2.namedWindow("Camera")
cv2.namedWindow("Debug")

detected_colors = []  # List to store detected colors

while capture.isOpened():
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (11, 11), 0)

    mask = np.zeros_like(hsv[:, :, 0])

    for lower, upper in color_ranges:
        color_mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        mask = cv2.bitwise_or(mask, color_mask)

    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result_frame = frame.copy()  # Create a copy of the frame to draw colored circles

    for contour in contours:
        # Filter out non-circular contours
        if cv2.contourArea(contour) < 100:
            continue

        (x, y), radius = cv2.minEnclosingCircle(contour)
        M = cv2.moments(contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Draw circles only if they are reasonably circular
        if radius > 10:
            color = frame[int(y), int(x)]  # Get color from the original frame
            color = tuple(int(c) for c in color)

            cv2.circle(result_frame, (int(x), int(y)), int(radius), color, 2)
            cv2.circle(result_frame, center, 5, color, -1)

            # Update the list with the detected color
            detected_colors.append(color)

            # Check for a winning sequence (three colors in a row)
            if len(detected_colors) >= 3:
                last_three_colors = detected_colors[-3:]
                if all(color == last_three_colors[0] for color in last_three_colors):
                    print("WIN")

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    cv2.imshow("Debug", mask)
    cv2.imshow("Camera", result_frame)

capture.release()
cv2.destroyAllWindows()
