from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
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

        return {
            "h1_exists": True,
            "h1_text": h1.text.strip()
        }

    except NoSuchElementException:
        return {
            "h1_exists": False,
            "h1_text": ""
        }


def get_interactive_elements_data(driver):
    links = driver.find_elements(By.TAG_NAME, "a")
    buttons = driver.find_elements(By.TAG_NAME, "button")

    return {
        "links_count": len(links),
        "buttons_count": len(buttons),
        "links_exist": len(links) > 0,
        "buttons_exist": len(buttons) > 0
    }


def get_images_data(driver):
    images = driver.find_elements(By.TAG_NAME, "img")

    images_without_alt = []

    for image in images:
        alt = image.get_attribute("alt")
        src = image.get_attribute("src")

        if alt is None or not alt.strip():
            images_without_alt.append(src)

    images_count = len(images)
    images_without_alt_count = len(images_without_alt)
    images_with_alt_count = images_count - images_without_alt_count

    return {
        "images_count": images_count,
        "images_with_alt_count": images_with_alt_count,
        "images_without_alt_count": images_without_alt_count,
        "images_without_alt": images_without_alt
    }


def create_firefox_driver():
    options = Options()
    options.add_argument("-headless")
    options.page_load_strategy = "eager"

    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(30)

    return driver


def get_error_result(
    url,
    error_message,
    screenshot_path=None
):
    return {
        "url": url,
        "title": "",
        "title_exists": False,
        "h1_exists": False,
        "h1_text": "",
        "links_count": 0,
        "buttons_count": 0,
        "links_exist": False,
        "buttons_exist": False,
        "images_count": 0,
        "images_with_alt_count": 0,
        "images_without_alt_count": 0,
        "images_without_alt": [],
        "ui_status": "ERROR",
        "error": error_message,
        "screenshot": screenshot_path
    }


def check_page_title(url, driver=None):
    own_driver = driver is None

    if own_driver:
        driver = create_firefox_driver()

    try:
        try:
            driver.get(url)

        except TimeoutException:
            screenshot_path = None

            try:
                screenshot_path = save_screenshot(driver)
            except Exception:
                pass

            return get_error_result(
                url=url,
                error_message="Page load timeout",
                screenshot_path=screenshot_path
            )

        title = driver.title.strip()
        h1_data = get_h1_data(driver)
        interactive_data = get_interactive_elements_data(driver)
        images_data = get_images_data(driver)

        ui_status = "PASS"

        if not title or not h1_data["h1_exists"]:
            ui_status = "WARN"

        if images_data["images_without_alt_count"] > 0:
            ui_status = "WARN"

        return {
            "url": url,
            "title": title,
            "title_exists": bool(title),
            "h1_exists": h1_data["h1_exists"],
            "h1_text": h1_data["h1_text"],
            "links_count": interactive_data["links_count"],
            "buttons_count": interactive_data["buttons_count"],
            "links_exist": interactive_data["links_exist"],
            "buttons_exist": interactive_data["buttons_exist"],
            "images_count": images_data["images_count"],
            "images_with_alt_count": images_data["images_with_alt_count"],
            "images_without_alt_count": images_data[
                "images_without_alt_count"
            ],
            "images_without_alt": images_data["images_without_alt"],
            "ui_status": ui_status,
            "screenshot": None
        }

    except WebDriverException as error:
        screenshot_path = None

        try:
            screenshot_path = save_screenshot(driver)
        except Exception:
            pass

        return get_error_result(
            url=url,
            error_message=str(error),
            screenshot_path=screenshot_path
        )

    except Exception as error:
        screenshot_path = None

        try:
            screenshot_path = save_screenshot(driver)
        except Exception:
            pass

        return get_error_result(
            url=url,
            error_message=str(error),
            screenshot_path=screenshot_path
        )

    finally:
        if own_driver:
            try:
                driver.quit()
            except Exception:
                pass