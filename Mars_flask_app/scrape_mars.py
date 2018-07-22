
# coding: utf-8

# In[13]:


import requests, time
from bs4 import BeautifulSoup as BS
# from splinter import Browser
import pandas as pd


# ## Step 1 - Scraping

# ### NASA Mars News

# In[2]:


# latest_news_raw = requests.get('https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')
# soup = BS(latest_news_raw.text,'html.parser')



# In[3]:
mars_data = dict()


def scrape(browser):
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(mars_news_url)


    # In[4]:


    html = browser.html
    soup = BS(html, 'html.parser')
    time.sleep(10)
    # extract the news items from the html
    news_items = soup.find('ul', class_='item_list')
    latest_news = news_items.find_all('li', class_='slide')[0]
    # retrieve the tile and paragraph
    news_title = latest_news.find('div', class_='content_title').text
    news_p = latest_news.find('div', class_='article_teaser_body').text



    # ### JPL Mars Space Images

    # In[7]:


    mars_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_images_url)

    # In[9]:


    # click on the 'full image' button to inspect the image
    browser.find_by_xpath('//*[@id="full_image"]').click()


    # In[10]:


    # click on 'more info' button to get the full-size version of the image
    # browser.find_by_xpath('//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]').click()

    visible = False
    while not visible:
        # wait until the element is visible
        visible = browser.is_element_present_by_xpath("//div[@class='buttons']/a[@class='button']")
        time.sleep(1)
    browser.find_by_xpath("//div[@class='buttons']/a[@class='button']").click()

    # In[11]:

    # get the url of the large version of the image
    img_html = browser.html
    soup = BS(img_html, 'html.parser')
    img_url = soup.find('img', class_='main_image')['src']
    featured_image_url = 'https://www.jpl.nasa.gov/' + img_url


    # ### Mars Weather

    # In[129]:


    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)


    # In[130]:


    mars_weather_html = browser.html
    soup = BS(mars_weather_html, 'html.parser')


    # In[131]:


    tweets =soup.find('div', class_='stream').find_all('li')


    # In[153]:


    mars_weather = None

    for tweet in tweets:
        tweet_account = tweet.find('span',class_='FullNameGroup')
        if tweet_account:
            tweet_account_text= tweet_account.text.lstrip()
            if 'mars weather' in tweet_account_text.lower():
                # the latest weather report on Mars
                mars_weather = tweet.find('div', class_='js-tweet-text-container').find('p').text
                break


    # ### Mars Facts

    # In[53]:


    # use pandas to scrape the html page
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_table = pd.read_html(mars_facts_url)


    # In[58]:


    df = mars_facts_table[0]
    # add columns to the dataframe
    df.columns = ['description','value']
    # set the alignment to left
    df.style.set_properties(**{'text-align':'left'})
    # set the index to the `description` column
    # df.set_index('description', inplace=True)


    # In[59]:


    # convert to HTML string
    mars_facts_table_string = df.to_html(index=False)

    # ### Mars Hemispheres

    # In[99]:


    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)


    # In[100]:


    # extract the elements with BS
    mars_hemispheres_html = browser.html
    soup = BS(mars_hemispheres_html, 'html.parser')


    # In[104]:


    hemisphere_image_urls =list()
    hemisphere_image_items = soup.find_all('div',class_='item')


    # In[106]:


    for item in hemisphere_image_items:

        # extract the title of the image
        title = item.find('h3').text
        # go to the link to get the details
        browser.find_by_text(title).click()
        # extract the url of the image
        img_html = browser.html
        soup = BS(img_html, 'html.parser')
        img_url = soup.find('div', class_='downloads').find_all('li')[0].find('a')['href']
        # add the `title` and `img_url` to the list
        hemisphere_image_urls.append({'title':title, 'img_url':img_url})
        # return to the previous webpage
        browser.visit(mars_hemispheres_url)


    # In[107]:

    mars_data = {
        'news_title':news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': mars_facts_table_string,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return mars_data


# d = scrape()
# print(d)