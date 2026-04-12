import win32gui
import win32con
from src.config import *
import src.adb_wrapper as adb


def get_window_rect(title_substr):
    def enum_handler(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title_substr in title:
                rect = win32gui.GetWindowRect(hwnd)
                results.append((hwnd, rect))

    results = []
    win32gui.EnumWindows(enum_handler, results)

    if not results:
        raise Exception("Window not found")

    hwnd, rect = results[0]
    x1, y1, x2, y2 = rect
    return hwnd, {"left": x1, "top": y1, "width": x2 - x1, "height": y2 - y1}


def lock_window_size(hwnd, width, height):
    rect = win32gui.GetWindowRect(hwnd)
    x, y = rect[0], rect[1]
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOP,
        x, y,
        width, height,
        win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
    )
    print(f"[INFO] Window locked to {width}x{height}")

def init_window():
    hwnd, rect = get_window_rect(WINDOW_NAME)
    lock_window_size(hwnd, LOCKED_WIDTH, LOCKED_HEIGHT)
    adb.connect()

    print("[INFO] Bot started")
    return hwnd, rect