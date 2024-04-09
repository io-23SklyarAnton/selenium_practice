import time

from fake_useragent import UserAgent
from selenium import webdriver


def _get_chrome_user():
    return UserAgent().getChrome


if __name__ == '__main__':
    ua = _get_chrome_user()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={ua}")

    browser = webdriver.Chrome(options=options)
    browser.get("https://www.whatismybrowser.com/detect/what-is-my-user-agent/")
    time.sleep(10)
    browser.close()
    browser.quit()
