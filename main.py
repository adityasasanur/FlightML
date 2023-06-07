import csv
import datetime
from tempfile import mkdtemp
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def handler(event=None, context=None):

    #CHROME OPTIONS
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    s = Service('/opt/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)
    
    NUM_LINKS = 2
    NUM_FLIGHTS = 2

    links = []
    with open('utils/flightLinks.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            links.append(row[0] + tomorrow.strftime("%Y-%m-%d"))

    for url in links[:NUM_LINKS]:

        #RETRIEVE POSSIBLE FLIGHTS FOR EACH AIRPORT COMBINATION
        driver.get(url)
        try:elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "yR1fYc")))
        except: continue

        #ITERATE THROUGH POSSIBLE FLIGHTS
        for i in range(min(NUM_FLIGHTS, len(elements))):

            #GET FLIGHT DATA
            try: WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "yR1fYc")))[i].click()
            except: continue
            try: prices = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ke9kZe-LkdAo-RbRzK-JNdkSc.pKrx3d")))
            except: continue

            print(len(prices))
            for price in prices[-60:]:
                print(price.get_attribute("aria-label"))
            print("NEXT")
            driver.back()

        

    driver.quit()