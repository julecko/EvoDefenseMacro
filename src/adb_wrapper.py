import subprocess
from src.config import *
import time
from typing import Literal

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print("[STDOUT]", result.stdout.strip())
    if result.stderr:
        print("[STDERR]", result.stderr.strip())
    
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {' '.join(cmd)} (code {result.returncode})")
    
    return result


def connect():
    run_cmd([ADB_PATH, "connect", ADB_HOST])
    run_cmd([
        ADB_PATH, "-s", ADB_HOST,
        "shell", "wm", "size", f"{LOCKED_WIDTH}x{LOCKED_HEIGHT}"
    ])
    print("[INFO] ADB connected")


def click(x, y):
    ax = int(x)
    ay = int(y)
    print(f"[ADB] tap {ax}, {ay}  (raw: {x},{y})")

    run_cmd([
        ADB_PATH, "-s", ADB_HOST,
        "shell", "input", "tap", str(ax), str(ay)
    ])

def swipe(x1, y1, x2, y2, duration=300):
    print(f"[ADB] swipe ({x1},{y1}) -> ({x2},{y2}) [{duration}ms]")
    
    run_cmd([
        ADB_PATH, "-s", ADB_HOST,
        "shell", "input", "swipe",
        str(int(x1)), str(int(y1)),
        str(int(x2)), str(int(y2)),
        str(duration)
    ])

    time.sleep(duration/1000)


def scroll(direction: Literal["down", "up"] = "down", length: int = 100, duration: int = 300):
    center_x = LOCKED_WIDTH // 2
    center_y = LOCKED_HEIGHT // 2

    if direction == "up":
        end_y   = int(center_y + length)
    elif direction == "down":
        end_y   = int(center_y - length)
    else:
        raise ValueError("direction must be 'down' or 'up'")

    swipe(center_x, center_y, center_x, end_y, duration)