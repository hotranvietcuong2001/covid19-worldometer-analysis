import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import csv
import os.path



url = 'https://www.worldometers.info/coronavirus/'


data = requests.get(url)
soup = BeautifulSoup(data.content, features="lxml")


def string_to_int_with_comma(cell):
    return cell.replace(',', '')


def crawl_covid_today(file_name='covid_data'):
    header = ['Date', 'Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 
                'Total Recovered', 'New Recovered', 'Active Cases', 'Serious Critical',
                'Tot Cases/1M pop', 'Deaths/1M pop', 'Total Tests', 'Tests/1M pop', 'Population']

    data = []

    table = soup.html.find('table', attrs={'id':'main_table_countries_yesterday'})
    rows_table = table.find('tbody').find_all('tr')

    for row in rows_table:
        cells = row.find_all('td')
        cells = [ele.text.strip() for ele in cells]
        if cells[0] != '':
            country_info = cells[1:15]
            country_info[1:] = list(map(string_to_int_with_comma, country_info[1:]))
            date = datetime.date(datetime.now() - timedelta(days=1))
            country_info.insert(0, date)
            data.append(country_info)

    is_exist = True

    if not os.path.isfile(file_name):
        is_exist = False
    
    with open(file_name, 'a', newline='') as fo:
        write = csv.writer(fo)

        if not is_exist:
            write.writerow(header)
        write.writerows(data)



if __name__ == '__main__':
    crawl_covid_today('data/covid_data.csv')
