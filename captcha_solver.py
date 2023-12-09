from bs4 import BeautifulSoup
import numpy as np
import cv2
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pickle
from utils import log
import tensorflow as tf
import time
import json

black = 0
white = 255

file = open("configs.json", "r", encoding="utf-8")
configs = json.loads(file.read())
file.close()

model_path = configs["model_path"]
le_path = configs["le_path"]


class Captcha_Solver():

    def __init__(self, browser) -> None:
        self.browser = browser
        self.tries = 0
        self.prediction = None
        self.model = tf.keras.models.load_model(model_path)
        self.chars = None
        with open(le_path, "rb") as le_file:
            self.le = pickle.load(le_file)

    def tune_captcha(self, preElement, scale=6, one_dimension=True):
        captcha_w = 80
        captcha_h = 7
        img = np.zeros((captcha_w*captcha_h,))
        soup = BeautifulSoup(preElement, "html.parser")
        pre = soup.find("pre")
        # pre["style"] = "font-size: 6px; line-height: 5px;"
        spans = pre.findChildren("span")

        for i, span in enumerate(spans):

            if (span["style"].find("bold") == -1):
                # span["style"] = "color:#000000"
                img[i] = 0
            else:
                # span["style"] = "font-weight:bold; color:#ffffff"
                img[i] = 255

            # span.string.replace_with("@")

        img = img.reshape((captcha_h, captcha_w, 1))
        if not one_dimension:
            img = np.repeat(img, 3, axis=2)
        if scale:
            img = cv2.resize(img, (captcha_w*scale, captcha_h*scale),
                             interpolation=cv2.INTER_AREA)

        pad = 10
        img = cv2.copyMakeBorder(img, pad, pad, pad, pad,
                                 cv2.BORDER_CONSTANT, None, 0)
        return img

    def split_chars(self):
        resized_h = 112
        resized_w = 110
        slices = []
        shouldSlice = True
        for j in range(0, self.chars.shape[1]):
            col = self.chars[:, j]
            if not shouldSlice and np.any(col == white):
                shouldSlice = True
            if shouldSlice and np.all(col == black):
                slices.append(j)
                shouldSlice = False

        img_segments = []
        for i, _ in enumerate(slices):
            if (i == 0):
                slice = self.chars[:, 0:slices[i]]
            else:
                slice = self.chars[:, slices[i-1]:slices[i]]
            width = slice.shape[1]
            if width > 10:
                img_segments.append(slice)

        padding = 25
        for i, segment in enumerate(img_segments):
            inv = cv2.copyMakeBorder(
                segment, padding, padding, padding, padding, cv2.BORDER_CONSTANT, None, black)
            inv = cv2.resize(inv, (resized_w, resized_h))
            inv = -inv+255
            img_segments[i] = inv
        img_segments = np.array(img_segments)
        img_segments = img_segments.reshape(img_segments.shape + tuple([1]))
        self.chars = img_segments

    def correct_captcha(self):

        try:
            alert = self.browser.find_element(
                By.CSS_SELECTOR, ".sweet-alert").get_attribute("class")
        except NoSuchElementException as e:
            return True
        if alert.find("showSweetAlert") != -1:
            WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".sa-confirm-button-container .confirm")))

            self.browser.find_element(
                By.CSS_SELECTOR, ".sa-confirm-button-container .confirm ").click()

            rand_name = str(time.time())[-9:-1].replace(".", "0")
            file_name = self.prediction+"-"+rand_name
            cv2.imwrite(f"./wrong_imgs/{file_name}.png", self.img)
            file = open("./wrong_imgs.txt", "a")
            file.write(f"{file_name}={self.prediction}" + "\n")
            file.close()
            log("wrong prediction")
            return False
        else:
            return True

    def find_and_tune(self):
        captchaHtml = self.browser.find_element(
            By.CSS_SELECTOR, ".newCaptcha").get_attribute("innerHTML")
        tuned_captcha_img = self.tune_captcha(captchaHtml)

        self.chars = tuned_captcha_img
        self.img = tuned_captcha_img.copy()

    def predict_captcha(self):

        scaled_chars = self.chars/255
        prediction = self.model.predict(scaled_chars)
        prediction = np.argmax(prediction, axis=1)
        print(prediction)
        prediction = self.le.inverse_transform(prediction)
        self.prediction = "".join(prediction)

    def send_captcha_pred(self):
        input_captcha = self.browser.find_element(By.NAME, "inputCaptcha")
        input_captcha.clear()
        input_captcha.send_keys(self.prediction)

    def refresh_captcha(self):
        self.browser.find_element(By.ID, "buttonCaptcha").click()

    def solve_captcha(self, by=By.NAME, btn="schengenBtn"):
        if self.tries > 1:
            raise Exception("too many captcha solving attempts")

        self.find_and_tune()
        self.split_chars()
        self.predict_captcha()
        log("prediction: ", self.prediction)
        self.send_captcha_pred()
        self.browser.find_element(by, btn).click()
        self.tries += 1
