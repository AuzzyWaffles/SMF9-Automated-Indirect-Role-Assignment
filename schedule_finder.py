import os
import time
from urllib3.exceptions import ProtocolError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import InvalidSessionIdException, TimeoutException, StaleElementReferenceException


def get_scheduled_associates(display, shift, date):
    year = date.strftime('%Y')
    day_of_week = date.strftime('%a')
    month_num = date.month
    month = date.strftime('%b')
    day = date.day
    day_decimal = date.strftime('%d')

    # Setup webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    wait = WebDriverWait(driver, timeout=10)
    wait_long = WebDriverWait(driver, timeout=60)

    try:
        driver.get(f'https://sspot.iad.corp.amazon.com/{display.site}/schedule-timeline')

        # Wait for Midway to load first
        wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="user_name"]')))

        # Enter username based on OS Login
        driver.find_element(By.XPATH, '//*[@id="user_name"]').send_keys(os.getlogin())

        pin = display.midway_pin()
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(pin)

        # Enter One-Time Password via Security Key
        otp = display.security_key()
        driver.find_element(By.XPATH, '//*[@id="otp"]').send_keys(otp)
        driver.find_element(By.XPATH, '//*[@id="verify_btn"]').click()

        # Wait for SSPOT to load
        wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div/div/nav/a/img')))

        # Enter the date that was entered by the user, have to do it twice
        wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="date-picker"]')))
        for _ in range(2):
            date_entry = driver.find_element(By.XPATH, '//*[@id="date-picker"]')
            date_entry.send_keys(month_num)
            if month_num == 1:
                date_entry.send_keys(Keys.TAB)

            date_entry.send_keys(day)
            if day <= 3:
                date_entry.send_keys(Keys.TAB)

            date_entry.send_keys(year)

            driver.find_element(By.XPATH, '//*[@id="schedule-timeline-current-week-text"]').click()

        # Find and click the relevant shift based on current datetime values
        wait.until(
            ec.visibility_of_element_located((By.ID, f'time-cell-{day_of_week}-{month}-{day_decimal}-{shift}')))
        driver.find_element(By.ID, f'time-cell-{day_of_week}-{month}-{day_decimal}-{shift}').click()

        driver.execute_script('window.scrollTo(0, 0);')

        wait_long.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="loading-bar"]/div[1]/div[1]/button')))
        attribute_button = driver.find_element(By.XPATH, '//*[@id="loading-bar"]/div[1]/div[1]/button')
        driver.execute_script('arguments[0].scrollIntoView(true);', attribute_button)
        attribute_button.click()

        # Uncheck boxes on attribute list
        wait.until(
            ec.visibility_of_element_located((By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[1]/input')))
        driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[4]/input').click()
        driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[6]/input').click()
        driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[7]/input').click()
        driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[8]/input').click()
        driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[10]/input').click()
        driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[11]/input').click()
        driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[12]/input').click()
        driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[13]/input').click()

        driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox-modal-submit-button"]').click()
        time.sleep(1)

        # Get logins and add to logins dictionary
        elements = driver.find_elements(By.CSS_SELECTOR, 'tbody tr td')
        logins = set()
        for element in elements:
            if element.text != '':
                logins.add(element.text)
            else:
                break

        driver.close()

        return logins

    except (TypeError, ProtocolError, InvalidSessionIdException, TimeoutException, StaleElementReferenceException):
        return None
