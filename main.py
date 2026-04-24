import cv2
import time
from src.navigation import Navigator, Page
from src.config import *
import src.adb_wrapper as adb
from src.window import init_window
from src.image_match import match_image, capture_window
from pathlib import Path
import re


def end(exit_code = 0):
    cv2.destroyAllWindows()
    exit(exit_code)

def watch_ads_blitz(navigator: Navigator):
    for _ in range(7):
        adb.click(83, 579)
        time.sleep(2)

        if navigator.move_in_page("claim_button", "bottom"):
            time.sleep(1)
            adb.click(250, 638)
            time.sleep(1)
        else:
            print("Claim button not found")

        if navigator.move_in_page("watch_ad_button", "bottom"):
            time.sleep(1)
        else:
            print("Watch ad button not found")
            exit(1)

        if navigator.move_in_page("ad_confirm_button", "bottom"):
            time.sleep(1)
        else:
            print("Ad confirm button not found")
            exit(1)

        while True:
            frame = capture_window(navigator.hwnd)
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

def coop(navigator: Navigator):
    result = navigator.move_to(Page.TERRITORY)
    if not result:
        return False

    time.sleep(1)

    result = navigator.move_in_page("portal_coop")
    if not result:
        return False
    else: 
        return True

def main():
    hwnd, rect = init_window()
    navigator = Navigator(hwnd)

    navigator.return_to_main()
    time.sleep(1)

    navigator.move_to(Page.TERRITORY)
    time.sleep(1)
    navigator.move_to(Page.SHOP)
    time.sleep(1)
    navigator.return_to_main()
    watch_ads_blitz(navigator)
if __name__ == "__main__":
    main()