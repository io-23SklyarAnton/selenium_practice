from pprint import pprint
from typing import Tuple
import pickle

from selenium import webdriver
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from ecampus_config import options_configuration

load_dotenv()


def _parse_grade_table(browser: WebDriver, table_num: int) -> Tuple[str, list]:
    """return a discipline name and a list of the table rows with grades of this discipline"""
    discipline = browser.find_element(
        By.XPATH,
        f'/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div/table/tbody/tr[{table_num}]/td[1]/a'
    )
    discipline_name = discipline.text
    discipline.click()
    rows = browser.find_elements(By.CSS_SELECTOR, '#cMonitoringRow tbody tr')
    return discipline_name, [row.text for row in rows]


def _campus_authentication(browser: WebDriver) -> None:
    # authentication
    browser.find_element(
        By.XPATH,
        '//*[@id="root"]/div/div/div/section/div[1]/div[2]/div/div/div/div/form/fieldset/div[1]/input') \
        .send_keys(os.getenv("LOGIN"))
    browser.find_element(
        By.XPATH,
        '//*[@id="root"]/div/div/div/section/div[1]/div[2]/div/div/div/div/form/fieldset/div[2]/input') \
        .send_keys(os.getenv("PASSWORD"))
    browser.find_element(
        By.XPATH,
        '//*[@id="root"]/div/div/div/section/div[1]/div[2]/div/div/div/div/form/fieldset/div[3]/input').click()


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

        for table_num in range(23, 30):
            grades_table = _parse_grade_table(browser, table_num)
            print(grades_table[0])
            pprint(grades_table[1])
            # return back to the all tables
            browser.find_element(By.LINK_TEXT, 'Поточний контроль').click()

    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()


if __name__ == '__main__':
    show_student_grades()
