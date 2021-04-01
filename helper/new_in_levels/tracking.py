from bs4 import BeautifulSoup
import json
import requests
import urllib.request
import os


def convert_to_link(hrefs):
    return hrefs['href']



def track_web_site(data):
    """
    Summary
    ------
    Track web site last modified in 

    Args:
        data (dict): Last modified data that is json. It includes the last title which added last data
    """
    page_number = 0
    with open('links.json', 'r') as outfile:
        data_link = json.load(outfile)["data_link"]
    isFinished = False
    result = []
    while isFinished == False:
        isFinished, hrefs =  main_parse_site(data_link[0]["link"].replace('PAGE_NUMBER',str(page_number+1)), data)
        result += hrefs
        page_number += 1
    with open("data/last_data.json", 'w') as out:
        out.write(json.dumps({"url":result[0]}, indent = 4))

def main_parse_site(site_link, data):
    """
    Summary
    ------
    Extract news link from web site up to the given link. 
    If the given link does not exist in the website page then apply this on the next page.

    Args:
        site_link (str): web site adress.
        data (dict): It includes the target link.
    """
    r = requests.get(site_link)
    soup = BeautifulSoup(r.text,'html.parser')
    main_links = soup.find_all('div',attrs={'class':'fancy-buttons'})  
    hrefs = []
    isExist = False
    for i in range(len(main_links)):
        all_links_in_div = list(map(convert_to_link,main_links[i].find_all('a')))
        # print(all_links_in_div)
        if data["url"] in all_links_in_div:
            isExist = True
            break
        else:
            hrefs += (all_links_in_div)
    return isExist, hrefs


with open("data/last_data.json", 'r') as out:
    last_data = json.load(out)
track_web_site(last_data)