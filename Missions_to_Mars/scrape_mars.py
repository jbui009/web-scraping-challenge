# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt

# Set Executable Path & Initialize Chrome Browser
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser('chrome', **executable_path, headless=False)

#create dictionary to save for MongoDB
mars_entries = {}

# NASA Mars News Site Web Scraper
def mars_news(browser):
    try:
        browser = init_browser()
        # Visit the NASA Mars News Site
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text
    
    #save entries for mongoDB
        mars_entries['news_title'] = news_title
        mars_entries['news_paragraph'] = news_p

        return mars_entries
    finally:
        browser.quit()

def featured_image(browser):

    try:
        browser = init_browser()
        #splinter to get image
        featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
        browser.visit(featured_image_url)

        html_image = browser.html

        soup = BeautifulSoup(html_image, 'html.parser')
        
        #find image url
        featured_image_url_located = soup.find('img', class_="thumbimg").get('src')


        # Website Url
        main_url = 'https://www.jpl.nasa.gov'

        # Display full link to featured image
        featured_image_url

        #show complete url 
        featured_image_url = main_url + featured_image_url_located
        featured_image_url

        #save url entry
        mars_entries['featured_image_url_located'] = featured_image_url

        return mars_entries
    finally:
        browser.quit()


def mars_facts():
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's with url to get dataframe of info from url
    mars_facts = pd.read_html(facts_url)

    # Create mars dataframe
    mars_df = mars_facts[0]

    # Assign the columns
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)

    # Save html code
    data = mars_df.to_html()

    # save mars facts for recall later
    mars_entries['mars_facts'] = data

    return mars_entries


def mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemisphere_image_urls = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemispheres_url.append({"title" : title, "img_url" : img_url})

        mars_entries['hiu'] = hemispheres_url

        
        # Return mars_data dictionary 

        return mars_entries
    finally:

        browser.quit()
