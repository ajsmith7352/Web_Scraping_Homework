#!/usr/bin/env python
# coding: utf-8

# #Imports

# In[1]:


#import dependencies (some of these may be superfluous)
import pandas as pd
import time
from splinter import Browser
import pymongo
import pandas as pd
import time
import shutil
import requests
from selenium import webdriver

import re
import numpy as np
from bs4 import BeautifulSoup as bs



def init_browser():
    executable_path = {"executable_path": os.path.abspath("chromedriver.exe")} 
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    # #Nasa Mars News Site



    # In[3]:


    #visiting the page
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    # In[4]:


    html = browser.html
    soup = bs(html, "html.parser")


    # In[5]:


    print(soup.prettify())


    # In[6]:


    #trying two different ways to pull the text from the title and the teaser
    title = soup.find(class_="content_title").get_text(strip=True)
    teaser = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {title}")
    print(f"Teaser: {teaser}")


    # #JPL Mars Space Images

    # In[7]:


    # Using splinter to navigate jpl.nasa.gov to find the featured image
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)


    # In[8]:


    html = browser.html
    img_soup = bs(html, "html.parser")


    # In[9]:


    image_xpath = '//*[@id="page"]/section[3]/div/ul/li[28]/a/div/div[2]/img'
    results = browser.find_by_xpath(image_xpath)
    img = results[0]
    img.click()


    # In[11]:


    #Retrieve image url
    img_html = browser.html
    soup = bs(img_html, "lxml")
    img_url = soup.find("img", class_= "fancybox-image")
    img_url_pt2 = img_url.get("src")
    featured_image_url = "https://www.jpl.nasa.gov" + img_url_pt2
    print(featured_image_url)


    # #Mars Weather (Twitter)

    # In[12]:


    # retrieve mars weather's most recent tweet from the website
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)


    # In[13]:


    # using BeautifulSoup to write it into html
    weather_html = browser.html
    soup = bs(weather_html, "lxml")
    weather_tweet = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(weather_tweet)


    # #Mars Facts

    # In[24]:


    #visit the Mars Facts webpage
    #Mars Facts....visit webpage, use pandas to scrape the page for facts
    request_mars_facts = requests.get("https://space-facts.com/mars/")


    # In[34]:


    facts_table = pd.read_html(request_mars_facts.text)
    facts_table


    # In[35]:


    facts_df = facts_table[0]
    facts_df.set_index(0, inplace=True)
    facts_df


    # In[36]:


    facts_html = facts_df.to_html()
    facts_html


    # In[38]:


    facts_html.replace('\n', '')


    # In[39]:


    facts_df.to_html('mars_table.html')


    # #Mars Hemispheres

    # In[68]:


    # go to the Astrogeology website to retrieve high res images for each hemisphere
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    usgs_html = browser.html
    soup = bs(usgs_html, "html.parser")
    mars_hemi = []


    # In[69]:


    results = soup.find("div", class_="collapsible results" )
    hemis = results.find_all("div", class_="item")


    # In[70]:


    # Create a loop that goes through each hemisphere
    for hemi in hemis:
        title = hemi.find("h3").text
        img_link = hemi.find("a")["href"]
        usgs_img_link = "https://astrogeology.usgs.gov" + img_link    
        browser.visit(usgs_img_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        usgs_img_url = downloads.find("a")["href"]
        mars_hemi.append({"title": title, "img_url": usgs_img_url})

    mars_dict = {
        "mars_title": title,
        "mars_p": teaser,
        "feat_img_url": featured_image_url,
        "mars_weather": weather_tweet,
        "facts_table": facts_df,
        "hemi_images": mars_hemi
    }
    return mars_dict

if __name__  ==  "__main__":
    print(scrape())