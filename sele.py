from time import sleep
from undetected_chromedriver import Chrome, options, By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import js_scripts
from selenium.common.exceptions import NoSuchElementException
import utils
from utils import log

import re
import jdatetime
import time
import threading


class Sele():

    def __init__(self, email_control, browser=None, info={}) -> None:
        self.email_control = email_control
        self.info = info
        self.browser = browser
        self.email_code = None

    def open_browser(self):
        opt = options.ChromeOptions()
        opt.add_argument("--auto-open-devtools-for-tabs")
        opt.add_argument("--disable-popup-blocking")
        opt.add_argument('--ignore-certificate-errors')
        # opt.add_argument('headless')
        self.browser = Chrome(options=opt)
        self.browser.get("https://google.com")

        self.browser.maximize_window()

    def get_blank(self, url):
        string = f"function test(){'{'}console.log('hi') ; window.open('{url}', '_blank');{'}'} test();"
        self.browser.execute_script(string)

    def wait_for_page_load(self):
        WebDriverWait(self.browser, 10).until(lambda d: d.execute_script(
            'return document.readyState') == 'complete')

    def agreement_page(self):
        WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located((By.ID, "result0"))).click()
        sleep(1)
        self.browser.find_element(By.ID, "result1").click()
        sleep(0.5)
        self.browser.find_element(By.ID, "btnSubmit").click()

    def get_n_past_monthes(self):
        m1 = int(self.info["generic_info"]["payed_date"].split(",")[1])
        m2 = int(str(jdatetime.date.today()).split("-")[1])
        diff = abs(m2-m1)

        return diff

    def city_page(self):
        Select(self.browser.find_element(By.ID, "city")).select_by_value("1")
        sleep(1)
        Select(self.browser.find_element(By.ID, "office")).select_by_value("1")
        sleep(0.5)
        Select(self.browser.find_element(
            By.ID, "officetype")).select_by_value("1")
        sleep(0.5)
        total_person = len(self.info["persons_info"])
        Select(self.browser.find_element(
            By.ID, "totalPerson")).select_by_value(str(total_person))

        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located(
            (By.ID, "atm"))).click()

        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located(
            (By.ID, "popupDatepicker2"))).click()
        past_monthes = self.get_n_past_monthes()
        for _ in range(past_monthes):
            sleep(0.2)
            self.browser.find_elements(
                By.CSS_SELECTOR, ".pwt-btn.pwt-btn-prev")[1].click()
        if past_monthes == 0:
            sleep(0.2)
        payed_date = self.info["generic_info"]["payed_date"]
        payed_date = f'td[data-date="{payed_date}"]'

        date_element = self.browser.find_elements(
            By.CSS_SELECTOR, payed_date)

        date_element = filter(
            lambda d: d.is_displayed() and d.is_enabled(), date_element)
        date_element = list(date_element)

        date_element[0].click()

        self.browser.find_element(By.ID, 'paymentCardInput').send_keys(
            self.info["generic_info"]["card_number"])

        self.browser.find_element(By.ID, 'checkCardListBtn').click()

        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "bankpaymentRadio"))).click()

        self.browser.find_element(By.ID, 'btnAppCountNext').click()

    def fill_input(self, key, value, by=By.NAME):
        e = self.browser.find_element(by, key)
        e.clear()
        e.send_keys(value)

    def fill_select(self, id, value):
        Select(self.browser.find_element(
            By.ID, id)).select_by_value(value)

    def fill_form(self, person_index, person_info):
        self.fill_input(f"name{person_index+1}", person_info["first_name"])

        self.fill_input(f"surname{person_index+1}", person_info["last_name"])

        self.fill_input(f"passport{person_index+1}",
                        person_info["passport_number"])

        self.fill_input(f"phone{person_index+1}", person_info["phone_number"])

        if person_info["phone_number_emg"] != "-":
            self.fill_input(f"phone2{person_index+1}",
                            person_info["phone_number_emg"])

        self.fill_input(f"email{person_index+1}", person_info["email"])

        self.fill_select(f"birthyear{person_index+1}",
                         person_info["birth"]["year"])

        self.fill_select(f"birthmonth{person_index+1}",
                         person_info["birth"]["month"])

        self.fill_select(f"birthday{person_index+1}",
                         person_info["birth"]["day"])

    def correct_email_code(self):
        try:
            alert = self.browser.find_element(
                By.CSS_SELECTOR, ".sweet-alert").get_attribute("class")
        except NoSuchElementException as e:
            return True
        if alert.find("showSweetAlert") != -1:
            WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".sa-confirm-button-container .confirm"))).click()
            log("wrong email code")
            return False
        else:
            return True

    def form_page(self, resolve_email=False):
        # self.fill_input("sheba_number", self.info["generic_info"]["sheba"])
        # self.fill_input(
        #     "sheba_name", self.info["generic_info"]["persian_name"])

        # for i, person_info in enumerate(self.info["persons_info"]):
        #     person_info["email"] = self.info["generic_info"]["email"]
        #     self.fill_form(i, person_info)
        self.browser.execute_script(js_scripts.fill_form(self.info))

        next_btn = self.browser.find_element(
            By.ID, "btnAppPersonalNext")
        next_btn.click()
        if resolve_email:
            code_input = WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located(
                (By.ID, "mailConfirmCodeControl")))

            for i in range(3):
                sleep(2.5)
                self.email_control.get_last_msg()
                self.email_code = self.email_control.find_code()
                code_input.clear()
                code_input.send_keys(self.email_code)
                next_btn.click()
                sleep(0.3)
                if self.correct_email_code():
                    break

        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located(
            (By.ID, "previewchk"))).click()

        self.browser.find_element(
            By.ID, "btnAppPreviewNext").click()

    def open_dates(self, dates):
        pattern = r'(\d{2})-(\d{2})-(\d{4})'
        dates = re.findall(pattern, dates)
        dates = list(
            map(lambda x: {"day": x[0], "month": x[1], "year": x[2]}, dates))

        self.browser.execute_script(js_scripts.enable_dates(dates.__str__()))
        # current_month = str(datetime.now().month)
        # self.browser.find_element(
        #     By.CSS_SELECTOR, ".calendarinput").click()
        # next_btn = self.browser.find_element(
        #     By.CSS_SELECTOR, ".datepicker-days th.next")
        # for date in dates:
        #     day, month, year = date
        #     diff = abs(int(month)-int(current_month))
        #     for _ in range(diff):
        #         next_btn.click()
        #         sleep(0.2)
        #     self.browser.execute_script(js_scripts.enable_date(day))
        #     current_month = month

    def date_page(self):
        self.browser.execute_script(js_scripts.stop_timer())
        response_element = self.browser.find_element(
            By.CLASS_NAME, "copyright")

        while True:
            script = js_scripts.get_date(
                self.email_code, self.info["generic_info"]["consular_id"])
            self.browser.execute_script(script)
            sleep(5)
            response = str(response_element.get_attribute("innerHTML"))
            log("get_date_res:", response)

            if response.startswith("error"):
                raise utils.TOO_MUCH_REQ_EXCEPTION(
                    "err when getting date via console")
            elif len(response) != 10:  # means there is time
                try:
                    self.open_dates(response)
                    log("!!!free time!!!")
                    utils.multiNotify(3)
                except Exception as e:
                    log(e)
                    while True:
                        ...

                while True:
                    ...
            sleep(30)
