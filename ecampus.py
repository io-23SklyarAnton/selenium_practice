import time
from copy import copy
from pprint import pprint
import pickle
import threading

from selenium import webdriver
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ecampus_config import options_configuration


def _open_grades_table(browser: WebDriver, discipline: WebElement):
    browser.execute_script("window.open(arguments[0], '_blank');", discipline.get_attribute("href"))


def _parse_grades_table(browser: WebDriver, discipline: WebElement) -> None:
    discipline_name = discipline.text

    browser.switch_to.window(browser.window_handles[1])
    rows = browser.find_elements(By.CSS_SELECTOR, '#cMonitoringRow tbody tr')

    rows_text = [[row.text for row in rows]]
    print(discipline_name)
    pprint(rows_text)
    browser.close()
    browser.switch_to.window(browser.window_handles[0])


def _show_grades_tables(browser: WebDriver) -> None:
    """print a disciplines names and a list of the table rows with grades of the all student disciplines"""
    disciplines = browser.find_elements(
        By.XPATH,
        f'//div[@class="studySheetBox"]/table/tbody/tr/td[1]/a'
    )
    threads = [threading.Thread(target=_open_grades_table, args=(browser, discipline)) for discipline in
               disciplines]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    [_parse_grades_table(browser, discipline) for discipline in disciplines]


def _campus_authentication(browser: WebDriver) -> None:
    # authentication
    browser.find_element(By.XPATH, '//input[@placeholder="Логін"]').send_keys(os.getenv("LOGIN"))
    browser.find_element(By.XPATH, '//input[@placeholder="Пароль"]').send_keys(os.getenv("PASSWORD"))
    browser.find_element(By.XPATH, '//input[@value="Вхід"]').click()


def _save_or_using_cookie_to_auth(browser: WebDriver) -> None:
    """if cookie file already exists - auth via cookies,
       if not - use env variables to login and then save the cookies file"""
    cookies_path = f"cookies\\{os.getenv('LOGIN')}"

    if os.path.exists(cookies_path):
        with open(cookies_path, "rb") as f:
            for cookie in pickle.load(f):
                browser.add_cookie(cookie)
        browser.get('https://ecampus.kpi.ua/home')
    else:
        _campus_authentication(browser)
        time.sleep(2)
        with open(cookies_path, "wb") as f:
            pickle.dump(browser.get_cookies(), f)


def _path_to_the_grades_tables(browser: WebDriver) -> None:
    browser.find_element(
        By.XPATH,
        '//*[@id="root"]/div/div/div/div/div/div[1]/div[1]/div/div/p[3]/button').click()
    browser.find_element(By.LINK_TEXT, 'Поточний контроль').click()


def show_student_grades() -> None:
    """Parses KPI Campus site to collect all student grades"""

    browser = webdriver.Chrome(options=options_configuration())
    browser.implicitly_wait(5)
    try:
        browser.get("https://ecampus.kpi.ua/login")

        # authentication
        _save_or_using_cookie_to_auth(browser)

        # path to the grades tables
        _path_to_the_grades_tables(browser)

        _show_grades_tables(browser)

    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()


if __name__ == '__main__':
    load_dotenv()

    show_student_grades()
