from time import sleep
from imutils import paths
from undetected_chromedriver import Chrome, options, By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import os
import utils
from captcha_solver import Captcha_Solver
from sele import Sele
# opt = options.ChromeOptions()
# opt.add_argument("--auto-open-devtools-for-tabs")
# browser = Chrome(options=opt)
# browser.get("https://ir-appointment.visametric.com/ir/recaptchaAscii")
# sleep(5)
import cv2
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--ignore-certificate-errors')

driver = uc.Chrome(options=chrome_options)
url = 'https://ir-appointment.visametric.com/ir/recaptchaAscii'
driver.get("https://google.com")
time.sleep(2)
string = f"function test(){'{'}console.log('hi') ; window.open('{url}', '_blank');{'}'} test();"
driver.execute_script(string)
time.sleep(3)
t1 = time.time()
os.startfile("cf_click_short.mrs.lnk")
utils.delay(t1, 10)

driver.switch_to.window(driver.window_handles[1])
# WebDriverWait(browser, 20).until(EC.frame_to_be_available_and_switch_to_it(
#     (By.CSS_SELECTOR, "iframe[title='Widget containing a Cloudflare security challenge']")))
# checkBox = WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
#     (By.CSS_SELECTOR, "label.ctp-checkbox-label")))

# # print("before click")
# checkBox.click()
# sleep(3)

n_previous_images = len(list(paths.list_images("./captcha_images")))
print(n_previous_images)
cs = Captcha_Solver(None)
sele = Sele(browser=driver)
for i in range(40):
    n = i+n_previous_images
    captchaHtml = driver.find_element(By.CSS_SELECTOR, "body").get_attribute(
        "innerHTML")
    with (open(f"./captcha_html/captcha-{n}.html", "w")) as file:
        file.write(captchaHtml)

        tuned_captcha = cs.tune_captcha(captchaHtml, 6)
        cv2.imwrite(f"./captcha_images/captcha-{n}.png", tuned_captcha)
    driver.refresh()
    sleep(0.5)
    sele.wait_for_page_load()
    sleep(5)


# driver.switch_to.window(driver.window_handles[1])
# WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
#     (By.CSS_SELECTOR, "iframe[title='Widget containing a Cloudflare security challenge']")))
# checkBox = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
#     (By.CSS_SELECTOR, "label.ctp-checkbox-label")))

# checkBox.click()
while True:
    ...
