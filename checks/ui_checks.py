from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.firefox.options import Options


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
            return {
                "url": url,
                "title": "",
                "title_exists": False,
                "ui_status": "ERROR",
                "error": "Page load timeout"
            }

        title = driver.title.strip()

        return {
            "url": url,
            "title": title,
            "title_exists": bool(title),
            "ui_status": "PASS" if title else "WARN"
        }

    except WebDriverException as error:
        return {
            "url": url,
            "title": "",
            "title_exists": False,
            "ui_status": "ERROR",
            "error": str(error)
        }

    except Exception as error:
        return {
            "url": url,
            "title": "",
            "title_exists": False,
            "ui_status": "ERROR",
            "error": str(error)
        }

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass