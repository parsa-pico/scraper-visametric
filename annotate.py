import cv2
import numpy as np
import imutils
from imutils import paths
import os
import time
list_imgs = paths.list_images("./wrong_chars")
save_path = "./labled_chars"
for img_index, img_path in enumerate(list_imgs):
    img = cv2.imread(img_path)
    cv2.imshow("win", img)
    key = cv2.waitKey(0)
    key = chr(key)
    if (key == "`"):
        print("ignoring this char")
        continue
    dir_path = os.path.sep.join([save_path, key.upper()])
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    new_img_path = os.path.sep.join([dir_path, str(time.time()) + ".png"])
    cv2.imwrite(new_img_path, img)
