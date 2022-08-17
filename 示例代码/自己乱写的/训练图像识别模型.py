from PIL import Image
import numpy as np
from skimage import morphology
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression as LR
import pickle
import os

model_path = r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如\train\LR.pkl'

def pic2vec(image):
    """
    将Image读取的图片转换为一维数组

    Parameters
    ----------
    image : PIL.JpegImagePlugin.JpegImageFile
        DESCRIPTION. 读取的图片

    Returns
    -------
    res: 一维数组

    """
    return np.array(image).reshape(1, -1)
    

def train():
    model = LR()
    images = []
    os.chdir(r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如')
    for i in range(10):
        image = Image.open('train/%d.jpg' % i)
        images.append(pic2vec(image))
    images = np.array(images)
    images = images.reshape((10, -1))
    print(images.shape)
    
    model.fit(images, np.array(range(10)))
    
    
    # save model
    with open(model_path, 'wb') as fw:
        pickle.dump(model, fw)

#%%
if __name__ == '__main__':
    train()