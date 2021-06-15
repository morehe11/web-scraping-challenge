from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = True)

def scrape_news(browser):
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    NASA_news_soup = soup(html, "html.parser")
    try:
       slide_elem = NASA_news_soup.select_one('div.list_text')
       news_title = slide_elem.find("div", class_ = "conent_title").get_text()
       news_para = slide_elem.find("div", class_ = "article_teaser_body").get_text()
    except AttributeError:
           return None, None
    return news_title,news_para


def featured_image(browser):
  
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    featured_image_elem = browser.find_by_tag('button')[1]
    featured_image_elem.click()     

    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
      
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():
    
    try:
        
        mars_facts_df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

   
    mars_facts_df.columns = ['Description', 'Mars', 'Earth']
    mars_facts_df.set_index('Description', inplace=True)

    
    return mars_facts_df.to_html(classes="table table-striped")


def hemispheres(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url + 'index.html')

    
    hemi_urls = []
    links = browser.find_by_css('a.product-item img')
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css('aproduct-item img')[i].click()
        samp_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = samp_elem['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemi_urls.append(hemisphere)
        browser.back()

    return hemi_urls


def scrape_hemisphere(html_text):
    
    hemi_soup = soup(html_text, "html.parser")

    try:
        title = hemi_soup.find("h2", class_="title").get_text()
        samp_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        
        title = None
        samp_elem = None

    hemispheres = {
        "title": title,
        "img_url": samp_elem
    }

    return hemispheres

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = True)

    news_title, news_para = scrape_news(browser)

    data = {
       "news_title": news_title,
        "news_paragraph": news_para,
        "featured_image": featured_image(browser),
        "news_facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "timestamps": dt.datetime.now()
   }

    browser.quit()
    return data

if __name__ == "__main__":
    print(scrape_all())

    
      
             
