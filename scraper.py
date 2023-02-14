import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


class Scraper:
    def __init__(self, year_range=(1956, 2022), sleep_time_range=(1,3)):
        self.sleep_time_range = sleep_time_range
        self.year_range = year_range
        self.BASE = 'https://www.basketball-reference.com/'
        self.mvp_year_urls = self.create_mvp_year_urls(self.year_range)

    def pause(self):
        time.sleep(random.uniform(self.sleep_time_range[0], self.sleep_time_range[1]))
    
    def create_mvp_year_urls(self, year_range):
        urls = [f'{self.BASE}awards/awards_{year}.html' for year in range(year_range[0], year_range[1] + 1)]
        return urls

    def get_mvp_stats(self, url):
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        stat_names = table.find('thead').find_all('tr')[-1].find_all('th')
        stat_names = [stat.text for stat in stat_names][1:]
        stats = [[item.text for item in row.find_all('td')] for row in table.find('tbody').find_all('tr')]
        df = pd.DataFrame(columns=stat_names, data=stats)   
        return df

    def get_all_mvp_stats(self):
        df_list = []
        for i, url in enumerate(self.mvp_year_urls):
            df_list.append(self.get_mvp_stats(url))
            print(f'Finished {i}/{len(self.mvp_year_urls)}')
            self.pause()
        return pd.concat(df_list)