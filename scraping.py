
from bs4 import BeautifulSoup as soup
from splinter import Browser
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path':'chromedriver'}
    browser = Browser('chrome',**executable_path,headless=True)
    news_title, news_paragraph = mars_news(browser)
    data = {
        'news_title':news_title,
        'news_paragraph':news_paragraph,
        'featured_image':featured_image(browser),
        'mars_facts': mars_data(browser),
        'hamisphere': hamisphere(browser), 
        'last_modified':dt.datetime.now()
    }
    browser.quit()
    return data





### summary and title
def mars_news(browser):
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css('ul.item_list li.slide')

    html = browser.html
    html_soup = soup(html,'html.parser')
    try:
        title = html_soup.select_one('ul.item_list li.slide').select_one('div.content_title').text

        summary = html_soup.select_one('ul.item_list li.slide').select_one('div.article_teaser_body').text
    except AttributeError:
        return None,None
    return title,summary


# ### Featured Images
def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    try:
        browser.links.find_by_partial_text('FULL IMAGE').click()
        browser.links.find_by_partial_text('more info').click()
        soup_img = soup(browser.html,'html.parser')
        img = soup_img.find('img',class_='main_image').get('src')
        img_url = f'https://www.jpl.nasa.gov/{img}'
    except AttributeError:
        return None
    return img_url
## data table

def mars_data(browser):
    
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    return df.to_html().replace('border=\"1\" class=\"dataframe\"', "class=table table-condensed")

def hamisphere(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    img_title_list = []
    links = [f"https://astrogeology.usgs.gov/{i.get('href')}" for i in soup(browser.html,'html.parser').find_all('a',class_='itemLink product-item')]
    try:
        for i in set(links):
            img_title={}
            browser.visit(i)
            img_url2 = soup(browser.html,'html.parser').find('div',class_='downloads').find('a').get('href')
            title = soup(browser.html,'html.parser').find('h2',class_='title').text
            img_title['url'] = img_url2
            img_title['title'] = title
            img_title_list.append(img_title)
    except AttributeError:
        return None
    return img_title_list

if __name__ == "__main__":
    print(scrape_all())


