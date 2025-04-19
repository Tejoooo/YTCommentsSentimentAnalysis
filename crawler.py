# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time

# Set up Chrome options (optional)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Initialize Chrome driver
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

items = []

try:
    driver.get('https://www.youtube.com/watch?v=IOopJ-PDpac')

    # Initial scroll to trigger comments load
    time.sleep(3)
    driver.execute_script('window.scrollTo(0, 500);')
    time.sleep(3)

    # Scroll multiple times to load more comments
    for i in range(5):
        driver.execute_script('window.scrollBy(0, 3000);')
        time.sleep(3)

    # Extract usernames and comments
    username_elems = driver.find_elements(By.XPATH, '//*[@id="author-text"]')
    comment_elems = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

    for username, comment in zip(username_elems, comment_elems):
        items.append({
            'Author': username.text.strip(),
            'Comment': comment.text.strip()
        })

    # Write to CSV
    filename = r'C:\Users\Archents1\Desktop\crawler\sample.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Author', 'Comment'])
        writer.writeheader()
        writer.writerows(items)

    print(f"✅ Extracted {len(items)} comments.")

finally:
    driver.quit()
