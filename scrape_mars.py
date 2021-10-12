# Dependencies
#########################################################################################################
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
import pandas as pd

executable_path = {"executable_path": '/Users/Serj/Documents/Chromedriver/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# Scrape all
#########################################################################################################
def scrape_all():
    title, paragraph =  mars_news_scraper(browser) 
    img_url_title =  hemisphere_scraper(browser)

    data = {
        'news_title' : title,
        'news_paragraph' : paragraph,
        'featured_image' :featured_image(browser),
        'facts' : mars_facts(),
        'hemispheres' : img_url_title
        }

    browser.quit()
    return data 
    
   

#This Section will scrape the mars news website and collect the latest news title and paragraph text. 
#########################################################################################################
def mars_news_scraper(browser):
    #Establish a connection for the nasa website
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)

    #This will parse the results with BF
    html_news = browser.html
    soup_news = bs(html_news,'lxml')

    try:
        slide_news = soup_news.select_one("ul.item_list li.slide")
        slide_news.find("div", class_="content_title")
        title = slide_news.find("div", class_="content_title").get_text()
        paragraph = slide_news.find("div",class_ = "article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return title,paragraph

#browser.quit()

#This Section will scrape Mars JPL space featured image.
#########################################################################################################

def featured_image(browser):
    #Establish a connection for the JPL website
    url_image = 'https://spaceimages-mars.com/'
    browser.visit(url_image)

    #This will parse the results with BF
    html_image = browser.html
    soup_image = bs(html_image,'lxml')

    #Click the featured image "Full Image" button
    browser.links.find_by_partial_text('FULL IMAGE').click()

    #Parse with BS
    html_image = browser.html
    soup_image = bs(html_image,'lxml')

    try:
        #Get the extension link
        relative_img_url = soup_image.find_all('img')[1]['src']
    except AttributeError:
        return None

    #combine image url with extension url for the full image path
    full_image_path = url_image + relative_img_url
    return full_image_path

#browser.quit()

#This section will scrape mars facts using Pandas
#########################################################################################################

def mars_facts():
    try:
        mars_facts_df = pd.read_html("https://galaxyfacts-mars.com/")[1]
    except BaseException:
        return None
    mars_facts_df.columns=["Data Type", "Value"]
    mars_facts_df.set_index("Data Type", inplace=True)

    return mars_facts_df.to_html(classes="table table-striped")



#This section will scrape the astrology website to obtain high-rez images of each of Mars' hemispheres. 
#########################################################################################################
def hemisphere_scraper(browser): 
    
    #Establish a connection for the JPL website
    url_image = 'https://marshemispheres.com/'
    browser.visit(url_image)
    
    #Parse with BS
    html_images = browser.html
    soup_images = bs(html_images,'lxml')

    #Empty list
    hem_list = []

    #Loop to parse the page
    for i in range(4):
       
        #Empty dictionary
        hem_dict = {}

        #Click on url   
        browser.find_by_css('a.product-item h3')[i].click()

        #Find the full image link
        element = browser.find_link_by_text('Sample').first
        img_url = element['href']
       
       #Find the title
        title = browser.find_by_css("h2.title").text

        hem_dict["Title"] = title
        hem_dict["Img_Url"] = img_url

        #Append the dictionary
        hem_list.append(hem_dict)

        browser.back()
    
    return hem_list
    
#browser.quit()  
    
if __name__ == "__main__":
    print(scrape_all())    
    
    
    

    

    