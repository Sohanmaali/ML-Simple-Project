import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import json
     
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'} 

webpage = requests.get('https://www.zoomcar.com/in/bhopal',headers=headers).text

soup=BeautifulSoup(webpage,'lxml')

service=soup.find_all('div',class_='companyCardWrapper')

companies = [
    {
        "name": i.find('h2').text.strip(),
        "rating": i.find('div', class_="rating_text").text.strip(),
        "reviews": i.find("span", class_="companyCardWrapper__ActionCount").text.strip()
    }
    for i in service
]