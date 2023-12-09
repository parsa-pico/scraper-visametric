# def edit_date_page(self):
#     WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located(
#         (By.ID, "passport"))).send_keys(self.info["passport_number"])
#     # self.browser.find_element(By.ID, "passport").send_keys(
#     #     self.info["passport_number"])
#     self.fill_select("birthday", self.info["birth"]["day"])
#     self.fill_select("birthmonth", self.info["birth"]["month"])
#     self.fill_select("birthyear", self.info["birth"]["year"])
#     self.fill_select("country", "2")

# def edit_date_access_page(self):
#     self.browser.execute_script(js_scripts.stop_timer())
#     response_element = self.browser.find_element(
#         By.CLASS_NAME, "copyright")
#     while True:
#         script = js_scripts.get_date_edit_page()
#         self.browser.execute_script(script)
#         sleep(3)
#         response = response_element.get_attribute("innerHTML")
#         log("get_date_res:", response)

#         if response.startswith("error"):
#             raise utils.TOO_MUCH_REQ_EXCEPTION(
#                 "err when getting date via console")
#         elif len(response) != 10:  # means there is time
#             utils.multiNotify(4)
#             log("!!!free time!!!")
#             while True:
#                 ...
#         sleep(20)
