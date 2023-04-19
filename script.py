import os
import requests
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from random import randrange

# set download directory
download_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'images')

# create download directory if it doesn't exist
if not os.path.exists("download_dir"):
    os.makedirs("download_dir")

# create a Chrome driver instance with options to download files automatically
firefox_options = FirefoxOptions()
firefox_options.set_preference("browser.download.folderList", 2)
firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
firefox_options.set_preference("browser.download.dir", download_dir)
firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
firefox_options.set_preference("browser.safebrowsing.enabled", True)

service = FirefoxService(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

# navigate to the website with the headless browser
url = input("Please enter Website: ")


def migros(url):
    
    driver.get(url)

    # wait for the page to load completely
    time.sleep(3)
    
    height = driver.execute_script("return document.body.scrollHeight")
    page_range = range(0, height, round(height/10))
    for i in range(0, len(page_range)-1):
        driver.execute_script(f"window.scrollTo({page_range[i]}, {page_range[i+1]});")
    time.sleep(5)

    print(f"Downloading from: Migros")
    # get the page source with requests
    image_elements = driver.find_element(By.CSS_SELECTOR, "div[class*='ng-star-inserted'")
    products = image_elements.find_elements(By.TAG_NAME, "li")

    # download the images to the download directory
    for product in products:
        imgs = product.find_elements(By.TAG_NAME, "img")
        for i, img in enumerate(imgs):
            urls_block = str(img.get_attribute("srcset"))
            urls = re.findall(r'https.*?jpg', urls_block)
            if urls:
                url = urls[-1]
                name = re.findall(r"/([^/]+)\.jpg$", url)[0]
                response = requests.get(url)
                with open(f"download_dir/{name}.jpg", "wb") as f:
                    f.write(response.content)

def coop(url):
    driver.get(url)
    time.sleep(3)
    # wait for the page to load completely
    height = driver.execute_script("return document.body.scrollHeight")
    page_range = range(0, height, round(height/10))
    for i in range(0, len(page_range)-1):
        driver.execute_script(f"window.scrollTo({page_range[i]}, {page_range[i+1]});")
    time.sleep(5)

    print(f"Downloading from: Coop")
    # get the page source with requests
    image_elements = driver.find_element(By.CSS_SELECTOR, "div[class*='list-page back-to-top-offset'")
    products = image_elements.find_elements(By.TAG_NAME, "li")

    # download the images to the download directory
    for product in products:
        imgs = product.find_elements(By.TAG_NAME, "img")
        for i, img in enumerate(imgs):
            urls_block = str(img.get_attribute("srcset"))
            urls = re.findall(r'\/\/.*?\.jpg', urls_block)
            if urls:
                url = "https:" + urls[-1]
                print(url)
                name = re.findall(r"/([^/]+)\.jpg$", url)[0]
                response = requests.get(url)
                with open(f"download_dir/{name}.jpg", "wb") as f:
                    f.write(response.content)


def check_supermarket(url):
    if "coop" in url:
        coop(url)
        driver.quit()
    else:
        migros(url)
        driver.quit()

check_supermarket(url)