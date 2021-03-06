# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #Set-up Splinter - Initial headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_data": hemisphere_scrape(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    #url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Setup the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    

     # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')    
    #slide_elem.find('div', class_ = 'content_title')

    # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
    # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

def featured_image(browser):
# Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    #url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # # Find the more info button and click that
    # browser.is_element_present_by_text('more info', wait_time=1)
    # more_info_elem = browser.links.find_by_partial_text('more info')
    # more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:  
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

#10.3.5 Mars facts

def mars_facts():
    # Add try/except for error handling
    try:
         # Use 'read_html' to scrape the facts table into a dataframe
         df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe    
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

#deliverable2- Below the def mars_facts() function in the scraping.pyfile, create a function that will scrape the hemisphere data by using your code from the Mission_to_Mars_Challenge.py file. At the end of the function, return the scraped data as a list of dictionaries with the URL string and title of each hemisphere image.
# # D1: Scrape High-Resolution Mars??? Hemisphere Images and Titles

# Hemispheres

def hemisphere_scrape(browser) :

   # ----------------
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html=browser.html
    hemisphere_soup = soup(html, 'html.parser') 

    #getting the links for each hemispheres
    hemisphere_links = hemisphere_soup.find_all('h3')
    #hemisphere_links

    # looping through each hemisphere link
    for i in range(4):     
        # Navigate and click the link of the hemisphere
        browser.find_by_css("a.product-item img")[i].click()
        html= browser.html
        img_soup = soup(html, 'html.parser')
        try:
            # Scrape the image link
            img_url = 'https://marshemispheres.com/' + str(img_soup.find('img', class_='wide-image')['src'])
            # Scrape the title
            title = img_soup.find('h2', class_='title').text
        except AttributeError:
            img_url = None
            title = None
        
        # Define and append to the dictionary
        hemi_dict = {'img_url': img_url,'title': title}
        #hemisphere_links.append(hemi_dict)
        hemisphere_image_urls.append(hemi_dict)
        browser.back()

        # 4. Print the list that holds the dictionary of each image url and title.
    #return hemisphere_links    
    return hemisphere_image_urls


# 5. Quit the browser
#browser.quit()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())



