from enum import Enum
from typing import Optional
from pathlib import Path
import re
import time
from src.config import TEMPLATES_FOLDER_NAME
from src.image_match import match_image, capture_window
import src.adb_wrapper as adb


def pascal_to_snake(name: str) -> str:
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def load_templates(folder: Path):
    return {
        pascal_to_snake(file.stem): str(file)
        for file in folder.iterdir()
        if file.is_file()
    }


class Page(Enum):
    MAIN = ""
    HERO = "hero_icon"
    KING = "king_icon"
    TERRITORY = "territory_icon"
    GUILD = "guild_icon"
    SHOP = "shop_icon"

class Navigator:
    def __init__(self, hwnd, timeout: float = 1.0):
        self.hwnd = hwnd
        self.timeout = timeout
        self.current_page: Page = Page.HERO
        self.images = load_templates(Path(TEMPLATES_FOLDER_NAME))
    
    def move_to(self, page: Page) -> bool:
        if page != self.current_page:
            frame = capture_window(self.hwnd)
            match = match_image(frame, self.images[page.value], "bottom")
            if match:
                cx, cy = match
                adb.click(cx, cy)
                self.current_page = page
                time.sleep(self.timeout)
                return True
            else:
                print(f"Icon for {page.value} not found")
                return False
        return True

    def move_in_page(self, image: str, region = "whole") -> bool:
        frame = capture_window(self.hwnd)
        match = match_image(frame, self.images[image], region)
        if match:
            cx, cy = match
            adb.click(cx, cy)
            time.sleep(self.timeout)
            return True
        else:
            print(f"Icon for {image} not found")
            return False
    
    def return_to_main(self) -> bool:
        frame = capture_window(self.hwnd)
        match = match_image(frame, self.images["return_icon"], "bottom")
        if match:
            cx, cy = match
            adb.click(cx, cy)
            self.current_page = Page.MAIN
            time.sleep(self.timeout)
            return True
        else:
            print("Return icon not found")
            return False
    
    def get_current_page(self) -> Page:
        return self.current_page
    
    def is_on_page(self, page: Page) -> bool:
        return self.current_page == page
    
    def __str__(self) -> str:
        return f"Navigator(current={self.current_page.value})"
