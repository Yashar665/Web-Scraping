import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import requests
from bs4 import BeautifulSoup
import pandas as pd

variable = str(input("Bina növü?\n"))
# variable = "Yeni tikili"
if variable == "Yeni tikili":
    search_term = 1
elif variable == "Köhnə tikili":
    search_term =2

search_term2 = int(input("Otaq sayı?\n")) + 1
# search_term2 = 4

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('http://www.bina.az/')
time.sleep(5)

element1 = driver.find_element_by_xpath("//div[@class = 'search-row__cell search-row__cell--category']//div[@class = 'selectric']/span[@class = 'button']")
element1.click()
element1 = driver.find_element_by_xpath("//div[@class = 'search-row__cell search-row__cell--category']//div[@class = 'selectric-items']//ul/li[@data-index = {}]".format(search_term))
element1.click()

time.sleep(10)

element2 = driver.find_element_by_xpath("/html/body/div//div[3]/div/form/div[1]/div[3]/div[1]/div[2]/span[2]")
element2.click()                        
element2 = driver.find_element_by_xpath("/html/body/div//div[3]/div/form/div[1]/div[3]/div[1]/div[3]/div/ul/li[{}]".format(search_term2))
element2.click()

#get all hyperlinks----------
elems = driver.find_elements_by_xpath("/html/body/div[5]/section/div/div[2]/div[3]/nav/div/span//a")
links = []
for elem in elems:
    link = elem.get_attribute('href')
    links.append(link)

links[-1] = links[-1][:-1] + str(1)
driver.quit()
#extract info
all_names,all_links, all_prices, all_dates, all_square_meters,= [],[], [], [], []

for l in links:
    page = l
    response = requests.get(page)
    bina_soup = BeautifulSoup(response.content, "html.parser")

    for advert in bina_soup.find_all('div', {'class': 'items-i'}):
        name = advert.find('div', {'class': 'location'}).get_text()
        all_names.append(name)

        link = "https://bina.az/" + advert.find('a').get('href')
        all_links.append(link)

        #price = advert.find('div', {'class': 'price'}).get_text()
        price = int(advert.find('span', {'class': 'price-val'}).get_text().replace(' ',''))
        all_prices.append(price)

        date = advert.find('div', {'class': 'city_when'}).get_text().split(',')[1]
        all_dates.append(date)
        
        square_meters = float(advert.find('ul',{'class':'name'}).get_text(separator = ' ').split()[2])
        all_square_meters.append(square_meters)
    
data_list = list(zip(all_names,all_links, all_dates, all_prices, all_square_meters))
column_names = ['Location','Learn More (Building Link)',
                'Date and Time of Publish', 'Price', 'Square Meters' ]
bina_df = pd.DataFrame(data_list, columns=column_names)
bina_df.drop_duplicates(inplace=True)

file_name = variable + "_" + str(search_term2) + " otaqlı" + ".xlsx"
bina_df.to_excel(file_name,index = False)