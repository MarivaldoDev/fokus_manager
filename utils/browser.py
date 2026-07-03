from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver
from webdriver_manager.firefox import GeckoDriverManager


def make_browser(*options: tuple[str, ...]) -> WebDriver:
    chrome_options = Options()

    if options is not None:
        for option in options:
            chrome_options.add_argument(str(option))

    chrome_service = Service(GeckoDriverManager().install())
    browser = WebDriver(service=chrome_service, options=chrome_options)

    return browser
