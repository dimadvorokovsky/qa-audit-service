from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def save_screenshot(driver):
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = screenshots_dir / f"ui_error_{timestamp}.png"

    driver.save_screenshot(str(screenshot_path))

    return str(screenshot_path)


def get_h1_data(driver):
    try:
        h1 = driver.find_element(By.TAG_NAME, "h1")
        h1_text = h1.text.strip()

        return {
            "h1_exists": True,
            "h1_text": h1_text
        }

    except NoSuchElementException:
        return {
            "h1_exists": False,
            "h1_text": ""
        }


def check_page_title(url):
    driver = None

    try:
        options = Options()
        options.add_argument("-headless")
        options.page_load_strategy = "eager"

        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(30)

        try:
            driver.get(url)

        except TimeoutException:
            screenshot_path = None

            try:
                screenshot_path = save_screenshot(driver)
            except Exception:
                pass

            return {
                "url": url,
                "title": "",
                "title_exists": False,
                "h1_exists": False,
                "h1_text": "",
                "ui_status": "ERROR",
                "error": "Page load timeout",
                "screenshot": screenshot_path
            }

        title = driver.title.strip()
        h1_data = get_h1_data(driver)

        ui_status = "PASS"

        if not title or not h1_data["h1_exists"]:
            ui_status = "WARN"

        return {
            "url": url,
            "title": title,
            "title_exists": bool(title),
            "h1_exists": h1_data["h1_exists"],
            "h1_text": h1_data["h1_text"],
            "ui_status": ui_status,
            "screenshot": None
        }

    except WebDriverException as error:
        screenshot_path = None

        if driver is not None:
            try:
                screenshot_path = save_screenshot(driver)
            except Exception:
                pass

        return {
            "url": url,
            "title": "",
            "title_exists": False,
            "h1_exists": False,
            "h1_text": "",
            "ui_status": "ERROR",
            "error": str(error),
            "screenshot": screenshot_path
        }

    except Exception as error:
        screenshot_path = None

        if driver is not None:
            try:
                screenshot_path = save_screenshot(driver)
            except Exception:
                pass

        return {
            "url": url,
            "title": "",
            "title_exists": False,
            "h1_exists": False,
            "h1_text": "",
            "ui_status": "ERROR",
            "error": str(error),
            "screenshot": screenshot_path
        }

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass