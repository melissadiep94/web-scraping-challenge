from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import pymongo


def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # get NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title= soup.find_all('div', class_='content_title')[0].text
    par=soup.find_all('div', class_='article_teaser_body')[0].text


    # get JPL Mars Space Images - Featured Image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)   
    browser.links.find_by_partial_text('FULL IMAGE').click()    

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find_all('img', class_='fancybox-image')[0]["src"]
    featured_image_url = url + image

    #get Mars facts table
    url = 'https://galaxyfacts-mars.com/#'
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ['Description', 'Mars']
    df_v2 = df.replace(':','', regex=True)
    df_v2.to_html("mars_facts_table_v2.html", index=False)
    df_v3 = df_v2.to_json(orient='split')
    df_v3_data = [["Equatorial Diameter","6,792 km"],["Polar Diameter","6,752 km"],["Mass","6.39 \\u00d7 10^23 kg (0.11 Earths)"],["Moons","2 ( Phobos & Deimos )"],["Orbit Distance","227,943,824 km (1.38 AU)"],["Orbit Period","687 days (1.9 years)"],["Surface Temperature","-87 to -5 \\u00b0C"],["First Record","2nd millennium BC"],["Recorded By","Egyptian astronomers"]]

    # get hemisphere names and images urls
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    for hem_num in range (4):
        partial_hem = browser.links.find_by_partial_text('Enhanced')
        name_hem = partial_hem[hem_num].text
        partial_hem[hem_num].click()
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        img_loc = soup.find('li')
        img_hem = url + img_loc.a['href']
    
        hem_dic = {"title": name_hem, "img_url": img_hem}
        hemisphere_image_urls.append(hem_dic)  
        browser.back()

    Mars_info = {
        'news_title': title, 
        'news_par':par,
        'featured_image' : featured_image_url,
        'table_facts': df_v3_data,
        'hemispheres_info': hemisphere_image_urls
    }
   
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mndb = myclient["mars_data"]
    mycol = mndb['Mars_info']
    x = mycol.insert_many(Mars_info)
    print(x)
   # Quit the browser
    browser.quit()
    return Mars_info 
