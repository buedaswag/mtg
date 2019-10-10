#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import time
from sqlalchemy import create_engine
import pickle
import os
from pathlib import Path
from psycopg2.errors import UndefinedTable
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())


# In[2]:


class TimeLimitExpired(Exception):
    pass

def load_page(url, card_name, debug = False):
    '''
    setup - load entire page, pressing 'show more' button
    '''
    
    #fix card name
    card_name = card_name.replace('/', '-')
    
    #load debug file
    debug_path = Path(os.path.join(Path().absolute() , 'debug'))
    pickle_file = Path(os.path.join(debug_path , '%s.pickle'%card_name))
    if debug == True and pickle_file.is_file():
        html = None
        with open(pickle_file, 'rb') as file:
            html = pickle.load(file)
        return html
    
    driver_path = Path(os.path.join(Path().absolute(), 'selenium_drivers', 'chromedriver'))
    #driver = webdriver.Chrome(driver_path)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    delay = 2
    timeout = 0
    html = None
    try:
        while True:
            try:
                driver.find_element_by_xpath(r"//span[contains(text(),'Show more results')]").click()
                #reset timeout
                timeout = 0
                time.sleep(delay)
            except ElementClickInterceptedException as e:
                if timeout >= 60:
                    raise TimeLimitExpired('timeout >= 60')
                time.sleep(delay)
                timeout += delay
    except ElementNotInteractableException as e:
        #now we have all the data, SCRAPE IT!!!
        html = driver.page_source.encode('utf-8')
        
        #dump file for debug if no file exists
        if not debug_path.is_dir():
            os.makedirs(debug_path)
        if pickle_file.is_file() == False:
            with open(pickle_file, 'wb') as file:
                pickle.dump(html, file, protocol=pickle.HIGHEST_PROTOCOL)
            
    finally:
        driver.quit()
        
    return html


# In[3]:


def get_soup(html):
    '''
    setup with selenium: get the html to scrape
    '''

    soup = BeautifulSoup(html, 'lxml')
    table_tag = soup.find_all('div', class_="table-body")
    table = table_tag[0]
    info_tag = soup.find_all('div', class_='tab-container d-flex flex-column h-100')
    info = info_tag[0]
    
    return info, table


# In[4]:


def get_sales_available_items(row_tag):
    tag=row_tag.find_all('span', class_='badge badge-faded d-none d-sm-inline-flex has-content-centered mr-1 sell-count')[0]#.get_text().strip()
    regex = r'\d+\sSales\s|\s\d+\sAvailable\sitems'
    match = re.findall(regex, str(tag))
    sales = match[0][:-7]
    available_items = match[1][1:-16]
    return sales, available_items

def get_product_information(row_tag):
    tag=row_tag.find_all('div', class_='product-attributes col-auto col-md-12 col-xl-5')[0]#.get_text().strip()
    regex = r'showMsgBox\(this,\'.*?\'\)'
    match = re.findall(regex, str(tag))
    
    item_conditions = match[0][17:-2]
    item_languages = match[1][17:-2]
    
    item_is_playset = False
    for item in match:
        if item[17:-2] == 'Playset':
            item_is_playset = True

    item_is_foil = False
    for item in match:
        if item[17:-2] == 'Foil':
            item_is_foil = True
    return item_conditions, item_languages, item_is_playset, item_is_foil

def get_data(row_tags, card_name, debug=False):
    '''
    iterate through each row in the table, getting the data
    '''
    
    seller_names = []
    item_prices = []
    item_amounts = [] 
    seller_sales = []
    seller_available_items = []
    item_locations = []
    item_conditions = []
    item_languages = []
    item_is_playsets = []
    item_is_foils = []
    
    for row_tag in row_tags:
        seller_names.append(row_tag.find_all('span', class_='d-flex has-content-centered mr-1')[0].get_text().strip())

        item_prices.append(row_tag.find_all('span', class_='font-weight-bold color-primary small text-right text-nowrap')[0].get_text().strip()[:-2])

        item_amounts.append(row_tag.find_all('span', class_='item-count small text-right')[0].get_text().strip()[:])

        sales, available_items = get_sales_available_items(row_tag)
        seller_sales.append(sales)
        seller_available_items.append(available_items)

        item_locations.append(row_tag.find_all('span', class_='icon d-flex has-content-centered mr-1')[0]['title'][15:])

        item_condition, item_language, item_is_playset, item_is_foil= get_product_information(row_tag)
        item_conditions.append(item_condition)
        item_languages.append(item_language)
        item_is_playsets.append(item_is_playset)
        item_is_foils.append(item_is_foil)
    
    '''
    put it into pandas
    '''
    data_dict = {
        'card_name': [card_name for i in range(len(seller_names))],
        'ts': [pd.Timestamp.now(tz='UTC') for i in range(len(seller_names))],
        'list_order': [i for i in range(len(seller_names))], 
        'seller_name': seller_names,
        'seller_sales': seller_sales,
        'seller_available_items': seller_available_items,
        'item_price': item_prices,
        'item_amount': item_amounts,
        'item_location': item_locations,
        'item_condition': item_conditions,
        'item_language': item_languages,
        'item_is_playset': item_is_playsets,
        'item_is_foil': item_is_foils,
    }
    df = pd.DataFrame(data_dict)
    
    '''
    change some datatypes
    '''
    df.seller_sales = df.seller_sales.astype(int)
    df.seller_available_items = df.seller_available_items.astype(int)
    df.item_amount = df.item_amount.astype(int)
    df.item_price = df.item_price.str.replace(',', '.')
    df.item_price = df.item_price.astype(float)
    
    '''
    make some replacements
    '''
    df.item_condition = df.item_condition.replace(
        {'Mint': 'M', 'Near Mint': 'NM', 'Excellent': 'EX', 
         'Good': 'GD', 'Light Played': 'LP', 'Played': 'PL', 'Poor': 'P'})

    '''
    correct for playsets:
    '''
    df.loc[df.item_is_playset == True, 'item_price'] =         df.loc[df.item_is_playset == True, 'item_price'] / 4
    df.loc[df.item_is_playset == True, 'item_amount'] =         df.loc[df.item_is_playset == True, 'item_amount'] * 4

    if debug == True:
        display('seller_names', len(seller_names), seller_names[:10], 
            'item_prices', len(item_prices), item_prices[:10], 
            'item_amounts', len(item_amounts), item_amounts[:10], 
            'item_locations', len(item_locations), item_locations[:10], 
            'item_conditions', len(item_conditions), item_conditions[:10], 
            'item_languages', len(item_languages), item_languages[:10], 
            'item_is_playsets', len(item_is_playsets), 'True: %d, False: %d'%(len([i for i in item_is_playsets if item_is_playsets[i]==True]), len([i for i in item_is_playsets if item_is_playsets[i]==False])), 
            'item_is_foils', len(item_is_foils), 'True: %d, False: %d'%(len([i for i in item_is_foils if item_is_foils[i]==True]), len([i for i in item_is_foils if item_is_foils[i]==False])))
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            display(df)
    return df


# In[5]:


''' 
CREATE DATABASE

sudo su - postgres 
psql
create database mtg;
\l # list databases, then press q to go back to db console

\q # to exit:

\dt # list tables of the public schema

CREATE TABLE card_listings (
  card_name varchar(100), 
  ts timestamp, 
  list_order int, 
  seller_name varchar(30), 
  seller_sales int, 
  seller_available_items int, 
  item_price int, 
  item_amount int, 
  item_location varchar(30), 
  item_condition char(2), 
  item_language varchar(20),  
  item_is_playset boolean, 
  item_is_foil boolean,
  PRIMARY KEY (card_name, ts, list_order)
);


  ID INT REFERENCES Artists(ID),
  BID INT REFERENCES Bands(BID),
  NAME CHAR(40) NOT NULL,
  DATE_JOIN date,
  PRIMARY KEY (ID, BID)
);

'''
def get_db_connection():
    username = 'mig'
    password = 'password' 
    host_name = 'localhost'
    port = 5432
    db_name = 'mtg'
    conn_str = 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host_name, port, db_name)

    engine = create_engine(conn_str)
    return engine


# In[6]:


now = pd.Timestamp.now() #Timestamp('2019-10-09 15:09:44.173350+0000')
minute = 0 if now.minute < 30 else 30
minute


# In[7]:


def conditional_insert(engine, card_name, frequency=30, debug = False):
    '''
    Checks if its time to insert records in the database.
    We only want to insert records with a frequency of frequency.
    
    engine - the db engine
    card_name - the card name
    frequency - the frequency of db inserts
    '''
    
    now = pd.Timestamp.now() #Timestamp('2019-10-09 15:09:44.173350+0000')
    minute = 0 if now.minute < 30 else 30
    now_date_time_hour = pd.Timestamp(now.year, now.month, now.day, now.hour, minute)
    
    #minus 1 minute to prevent conflicts with cron
    now_date_time_hour_puls_frequency_min = now_date_time_hour + pd.Timedelta('%d minutes'%(frequency - 1))
    
    query = '''
    SELECT COUNT(*)  
    FROM card_listings
    WHERE card_name = '%s' 
    AND ts::time BETWEEN '%s' AND '%s';
    '''%(card_name, now_date_time_hour, now_date_time_hour_puls_frequency_min)
    
    df_result = pd.read_sql_query(query, engine)
    
    if debug==True:
        print(query)
    
    return df_result.iloc[0][0], now_date_time_hour, now_date_time_hour_puls_frequency_min


# In[8]:


14.5*2*24*31


# In[9]:


def main(debug=False):
    '''
    the 6 debug files have 14.5 MB total
    14.5MB x 2 times per hour x 24 hours x 31 days = 21576 GB per month
    '''
    
    '''
    card_names and links
    '''
    card_names_urls = {
        'Snow Covered Island': 'https://www.cardmarket.com/en/Magic/Products/Singles/Modern-Horizons/Snow-Covered-Island', 
        'Fabled Passage': 'https://www.cardmarket.com/en/Magic/Products/Singles/Throne-of-Eldraine/Fabled-Passage', 
        'Once Upon a Time': 'https://www.cardmarket.com/en/Magic/Products/Singles/Throne-of-Eldraine/Once-Upon-a-Time', 
        'Murderous Rider // Swift End': 'https://www.cardmarket.com/en/Magic/Products/Singles/Throne-of-Eldraine/Murderous-Rider-Swift-End', 
        'Questing Beast': 'https://www.cardmarket.com/en/Magic/Products/Singles/Throne-of-Eldraine/Questing-Beast', 
        'Oko, Thief of Crowns': 'https://www.cardmarket.com/en/Magic/Products/Singles/Throne-of-Eldraine/Oko-Thief-of-Crowns'
    }
    
    engine = get_db_connection()
    
    for card_name in card_names_urls:  
        
        '''
        checks if its time to insert data for this card, and skips it if its not
        '''
        count, start, end = conditional_insert(engine, card_name, frequency=30)
        if count > 0:
            print('There are already %d records from %s to %s'%(count, start, end))
            continue
        
        url = card_names_urls[card_name]
        html = load_page(url, card_name, debug=debug)
        info, table = get_soup(html)
        row_tags = table.find_all('div', class_='row no-gutters article-row')
        df = get_data(row_tags, card_name)
        
        print('inserting records of card %s with shape %s'%(card_name, str(df.shape)))
        
        df.to_sql('card_listings', con=engine, if_exists='append', index=False)
        
        if debug == True:
            print(card_name)
            print(card_names_urls[card_name])
            print(df.shape)
            print(df.dtypes)
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                display(df)
        
if __name__ == '__main__':
    main(debug=False)


# In[12]:


get_ipython().system('jupyter nbconvert --to script prototype_scraping.ipynb')

