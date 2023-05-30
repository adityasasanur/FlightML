from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import cloudscraper
# https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDIzLTA1LTI4agcIARIDQVRMcgcIARIDU05BQAFIAXABggELCP___________wGYAQI
# https://www.google.com/travel/flights/booking?tfs=CBwQAhpiEgoyMDIzLTA1LTI4IiAKA0FUTBIKMjAyMy0wNS0yOBoDTEFTKgJOSzIEMTM2MSIgCgNMQVMSCjIwMjMtMDUtMjgaA1NOQSoCTksyBDE4NDlqBwgBEgNBVExyBwgBEgNTTkFAAUgBcAGCAQsI____________AZgBAg&tfu=CnhDalJJWVcxS1NUWnNRWGRrTjBWQlZIRm5jVUZDUnkwdExTMHRMUzB0ZVhOamEzVXhNRUZCUVVGQlIxSjVhM05KUjJwbE5VRkJFZzFPU3pFek5qRjhUa3N4T0RRNUdnc0kvcUVDRUFJYUExVlRSRGdjY1A2aEFnPT0SAggBIgcSBVgxZkRM
# ke9kZe-LkdAo-RbRzK-JNdkSc pKrx3d
# https://www.google.com/travel/flights?q=one%20way%20Flights%20to%20SNA%20from%20ATL%20on%202023-09-13
https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDIzLTA5LTEzagwIAhIIL20vMDEzeXFyDAgCEggvbS8wamJyckABSAFwAYIBCwj___________8BmAEC
click:O1htCb;gP4E0b:O1htCb;DIjhEc:YmNhJf
BXUrOb
https://www.google.com/travel/flights/booking?tfs=CBwQAhpqEgoyMDIzLTA5LTEzIiAKA0FUTBIKMjAyMy0wOS0xMxoDTEFTKgJOSzIEMTM2MSIeCgNMQVMSCjIwMjMtMDktMTMaA1NOQSoCTksyAjcxagwIAhIIL20vMDEzeXFyDAgCEggvbS8wamJyckABSAFwAYIBCwj___________8BmAEC&tfu=CnBDalJJWDE5eE9FbFZkRnBwWDBGQlJGZEpkMEZDUnkwdExTMHRMUzB0ZVhOaVltd3pNa0ZCUVVGQlIxSXhZbVl3UzNNek9VRkJFZ3RPU3pFek5qRjhUa3MzTVJvS0NQNVpFQUlhQTFWVFJEZ2NjUDVaEgIIASIA
https://www.google.com/travel/flights/booking?tfs=CBwQAhpJEgoyMDIzLTA5LTEzIh8KA0FUTBIKMjAyMy0wOS0xMxoDU05BKgJETDIDNTUyagwIAhIIL20vMDEzeXFyDAgCEggvbS8wamJyckABSAFwAYIBCwj___________8BmAEC&tfu=CmxDalJJU1RWcVdIaHdXRWMxUjBWQlJEUm1WSGRDUnkwdExTMHRMUzB0ZVhOaVluUXpNRUZCUVVGQlIxSXhZM2x2UzFCTFFVRkJFZ1ZFVERVMU1ob0xDS2FjQWhBQ0dnTlZVMFE0SEhDbW5BST0SAggBIgA


# file = open("test.html", 'r')
# html_doc = file.readlines()
# html_doc = "".join(html_doc)
# soup = BS(html_doc, 'html.parser')
# # print(soup.prettify())
# for price in soup.find_all(class_="ke9kZe-LkdAo-RbRzK-JNdkSc pKrx3d"):
#     price = str(price).split(" ")
#     # print(price)
#     day = price[1].split("\"")[-1]
#     cost = price[5][1:-1]
#     print(day,cost)

url = "https://www.google.com/travel/flights?q=one%20way%20Flights%20to%20SNA%20from%20ATL%20on%202023-09-13"
driver = webdriver.Chrome()
scraper = cloudscraper.create_scraper()
driver.get(url)
html = driver.execute_script("return document.documentElement.outerHTML")
# WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "css_of_a-visible_element")))
# html = driver.page_source
f = open("myfile.txt", "x")
f.write(html)
f.close()
