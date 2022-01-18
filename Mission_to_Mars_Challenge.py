#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


#Setup the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


#Begin scraping
slide_elem.find('div', class_ = 'content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[13]:


#10.3.5


# In[14]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
#df
df.to_html()


# In[15]:


browser.quit()


# In[16]:


#starter code


# In[17]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[18]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# #Visit the NASA Mars News Site

# In[19]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[20]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[21]:


slide_elem.find('div', class_='content_title')


# In[22]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[23]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[24]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[25]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[26]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[27]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[28]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# Mars Facts

# In[29]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[30]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[31]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Hemispheres

# In[32]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[33]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# 3. Write code to retrieve the image urls and titles for each hemisphere.
html=browser.html
hemisphere_soup = soup(html, 'html.parser') 

#getting the links for each hemispheres
hemisphere_links = hemisphere_soup.find_all('h3')
hemisphere_links


# In[52]:


# loop through each hemisphere link
for hemisphere in hemisphere_links:
    # Navigate and click the link of the hemisphere
    img_page = browser.find_by_text(hemisphere.text)
    img_page.click()
    html= browser.html
    img_soup = soup(html, 'html.parser')
    # Scrape the image link
    img_url = 'https://marshemispheres.com/' + str(img_soup.find('img', class_='wide-image')['src'])
    # Scrape the title
    title = img_soup.find('h2', class_='title').text
    # Define and append to the dictionary
    hemi_dict = {'img_url': img_url,'title': title}
    hemisphere_image_urls.append(hemi_dict)
    #browser.back()
    print(hemisphere_image_urls)


# In[55]:


print (img_url)


# In[56]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[57]:


# 5. Quit the browser
browser.quit()

