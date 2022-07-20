# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 16:28:16 2022

@author: 47176
"""

from PIL import Image
from io import BytesIO
import requests
import numpy as np
from skimage import morphology
from sklearn.cluster import KMeans
import pickle
image_width = 30


image_file = r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如\data\测试价格图片.png'    
image = Image.open(image_file)

images = []
for i in range(10):
    im = image.crop((image_width*i, 0, image_width *
                     (i+1), image.size[1])).convert('L')
    images.append(im)

model_path = r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如\示例代码\train\LR.pickle'    


def thresholding(image):
    predicted = KMeans(n_clusters=2, random_state=9).fit_predict(
        image.reshape((image.shape[0]*image.shape[1], 1)))
    image = predicted.reshape((image.shape[0], image.shape[1]))
    return image

def thin(image):
    image = thresholding(np.array(image))
    thin_image = morphology.skeletonize(image)
    return thin_image

def predict(model, image):
    image = thin(image)
    return model.predict(image.reshape((1, -1)))[0]

def ocr(position, image_file):
    image = Image.open(image_file)
    images = []
    for i in range(10):
        im = image.crop((image_width*i, 0, image_width *
                         (i+1), image.size[1])).convert('L')
        images.append(im)
    model = None
    with open(model_path, 'rb') as fr:
        model = pickle.load(fr)
    numbers = []
    for image in images:
        number = predict(model, image)
        numbers.append(number)
    value = []
    for pos in position:
        value.append(str(numbers[pos]))
    return int(''.join(value))

#%%

a = ocr(0, image_file)



