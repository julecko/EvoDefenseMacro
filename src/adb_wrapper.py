import subprocess
from src.config import *

def connect():
    subprocess.run([ADB_PATH, "connect", ADB_HOST], capture_output=True)
    subprocess.run([ADB_PATH, "-s", ADB_HOST, "shell", "wm", "size", f"{LOCKED_WIDTH}x{LOCKED_HEIGHT}"], capture_output=True)
    print("[INFO] ADB connected")

def click(x, y):
    ax = int(x)
    ay = int(y)
    print(f"[ADB] tap {ax}, {ay}  (raw: {x},{y})")
    subprocess.run(
        [ADB_PATH, "-s", ADB_HOST, "shell", "input", "tap", str(ax), str(ay)],
        capture_output=True
    )
