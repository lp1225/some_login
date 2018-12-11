import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bilibili_login import bili_login

username = 'your name'
password = 'your password'
crack = bili_login.Crack(username, password)

crack.run(crack)
browser = crack.browser
bowton = WebDriverWait(browser, timeout=100).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn btn-login')))
time.sleep(5)
bowton.click()
print('login finish')
