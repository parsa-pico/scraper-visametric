from time import sleep
from undetected_chromedriver import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import log
from captcha_solver import Captcha_Solver
import utils
import json
from sele import Sele
import traceback
import os
import time


def run(driver):
    browser = driver.browser

    driver.get_blank(
        "https://ir-appointment.visametric.com/ir/editappointment")
    driver.wait_for_page_load()
    sleep(1)
    t1 = time.time()
    os.startfile("cf_click_short.mrs.lnk")
    utils.delay(t1, 10)
    browser.switch_to.window(browser.window_handles[1])
    # WebDriverWait(browser, 20).until(EC.frame_to_be_available_and_switch_to_it(
    #     (By.CSS_SELECTOR, "iframe[title='Widget containing a Cloudflare security challenge']")))
    # checkBox = WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
    #     (By.CSS_SELECTOR, "label.ctp-checkbox-label")))

    # checkBox.click()
    sleep(2)
    driver.wait_for_page_load()
    driver.edit_date_page()

    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".newCaptcha")))

    solver = Captcha_Solver(browser)
    solver.solve_captcha(By.ID, "btnEditAppointment")

    while not solver.correct_captcha():
        solver.refresh_captcha()
        sleep(1.5)
        solver.solve_captcha(By.ID, "btnEditAppointment")
        sleep(4)

    sleep(1)

    driver.wait_for_page_load()
    driver.edit_date_access_page()
    while True:
        ...


if __name__ == "__main__":
    file = open("personal_info.json", "r")
    personal_info = json.loads(file.read())

    file.close()
    while True:
        browser = None
        try:
            driver = Sele(info=personal_info)
            driver.open_browser()
            browser = driver.browser
            run(driver)
        except utils.TOO_MUCH_REQ_EXCEPTION as e:
            log(e)
            if browser:
                browser.quit()
            sleep(250)
        except Exception as e:
            print("browser", type(browser))
            log(e)
            log(traceback.format_exc())
            if browser:
                print("closing browser")
                browser.quit()
            sleep(10)
