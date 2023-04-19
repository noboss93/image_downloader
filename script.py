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
print(f"Downloading from: {url}")

driver.get(url)

# wait for the page to load completely
time.sleep(3)

# get the page source with requests
image_elements = driver.find_element(By.CSS_SELECTOR, "div[class*='ng-star-inserted'")
products = image_elements.find_elements(By.TAG_NAME, "li")

# download the images to the download directory
for product in products:
    imgs = product.find_elements(By.TAG_NAME, "img")
    for i, img in enumerate(imgs):
        urls = str(img.get_attribute("srcset"))
        url = re.findall(r'https.*?jpg', urls)
        print(url)
        #response = requests.get(urls)
        #number = randrange(1337)
        #with open(f"download_dir/image_{number}.jpg", "wb") as f:
        #    f.write(response.content)


# close the browser
driver.quit()
