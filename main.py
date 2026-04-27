import cv2
import time
from src.navigation import Navigator, Page
from src.config import *
import src.adb_wrapper as adb
from src.window import init_window
from src.image_match import match_image, capture_window
from pathlib import Path


def end(exit_code = 0):
    cv2.destroyAllWindows()
    exit(exit_code)

def watch_ad(navigator: Navigator):
    if not navigator.move_in_page("ad_confirm_button", "bottom"):
        print("Ad confirm button not found")
        return False

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
    time.sleep(7)
    return True

def watch_ads_blitz(navigator: Navigator):
    adb.click(83, 579)
    time.sleep(2)
    
    if navigator.move_in_page("claim_button", "bottom"):
        adb.click(250, 638)
        time.sleep(1)
    else:
        print("Claim button not found")

    for _ in range(3):
        if navigator.move_in_page("quick_blitz_button"):
            adb.click(270, 900)
        time.sleep(1)

    for _ in range(7):
        if not navigator.move_in_page("watch_ad_button", "bottom"):
            print("Watch ad button not found")
            time.sleep(1)
        
        if not watch_ad(navigator):
            break
        adb.click(270, 900)
        time.sleep(2)

    if navigator.move_in_page("claim_button", "bottom"):
        adb.click(250, 638)
        time.sleep(1)
    else:
        print("Claim button not found")

    adb.click(270, 930)

    navigator.return_to_main()


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
    
def watch_ads_shop(navigator: Navigator):
    navigator.move_to(Page.SHOP)
    for _ in range(10):
        adb.scroll("up", length=200, duration=150)

    for _ in range(10):
        adb.scroll("down")
        if navigator.move_in_page("free_chest_button"):
            watch_ad(navigator)
            adb.click(270, 900)

    for _ in range(5):
        adb.scroll("down", length=200, duration=150)

    if navigator.move_in_page("free_gold_button"):
        watch_ad(navigator)
        adb.click(270, 900)
    
    navigator.return_to_main()


def watch_ads_guild(navigator: Navigator):
    navigator.move_to(Page.GUILD)

    navigator.move_in_page("daily_donate")

    if not navigator.move_in_page("free_guild_button", "whole"):
        return False

    watch_ad(navigator)

    adb.click(270, 900)
    time.sleep(1)

    navigator.return_to_main()

def watch_ads_fort(navigator: Navigator):
    navigator.move_to(Page.TERRITORY)

    navigator.move_in_page("fort")

    navigator.move_in_page("fort_craft_button")
    navigator.move_in_page("free_fort_button")

    watch_ad(navigator)

    time.sleep(5)
    adb.click(270, 900)
    time.sleep(2)

    navigator.move_in_page("fort_back_button")

    navigator.return_to_main()

def watch_ads_event(navigator: Navigator):
    adb.click(40, 280)
    time.sleep(3)

    navigator.move_in_page("free_stamina_event")
    watch_ad(navigator)
    time.sleep(1)
    adb.click(240, 900)
    time.sleep(1)

    navigator.move_in_page("daily_deals_button")
    time.sleep(2)
    navigator.move_in_page("free_crystal_event")
    watch_ad(navigator)
    time.sleep(1)
    adb.click(240, 900)
    time.sleep(1)

    navigator.move_in_page("event_back_button")


def main():
    hwnd, rect = init_window()
    navigator = Navigator(hwnd)
    navigator.return_to_main()
    watch_ads_fort(navigator)
    watch_ads_shop(navigator)
    watch_ads_event(navigator)
    watch_ads_blitz(navigator)
    watch_ads_guild(navigator)
   
if __name__ == "__main__":
    main()