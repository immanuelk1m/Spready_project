from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # browser를 띄우지 않고 실행하기
options.add_argument('--no-sandbox')  # sandbox 기능을 비활성화 하기
options.add_argument('--disable-dev-shm-usage')  # dev/shm/ 폴더를 사용하지 않기
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome('./chromedriver', options=options)