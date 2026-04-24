import subprocess
from src.config import *

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