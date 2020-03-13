#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser("chrome", executable_path, headless=True)
def scrape(): 

   


    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


    response = requests.get(url)


    soup = bs(response.text, 'lxml')
    # soup = bs(html, 'html.parser')
    type(soup)


    print(soup.prettify())


    results = soup.find("div", class_="slide")
    print(results)


    # for result in results: 
    news_title = results.find("div", class_="content_title").text
    print(news_title)
    news_p = results.find("div", class_="rollover_description_inner").text
    #     news_p = result.find('div', class_="article_body_teaser")
    print(news_p)
    #     print('\n-----------------\n')


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    html = browser.html
    soup = bs(html,'html.parser')


    browser.click_link_by_partial_text('FULL IMAGE')


    browser.click_link_by_partial_text('more info')


    browser.find_by_css('.main_image').click()


    featured_image_url = browser.url
    print(featured_image_url)


    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)


    soup = bs(response.text, "lxml")
    soup


    mars_weather = ''
    tweets = soup.find_all('p', class_="js-tweet-text")
    for tweet in tweets:
        if "InSight " in tweet.text:
            mars_weather = tweet.text.split("pic.twitter")[
                0].split("InSight ")[-1]
            break
    mars_weather


    url = "https://space-facts.com/mars/"


    table = pd.read_html(url)
    df = pd.DataFrame(data=table[0])
    df = df.rename(columns={0:'description',1:'values'})
    df.set_index('description', inplace = True)
    df


    html_table = df.to_html()
    html_table.replace('\n', '')


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    hemispheres = []
    for image in range(4):
        link = browser.find_link_by_partial_text('Hemisphere Enhanced')[image]
        link.click()
        title = browser.find_by_css('.title').first.text
        url = browser.find_by_text('Sample').first["href"]

        current_image = {
            "title": title,
            "img_url": url
        }
        hemispheres.append(current_image)
        browser.back()


    print(hemispheres)


    return({
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table": html_table,
        "hemisphere_image_urls": hemispheres
    })

