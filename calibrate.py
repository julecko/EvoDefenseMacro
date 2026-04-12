import cv2
import numpy as np
from src.window import init_window
from src.image_match import capture_window

# -------------------------
# STATE
# -------------------------
drawing = False
start_x, start_y = -1, -1
end_x, end_y = -1, -1
frame_display = None

# -------------------------
# MOUSE CALLBACK
# -------------------------
def on_mouse(event, x, y, flags, param):
    global drawing, start_x, start_y, end_x, end_y, frame_display

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y
        end_x, end_y = x, y
        print(f"[CLICK] x={x}, y={y}")

    elif event == cv2.EVENT_MOUSEMOVE:
        end_x, end_y = x, y

        if drawing:
            # Show live coords while dragging
            print(f"[DRAG]  top_left=({start_x},{start_y})  bottom_right=({x},{y})  size=({x - start_x}x{y - start_y})", end="\r")

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_x, end_y = x, y

        w = end_x - start_x
        h = end_y - start_y

        print(f"\n[RECT]  top_left=({start_x},{start_y})  bottom_right=({end_x},{end_y})")
        print(f"[RECT]  x={start_x}, y={start_y}, w={w}, h={h}")
        print(f"[RECT]  center=({start_x + w//2}, {start_y + h//2})")
        print("-" * 60)

# -------------------------
# MAIN
# -------------------------
def main():
    global frame_display

    hwnd, rect = init_window()
    print("[INFO] Calibration tool started")
    print("[INFO] Left click  → print coords")
    print("[INFO] Click+drag  → print rectangle coords")
    print("[INFO] Q           → quit")
    print("-" * 60)

    cv2.namedWindow("calibrate")
    cv2.setMouseCallback("calibrate", on_mouse)

    while True:
        frame = capture_window(hwnd)
        frame_display = frame.copy()

        # Draw crosshair at current mouse pos
        if end_x >= 0 and end_y >= 0:
            cv2.line(frame_display, (end_x, 0), (end_x, frame_display.shape[0]), (0, 255, 255), 1)
            cv2.line(frame_display, (0, end_y), (frame_display.shape[1], end_y), (0, 255, 255), 1)
            cv2.putText(frame_display, f"({end_x}, {end_y})", (end_x + 5, end_y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)

        # Draw live rectangle while dragging
        if drawing and start_x >= 0:
            cv2.rectangle(frame_display, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

            # Show dimensions inside rectangle
            w = end_x - start_x
            h = end_y - start_y
            label = f"({start_x},{start_y}) → ({end_x},{end_y})  {w}x{h}"
            cv2.putText(frame_display, label, (start_x, start_y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

        # Draw finalized rectangle after release
        elif not drawing and start_x >= 0 and (end_x != start_x or end_y != start_y):
            cv2.rectangle(frame_display, (start_x, start_y), (end_x, end_y), (0, 100, 255), 2)
            w = end_x - start_x
            h = end_y - start_y
            label = f"({start_x},{start_y}) → ({end_x},{end_y})  {w}x{h}"
            cv2.putText(frame_display, label, (start_x, start_y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 100, 255), 1)

        cv2.imshow("calibrate", frame_display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()