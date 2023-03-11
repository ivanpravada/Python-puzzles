from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from attributes import url

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get(url=url)
    search_field = driver.find_element(by=By.NAME, value="search")
    search_field.send_keys("Iphone")
    search_field.send_keys(Keys.ENTER)
    time.sleep(5)

    add_to_cart_button = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div/div/div[2]/div[2]/button[1]')
    add_to_cart_button.click()
    time.sleep(5)

    shopping_cart_button = driver.find_element(by=By.LINK_TEXT, value='Shopping Cart')
    shopping_cart_button.click()
    time.sleep(5)

    assert "product 11" in driver.page_source

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()