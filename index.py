from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://www.etf.com/etfanalytics/etf-finder')

time.sleep(10)

button_100 = driver.find_element("xpath",
                                '/html/body/div[5]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/section[2]/div[1]/div/div[4]/button/label/span')

button_100.click()


number_pages = driver.find_element("xpath", '//*[@id="totalPages"]')

number_pages = number_pages.text.replace("of ", "")

number_pages = int(number_pages)


element = driver.find_element("xpath", '//*[@id="finderTable"]')

html_table = element.get_attribute('outerHTML')

table = pd.read_html(str(html_table))[0]


list_table_per_page = []

element = driver.find_element("xpath", '//*[@id="finderTable"]')

for page in range(1, number_pages + 1):

    html_table = element.get_attribute('outerHTML')

    table = pd.read_html(str(html_table))[0]

    list_table_per_page.append(table)

    button_advance_page = driver.find_element("xpath", '//*[@id="nextPage"]')

    driver.execute_script("arguments[0].click();", button_advance_page)


table_register_etfs = pd.concat(list_table_per_page)


form_back_to_page = driver.find_element(
    "xpath", '//*[@id="goToPage"]')

form_back_to_page.clear()
form_back_to_page.send_keys("1")
form_back_to_page.send_keys(u'\ue007')

button_change_to_performance = driver.find_element(
    "xpath", '/html/body/div[5]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/ul/li[2]/span')

button_change_to_performance.click()


list_table_per_page = []

element = driver.find_element("xpath", '//*[@id="finderTable"]')

for page in range(1, number_pages + 1):

    html_table = element.get_attribute('outerHTML')

    table = pd.read_html(str(html_table))[0]

    list_table_per_page.append(table)

    button_advance_page = driver.find_element("xpath", '//*[@id="nextPage"]')

    driver.execute_script("arguments[0].click();", button_advance_page)


table_rentabilidade_etfs = pd.concat(list_table_per_page)

table_rentabilidade_etfs

driver.quit()

table_rentabilidade_etfs = table_rentabilidade_etfs.set_index("Ticker")
table_rentabilidade_etfs = table_rentabilidade_etfs[[
    '1 Year', '3 Years', '5 Years']]
table_register_etfs = table_register_etfs.set_index("Ticker")

base_de_dados_final = table_register_etfs.join(
    table_rentabilidade_etfs, how='inner')

print(base_de_dados_final)
