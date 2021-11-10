from bs4 import BeautifulSoup
import io
import time
import requests
import random
import re
import os
import string
import pandas as pd
import mysql.connector
import time
from datetime import datetime
from pytz import timezone
from dateutil.parser import parse
import pytz

dev_print = False

def ugly():
    req = requests.get("https://airdrops.io/latest/").text
    soup = BeautifulSoup(req, "lxml")
    tables = soup.find_all('article')
    tables.pop(0)
    airdop_list = []
    for table in tables:
        airdrop_info = []
        links = table.find_all('a', href=True)
        print(links)
        test2 = table.text
        test3 = test2.split(" Value:")[0]
        getVals = list([val for val in test3
               if val.isalpha()])
  
        result = "".join(getVals)
        print(result)
        airdrop_info.append(result)
        for link in table.find_all('a', attrs={'href': re.compile("^https://")}):
            airdrop_info.append(link.get('href'))
        social_array = []
        social_list = table.find_all("li", {"class": "reqdrop"})
        
        for list_element in social_list:
            print(list_element.get("title"))
            social_array.append(list_element.get("title"))
        airdrop_info.append(social_array)
        print(table.text)
        print("-----")
        print(table)
        airdop_list.append(airdrop_info)

    print(airdop_list)


def get_airdop_infos(url):
    req = requests.get(url).text
    soup = BeautifulSoup(req, "lxml")
    airdorps = soup.find_all('article')
    airdorps.pop(0)
    airdop_list = []

    for airdrop in airdorps:
        airdrop_info = []
        airdrop_name_dummy = airdrop.text.split(" Value:")[0]
        getVals = list([val for val in airdrop_name_dummy
               if val.isalpha()])
        airdrop_name = "".join(getVals)
        airdrop_info.append(airdrop_name)
        for link in airdrop.find_all('a', attrs={'href': re.compile("^https://")}):
            airdrop_info.append(link.get('href'))

        social_array = []
        social_list = airdrop.find_all("li", {"class": "reqdrop"})
        
        for list_element in social_list:
            social_array.append(list_element.get("title"))
        airdrop_info.append(social_array)
        airdop_list.append(airdrop_info)

    print(airdop_list)
    return airdop_list


def save_wikilist_to_csv():
    url_array = [
    "https://airdrops.io/latest/"
    ]
    for url in url_array:
        while True:
            try:
                req = requests.get(url).text
                soup = BeautifulSoup(req, "lxml")
                break
            except:
                print("error  during  of website tying again in 5 Seconds")
                time.sleep(5)
        
        print(soup.text)
        
        tables = soup.find_all('article')
        tables.pop(0)
        id = 1

        print("----------------------------------")
        for table in tables:
            print(table)


        #     df = pd.read_html(str(table))[0]
        #     df.index.name = "id"
        #     print("Dataframe Done")
        #     dummy = df.columns[0]
        #     if isinstance(dummy, str):
        #         name = dummy
        #     elif isinstance(dummy, tuple):
        #         name = dummy[0]
        #     else:
        #         continue
        #     if len(df) > 1:
        #         print(f"{directory}{scrape_name}_{id}_{name}.csv")
        #         df.to_csv(f"{directory}{scrape_name}_{id}_{name}.csv")
        #         id +=1
        # time.sleep(1)

def parse_lists():
    for filename in os.listdir(directory):
        #just in case something else sneeks into that folder
        if filename.endswith(".csv"):
            #opening one downloaded .html file at a time
            with io.open(directory+filename,"r",encoding="utf-8") as html_file:
                try:
                    df = pd.read_csv(directory+filename,index_col=0)
                    df.index.name = "id"
                    print(df)
                    df.to_csv(f"{directory2}{filename}")
                except os.error as e:
                    print(e)
                    exit()

def combine_lists():
    weapon_list = []
    print(weapon_list)
    for filename in os.listdir(directory):
        #just in case something else sneeks into that folder
        if filename.endswith(".csv"):
            #opening one downloaded .html file at a time
            with io.open(directory+filename,"r",encoding="utf-8") as html_file:
                print(filename.split("_")[0])
                if filename.split("_")[0] == "GearListsWeapons":
                    try:
                        df = pd.read_csv(directory+filename,index_col=0)
                        df["Type"] = filename.split("_")[2].replace(".csv","")
                        weapon_list.append(df)
                    except os.error as e:
                        print(e)
                        exit()    
    weapon_df = pd.concat(weapon_list)
    
    weapon_df["Cost"] = weapon_df["Cost"].apply(lambda x: x.replace("¥","").replace('"','').replace(',',''))
    print(weapon_df)
    weapon_df.to_csv(f"{directory}all.csv")


# save_wikilist_to_csv()
infos = get_airdop_infos("https://airdrops.io/latest/")
infos = get_airdop_infos("https://airdrops.io/hot/")
# print(infos)
