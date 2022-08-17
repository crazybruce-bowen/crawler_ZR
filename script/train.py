#! /usr/bin/python3
# Attention path
from PIL import Image
import numpy as np
from skimage import morphology
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression as LR
import pickle
import os

path = r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如'
os.chdir(path)

model_path = 'data/LR_0817.pickle'


def convert_PIL(image):
    image = Image.fromarray(image).convert('L')
    return image


def thresholding(image):
    predicted = KMeans(n_clusters=2, random_state=9).fit_predict(
        image.reshape((image.shape[0]*image.shape[1], 1)))
    image = predicted.reshape((image.shape[0], image.shape[1]))
    return image


def thin(image):
    image = thresholding(np.array(image))
    thin_image = morphology.skeletonize(image)
    return thin_image


def train():
    model = LR()
    images = []
    for i in range(10):
        image = Image.open('data/training_data/%d.jpg' % i)
        image = thin(image)
        images.append(image)
    images = np.array(images)
    images = images.reshape((10, -1))
    print(images.shape)
    X = images
    # Y = np.reshape(np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]), (10, 1))
    Y = np.array(range(10))
    model.fit(images, Y)
    # save model
    with open(model_path, 'wb') as fw:
        pickle.dump(model, fw)


if __name__ == '__main__':
    train()
