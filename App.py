import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

URL = "https://www.amazon.in/gp/bestsellers/hpc/1374508031"
domain = "https://www.amazon.in/"
prod_details = {}
prod_list=[]
def getallPageLinks(soup):
    """
    Input: soup for the website after succesful retrieval
    output: list of all product links

    """


    titles = soup.find_all("div", class_="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
    prices = soup.find_all("span",class_="p13n-sc-price")
    ratings = soup.find_all("span",{"class":"a-icon-alt"})
    for title, price,rating in zip(titles, prices,ratings):
        prod_list.append({"title": title.text,
                         "ratings": rating.text,
                         "price": price.text})

    return prod_list

def access_url():
    max_retries=3
    retry_delay=2
    retries=0
    while retries<max_retries:
       page = requests.get(URL)
       if page.status_code == 200:
          return page
       else:
           time.sleep(retry_delay)
           retries+=1

    return None



def main():
    
    try:
       page=access_url()
       soup = BeautifulSoup(page.content, "html.parser")
       print("Test 1: Passed | Page fetched successfully")
       Product_details = getallPageLinks(soup)
       df=pd.DataFrame(Product_details)
       df.to_csv('Product_details.csv',index=False)


    except:
        print(f"Test Failed | the requested url throws error! with error code {page.status_code}")


main()
