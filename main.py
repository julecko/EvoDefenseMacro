import cv2
import time
from src.config import *
import src.adb_wrapper as adb
from src.window import init_window
from src.image_match import match_image, capture_window
from pathlib import Path
import re


def pascal_to_snake(name: str) -> str:
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

def load_templates(folder: Path):
    return {
        pascal_to_snake(file.stem): str(file)
        for file in folder.iterdir()
        if file.is_file()
    }

images = load_templates(Path(TEMPLATES_FOLDER_NAME))

def end(exit_code = 0):
    cv2.destroyAllWindows()
    exit(exit_code)

def watch_ads_blitz(hwnd):
    for _ in range(7):
        adb.click(83, 579)
        time.sleep(2)

        frame = capture_window(hwnd)
        match = match_image(frame, images["claim_button"], "bottom")
        if match:
            cx, cy = match
            adb.click(cx, cy)
            time.sleep(1)
            adb.click(250, 638)
            time.sleep(1)
        else:
            print("Claim button not found")

        match = match_image(frame, images["watch_ad_button"], "bottom")
        if match:
            cx, cy = match
            adb.click(cx, cy)
            time.sleep(1)
        else:
            print("Watch ad button not found")
            exit(1)

        frame = capture_window(hwnd)
        match = match_image(frame, images["ad_confirm_button"], "bottom")
        if match:
            cx, cy = match
            adb.click(cx, cy)
            time.sleep(1)
        else:
            print("Ad confirm button not found")
            exit(1)

        while True:
            frame = capture_window(hwnd)
            found = False
            for x in Path(TEMPLATES_FOLDER_NAME + "/X").iterdir():
                if x.is_file():
                    match = match_image(frame, str(x), "top")
                    if match:
                        cx, cy = match
                        adb.click(cx, cy)
                        found = True
                        break
            if found:
                break
            time.sleep(5)
        time.sleep(10)
        adb.click(250, 638)
        time.sleep(2)

def coop(hwnd):
    frame = capture_window(hwnd)
    match = match_image(frame, images["territory_image"], "bottom")
    if match:
        cx, cy = match
        adb.click(cx, cy)
        time.sleep(1)
    else:
        print("Territory not found")
        end(1)

    time.sleep(1)

    frame = capture_window(hwnd)
    match = match_image(frame, images["portal_coop"], "top")
    if match:
        cx, cy = match
        adb.click(cx, cy)
        time.sleep(1)
    else:
        print("Portal coop not found")
        end(1)

def main():
    hwnd, rect = init_window()

    watch_ads_blitz(hwnd)
if __name__ == "__main__":
    main()