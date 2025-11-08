# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import numpy as np
# import json
     
# headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'} 

# webpage = requests.get('https://www.ambitionbox.com/list-of-companies?page=2',headers=headers).text



# soup=BeautifulSoup(webpage,'lxml')

# service=soup.find_all('div',class_='companyCardWrapper')

# companies = [
#     {
#         "name": i.find('h2').text.strip(),
#         "rating": i.find('div', class_="rating_text").text.strip(),
#         "reviews": i.find("span", class_="companyCardWrapper__ActionCount").text.strip()
#     }
#     for i in service
# ]

# companies_json = json.dumps(companies, indent=4)

# with open("companies.json", "w", encoding="utf-8") as f:
#     json.dump(companies, f, indent=4, ensure_ascii=False)

import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
}

all_companies = []


# Set the range of pages you want to scrape
for page in range(1, 5):  # Example: pages 1 to 5
    url = f'https://www.ambitionbox.com/list-of-companies?page={page}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    service = soup.find_all('div', class_='companyCardWrapper')
    
    for i in service:
         img_tag = i.find('div', class_='companyCardWrapper__companyLogo').find('img') if i.find('div', class_='companyCardWrapper__companyLogo') else None
         all_companies.append({
            "name": i.find('h2').text.strip() if i.find('h2') else None,
            "rating": i.find('div', class_="rating_text").text.strip() if i.find('div', class_="rating_text") else None,
            "reviews": i.find("span", class_="companyCardWrapper__ActionCount").text.strip() if i.find("span", class_="companyCardWrapper__ActionCount") else None,
            "logo_url": img_tag['src'] if img_tag else None
        })
    

# Save all pages to JSON
with open("companies.json", "w", encoding="utf-8") as f:
    json.dump(all_companies, f, indent=4, ensure_ascii=False)

print(f"Saved {len(all_companies)} companies from {page} pages")