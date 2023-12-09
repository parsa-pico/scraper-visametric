import os
import cv2
import numpy as np
from imutils import paths
import glob
black = 0
white = 255

imgs_path = "./wrong_imgs"
chars_path = "./wrong_chars"

list_imgs = list(paths.list_images(imgs_path))
char_index = len(list(paths.list_images(chars_path)))+1

list_imgs = sorted(list_imgs, key=os.path.getmtime, reverse=True)


for img_index, img_path in enumerate(list_imgs):

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(
        gray, 128, 255,  cv2.THRESH_BINARY)

    pre_img = thresh1
    # cv2.imshow("win", pre_img)
    # cv2.waitKey(0)
    slices = []
    shouldSlice = True

    for j in range(0, pre_img.shape[1]):
        col = pre_img[:, j]

        if not shouldSlice and np.any(col == white):
            shouldSlice = True

        if shouldSlice and np.all(col == black):
            slices.append(j)
            shouldSlice = False

    img_segments = []
    for i, _ in enumerate(slices):

        if (i == 0):
            slice = pre_img[:, 0:slices[i]]
        else:
            slice = pre_img[:, slices[i-1]:slices[i]]
        width = slice.shape[1]
        if width > 10:
            img_segments.append(slice)

    for i, segment in enumerate(img_segments):
        padding = 25

        inv = cv2.copyMakeBorder(
            segment, padding, padding, padding, padding, cv2.BORDER_CONSTANT, None, black)
        inv = cv2.bitwise_not(inv)
        print(char_index)
        cv2.imwrite(f'{chars_path}/char-{char_index}.png', inv)
        # cv2.imshow("win2", inv)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        char_index += 1
