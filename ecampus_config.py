from fake_useragent import UserAgent
from selenium import webdriver


def _add_user_agent(options):
    ua = UserAgent().getChrome
    options.add_argument(f"user-agent={ua}")
    return options


def options_configuration() -> webdriver.IeOptions:
    options = webdriver.ChromeOptions()

    _add_user_agent(options)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")

    return options


if __name__ == '__main__':
    import time

    browser = webdriver.Chrome(options=options_configuration())
    try:
        browser.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
        time.sleep(10)
    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()
