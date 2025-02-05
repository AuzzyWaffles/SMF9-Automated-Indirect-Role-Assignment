from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from tkinter import messagebox
import time
import sys
import os


def get_scheduled_associates(shift, date):

    if shift == 'MOR':
        shift = '04-00-00'
    elif shift == 'DAY':
        shift = '09-30-00'
    elif shift == 'TWI':
        shift = '15-00-00'
    else:
        shift = '20-30-00'

    year = date.strftime('%Y')
    day_of_week = date.strftime('%a')
    month_num = date.month
    month = date.strftime('%b')
    day = date.day
    day_decimal = date.strftime('%d')

    # Setup webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)

    timeout = sys.maxsize
    wait = WebDriverWait(driver, timeout)
    wait_short = WebDriverWait(driver, 20)

    # Go to Scheduling Site
    driver.get(os.getenv('SCHEDULING_SITE'))

    # Log into Midway
    driver.find_element(By.XPATH, '//*[@id="user_name"]').send_keys(os.getenv('USERNAME'))
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(os.getenv('MIDWAY_PASSWORD'))
    driver.find_element(By.XPATH, '//*[@id="verify_btn"]').click()
    wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div/div/nav/a/img')))

    # Find and click the date entry element
    try:
        wait_short.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="date-picker"]')))
    except TimeoutException:
        driver.close()
        messagebox.showinfo(title="Error", message='Scheduling Site took too long to load, please try again.')
        return False

    # Enter the date that was entered by the user, have to do it twice
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
    try:
        wait_short.until(ec.visibility_of_element_located((By.ID, f'time-cell-{day_of_week}-{month}-{day_decimal}-{shift}')))
    except TimeoutException:
        driver.close()
        messagebox.showinfo(title="Error", message='Scheduling Site took too long to load, please try again.')
        return False

    driver.find_element(By.ID, f'time-cell-{day_of_week}-{month}-{day_decimal}-{shift}').click()

    # Scroll to the top of the screen
    driver.execute_script("window.scrollTo(0, 0);")

    # Find, scroll, and click the 'Select display attribute' button
    wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="loading-bar"]/div[1]/div[1]/button')))
    attribute_button = driver.find_element(By.XPATH, '//*[@id="loading-bar"]/div[1]/div[1]/button')
    driver.execute_script("arguments[0].scrollIntoView(true);", attribute_button)
    attribute_button.click()

    # Uncheck boxes on attribute list
    wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[1]/input')))
    driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[4]/input').click()
    driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[6]/input').click()
    driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[7]/input').click()
    driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[8]/input').click()
    driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[10]/input').click()
    driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[11]/input').click()
    driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[12]/input').click()
    driver.find_element(By.XPATH, '//*[@id="roster-details-multi-checkbox"]/div[13]/input').click()

    # Click submit button
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

    if shift == '20-30-00' and (day_of_week == 'Thu' or day_of_week == 'Fri' or day_of_week == 'Sat'):
        logins.add(os.getenv('EXCEPTION_AA'))

    driver.close()

    return logins
