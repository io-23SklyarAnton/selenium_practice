import time
from pprint import pprint
from typing import Tuple

from selenium import webdriver
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

load_dotenv()


def _parse_grade_table(browser: webdriver, table_num: int) -> Tuple[str, list]:
    """return a discipline name and a list of the table rows with grades of this discipline"""
    discipline = browser.find_element(
        By.XPATH,
        f'/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div/table/tbody/tr[{table_num}]/td[1]/a'
    )
    discipline_name = discipline.text
    discipline.click()
    time.sleep(3)
    rows = browser.find_elements(By.CSS_SELECTOR, '#cMonitoringRow tbody tr')
    return discipline_name, [row.text for row in rows]


def _campus_authentication(browser: webdriver) -> None:
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
    time.sleep(2)


def _path_to_the_grades_tables(browser: webdriver) -> None:
    browser.find_element(
        By.XPATH,
        '//*[@id="root"]/div/div/div/div/div/div[1]/div[1]/div/div/p[3]/button').click()
    time.sleep(3)
    browser.find_element(By.LINK_TEXT, 'Поточний контроль').click()


def english_grades():
    browser = webdriver.Chrome()
    try:
        browser.get("https://ecampus.kpi.ua/login")
        _campus_authentication(browser)

        # path to the grades tables
        _path_to_the_grades_tables(browser)

        for table_num in range(23, 30):
            grades_table = _parse_grade_table(browser, table_num)
            print(grades_table[0])
            pprint(grades_table[1])
            # return back to the all tables
            browser.find_element(By.LINK_TEXT, 'Поточний контроль').click()
            time.sleep(2)
    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()


if __name__ == '__main__':
    english_grades()
