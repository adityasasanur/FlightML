import csv
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

chromium_driver_path = os.getenv('CHROME_DRIVER')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(options=chrome_options, executable_path=chromium_driver_path)
driver = webdriver.Chrome(options=chrome_options)

links = []

with open('flightLinks.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        links.append(row[0] + tomorrow.strftime("%Y-%m-%d"))

for url in links[:4]:
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "yR1fYc")))

        total = min(3, len(elements))
        for i in range(total):
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "yR1fYc")))[i].click()
            except:
                continue

            try:
                prices = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ke9kZe-LkdAo-RbRzK-JNdkSc.pKrx3d")))
            except:
                continue
            print(len(prices))
            # for price in prices[-60:]:
            #     print(price.get_attribute("aria-label"))
            print("NEXT")
            driver.back()
    except:
        continue

driver.quit()