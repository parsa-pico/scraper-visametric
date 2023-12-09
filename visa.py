from start_end import time_passed
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
import os
import time
from email_utils import Email_Logger
from imaplib import IMAP4
from sys import argv
from args_parse import args_parse


def select_btn(number):
    if number == 2:
        return "schengenBtn"
    elif number == 3:
        return "legalizationBtn"
    else:
        raise Exception("not valid number")


def run(driver, info, parsed_args):
    browser = driver.browser

    driver.get_blank("https://ir-appointment.visametric.com/ir")
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

    WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".newCaptcha pre")))

    sleep(1)
    btn = select_btn(info["generic_info"]["consular_id"])
    print('a')
    auto_solver = True if parsed_args.get("manual") == None else False
    print("auto", auto_solver)
    if auto_solver:
        solver = Captcha_Solver(browser)
        solver.solve_captcha(btn=btn)
        print('here')
        while not solver.correct_captcha():
            solver.refresh_captcha()
            sleep(5)
            solver.solve_captcha(btn=btn)
            sleep(1)
        sleep(1)
    else:
        input("waiting for solving captcha")
        sleep(1.5)
    # driver.wait_for_page_load()
    log("before agreement_page")
    driver.agreement_page()
    log("before city_page")
    driver.city_page()
    sleep(1)
    driver.wait_for_page_load()
    driver.form_page()
    sleep(1)
    driver.wait_for_page_load()
    driver.date_page()
    while True:
        ...


if __name__ == "__main__":

    file = open("personal_info_2.json", "r", encoding="utf-8")
    personal_info = json.loads(file.read())
    file.close()
    parsed_args = args_parse(argv)
    email_logger = None
    start_time = parsed_args.get("s")
    s_time_delta = int(parsed_args.get("s_delta") or 0)
    end_time = parsed_args.get("e")
    e_time_delta = int(parsed_args.get("e_delta") or 0)
    log("start time: ", start_time, " end time: ",
        end_time, " start delta: ", s_time_delta, " end delta: ", e_time_delta)

    while True:
        browser = None
        try:
            if start_time and not time_passed(start_time, s_time_delta):
                log("task not started yet...")
                sleep(60)
                continue
            if end_time and time_passed(end_time, e_time_delta):
                log("program finsihed, shutting down the system...")
                os.system("shutdown /s /t 1")
                exit(0)
            if not email_logger:
                email_logger = Email_Logger(personal_info)
                email_logger.login()

            driver = Sele(email_control=email_logger, info=personal_info)
            driver.open_browser()
            browser = driver.browser
            run(driver, personal_info, parsed_args)
        except KeyboardInterrupt as e:
            input("press enter to close program")
            utils.handle_exception("Keyboard Interrupt", "", browser, 1, False)
            exit(0)

        except (IMAP4.error, IMAP4.abort, IMAP4.readonly) as e:
            email_logger = None

            utils.handle_exception("email problem:", e, browser, 30)

        except utils.TOO_MUCH_REQ_EXCEPTION as e:
            utils.handle_exception("", e, browser, 301, False)

        except Exception as e:
            utils.handle_exception("", e, browser, 30)
