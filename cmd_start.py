from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
string = "start chrome --start-maximized  --remote-debugging-port=9222 --user-data-dir=C:\chromeData --new-window http://ir-appointment.visametric.com/ir"
os.system(string)
time.sleep(3)
os.startfile("cf_click_short.mrs.lnk")
time.sleep(5)
opts = webdriver.ChromeOptions()
opts.add_experimental_option("debuggerAddress", "127.0.0.1:9222 ")
driver = Chrome(options=opts)
time.sleep(10)
input_captcha = driver.find_element(By.NAME, "inputCaptcha")
input_captcha.clear()
input_captcha.send_keys("!")
print("here")

while True:
    ...
