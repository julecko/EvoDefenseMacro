import win32gui
import win32ui
import ctypes
import numpy as np
import cv2

def capture_window(hwnd):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
    save_dc.SelectObject(bitmap)

    user32 = ctypes.windll.user32
    result = user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 1)
    if result != 1:
        print("[WARN] PrintWindow failed")

    bmpstr = bitmap.GetBitmapBits(True)
    img = np.frombuffer(bmpstr, dtype=np.uint8)
    img.shape = (h, w, 4)

    win32gui.DeleteObject(bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def find_object(frame, template_path, threshold=0.8):
    template = cv2.imread(template_path)
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        return max_loc, template.shape
    return None

def match_image(frame, template_path, region="whole", threshold=0.8, draw=False):
    if region == "bottom":
        roi = frame[frame.shape[0] // 2:, :]
        y_offset = frame.shape[0] // 2
    elif region == "top":
        roi = frame[:frame.shape[0] // 2, :]
        y_offset = 0
    else:
        roi = frame
        y_offset = 0

    template = cv2.imread(template_path)
    res = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val < threshold:
        return None

    x, y = max_loc
    h, w = template.shape[:2]

    cx = x + w // 2
    cy = y + h // 2 + y_offset

    return cx, cy