# --------------------
# Mission to Mars
# Scrape Mars
# --------------------

# import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time as time
import re

# go to the directory
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# scrapey scrape function TIME BOYS LETS GO
def scrape():

    # """ NASA Mars News """
    # browse the web page
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(1)
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'html.parser')
    # print the news titles
    news_title = nasa_soup.find("li", class_="slide").find("div", class_="content_title").text
    news_p = nasa_soup.find("li", class_="slide").find("div", class_="article_teaser_body").text
    # exit Browser.
    browser.quit()

    print(news_title)
    print(news_p)

    # """ JPL Mars Space Images """
    # visit the jpl image source
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    # jpl html
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')
    # find the featured image and print
    featured_img_base = "https://www.jpl.nasa.gov"
    featured_img_url_raw = jpl_soup.find("div", class_="carousel_items").find("article")["style"]
    featured_img_url = featured_img_url_raw.split("'")[1]
    featured_img_url = featured_img_base + featured_img_url
    # exit Browser.
    browser.quit()

    print(featured_img_url)

    # """ Mars Weather """
    # find the weather and print it
    # visit the twitter source
    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_twitter_url)
    # wait a bit cause idk why it just doesnt work thanks america
    time.sleep(5)
    # convert html to bs
    twitter = browser.html
    soup = bs(twitter,"lxml")
    # use this if you need to print to console (gross!)
    # print(weather_soup.prettify())
    mars_insight = soup.find(text=re.compile('InSight sol'))
    mars_weather = mars_insight.replace('InSight sol', 'Sol', 1)

    # exit Browser.
    browser.quit()
    print(mars_weather) 

    # """ Mars Facts """
    # facts url
    facts_url = "https://space-facts.com/mars/"
    #   make into a table
    tables = pd.read_html(facts_url)
    mars_df = tables[0]
    # assign column values and set index
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    # convert to html string
    mars_df.to_html()
    data = mars_df.to_dict(orient='records') 
    # print results
    mars_df

    # """ Mars hemispheres """
    # hemispheres website
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    # HTML Object and parse said object
    html_hemispheres = browser.html
    hemisphere_soup = bs(html_hemispheres, 'html.parser')
    # retrieve all items for it
    items = hemisphere_soup.find_all('div', class_='item')
    # make an empty list for image urls
    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    # exit Browser.
    browser.quit()
    # loopity loop through the items previously stored
    for i in items: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)
        partial_img_html = browser.html
     
        soup = bs( partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        # exit Browser.
        browser.quit()

    # print result
    print(hemisphere_image_urls)

    # close browser once data is pulled
    # browser.quit()
    results = {
        'news_title' : news_title,
        'news_p': news_p,
        'featured_image_url': featured_img_url,
        'mars_weather' : mars_weather,
        'hemisphere_image_urls': hemisphere_image_urls
    }   
    return(results)


