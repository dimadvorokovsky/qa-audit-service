import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


@pytest.fixture(scope="session")
def browser():
    options = Options()
    options.add_argument("-headless")
    options.page_load_strategy = "eager"

    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(30)

    yield driver

    driver.quit()