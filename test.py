from PIL import Image
import pickle
import numpy as np

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


pic = r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如\train\4.jpg'
t = Image.open(pic)


with open(r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如\train\LR.pkl', 'rb') as f:
    model = pickle.load(f)

a = model.predict(pic2vec(t))