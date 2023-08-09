import csv
import datetime
import json
import boto3
from tempfile import mkdtemp
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def handler(event=None, context=None):
    start_time = time.time()

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
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("enable-automation")
    options.add_argument("start-maximized")
    options.page_load_strategy = 'eager'

    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    s = Service('/opt/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)


    NUM_FLIGHTS = 3    
    links = event.get('links')
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    cols = ["departure_airport_int",
            "arriving_airport_int",
            "departure_time_float",
            "airline_int",
            "date_year",
            "date_month",
            "date_day",
            "date_dow",
            "duration_hours",
            "numStops",
            "price_min_day",
            "price_min",
            "Day 0",
            "Day 1",
            "Day 2",
            "Day 3",
            "Day 4",
            "Day 5",
            "Day 6",
            "Day 7",
            "Day 8",
            "Day 9",
            "Day 10",
            "Day 11",
            "Day 12",
            "Day 13",
            "Day 14",
            "Day 15",
            "Day 16",
            "Day 17",
            "Day 18",
            "Day 19",
            "Day 20",
            "Day 21",
            "Day 22",
            "Day 23",
            "Day 24",
            "Day 25",
            "Day 26",
            "Day 27",
            "Day 28",
            "Day 29",
            "Day 30",
            "Day 31",
            "Day 32",
            "Day 33",
            "Day 34",
            "Day 35",
            "Day 36",
            "Day 37",
            "Day 38",
            "Day 39",
            "Day 40",
            "Day 41",
            "Day 42",
            "Day 43",
            "Day 44",
            "Day 45",
            "Day 46",
            "Day 47",
            "Day 48",
            "Day 49",
            "Day 50",
            "Day 51",
            "Day 52",
            "Day 53",
            "Day 54",
            "Day 55",
            "Day 56",
            "Day 57",
            "Day 58",
            "Day 59",
            "Day 60",
            ]
    dict_arr = []


    for url in links:
        #RETRIEVE POSSIBLE FLIGHTS FOR EACH AIRPORT COMBINATION
        driver.get(url)
        try: elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "yR1fYc")))
        except: continue

        #ITERATE THROUGH POSSIBLE FLIGHTS
        for i in range(min(NUM_FLIGHTS, len(elements))):

            #GET FLIGHT DATA
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "yR1fYc")))[i].click()
            except Exception as e:
                print("couldn't get to the link")
                continue

            #PARSE PRICES
            try:
                prices = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ke9kZe-LkdAo-RbRzK-JNdkSc.pKrx3d")))
                priceGraph = []
                for price in prices[-61:][::-1]:
                    price = price.get_attribute("aria-label")
                    priceGraph.append(int(price.split(' ')[-1][1:]))
                price_min = min(priceGraph)
                priceGraph += [None]*(61 - len(priceGraph))
                price_min_day = priceGraph.index(price_min)
            except Exception as e:
                print("couldn't get to the flight")
                print("url: ", url)
                print(i)
                driver.back()
                continue

            try:
                #PARSE STOPS
                stopWrapper = driver.find_element(By.CLASS_NAME, "EfT7Ae.AdWm1c.tPgKwe")
                stops = stopWrapper.find_element(By.CLASS_NAME, "ogfYpf").get_attribute("aria-label").split(" ")[0]
                numStops = int(stops) if stops.isnumeric() else 0

                #PARSE DURATION(HOURS)
                duration = driver.find_element(By.CLASS_NAME, "gvkrdb.AdWm1c.tPgKwe.ogfYpf").get_attribute("aria-label").split(' ')
                duration_hours = duration[2]

                #GET DATE
                date_year, date_month, date_day, date_dow = tomorrow.year%2000, tomorrow.month, tomorrow.day, tomorrow.weekday()

                #GET AIRLINE
                airline = driver.find_element(By.CLASS_NAME, "sSHqwe.tPgKwe.ogfYpf").find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
                airlineEncoding = json.load(open("airlineEncodings.json"))
                airline_int = airlineEncoding[airline]

                #GET DEPARTURE
                departure_time = driver.find_element(By.XPATH,"//span[@jscontroller=\"cNtv4b\"]").find_element(By.TAG_NAME, "span").get_attribute("innerHTML").split('\u202f')
                departure_time_hhmm = departure_time[0].split(":")
                departure_time_float = round(int(departure_time_hhmm[0]) + 12 * (departure_time[1] == "PM") + int(departure_time_hhmm[1])/60, 3)

                #GET DEPARTING/ARRIVING AIRPORT
                departure_airport = driver.find_element(By.XPATH,"(//span[@jscontroller=\"cNtv4b\"])[3]").get_attribute("innerHTML")
                arriving_airport = driver.find_element(By.XPATH,"(//span[@jscontroller=\"cNtv4b\"])[4]").get_attribute("innerHTML")
                airportEncoding = json.load(open("airportEncodings.json"))
                departure_airport_int = airportEncoding[departure_airport]
                arriving_airport_int = airportEncoding[arriving_airport]

                FINAL_DATA_ROW = [departure_airport_int, arriving_airport_int, departure_time_float, airline_int, date_year, date_month, date_day, date_dow, duration_hours, numStops, price_min_day, price_min] + priceGraph

                row = {}
                for col,val in zip(cols,FINAL_DATA_ROW):
                    row[col] = val
                dict_arr.append(row)
            except Exception as e:
                print("couldn't find data")
                print("url: ", url)
                print(i)
                driver.back()
                continue

            driver.back()

    driver.quit()

    # Put Data into S3
    df = pd.DataFrame.from_dict(dict_arr)
    print(links)
    output = bytes(df.to_csv(lineterminator='\r\n', index=False), encoding='utf-8')
    s3 = boto3.client('s3')
    s3.put_object(Body=output, Bucket='google-flight-data-db', Key=tomorrow.strftime("%Y-%m-%d") + "/" + str(event.get('batch_num')) + '.csv')
    end_time = time.time()
    return {
        'statusCode': 200,
        'body': json.dumps('Execution time = %.6f seconds' % (end_time-start_time))
    }
