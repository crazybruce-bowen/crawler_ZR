# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 10:15:42 2022

@author: 47176
"""

import requests

url = 'https://static8.ziroom.com/phoenix/pc/images/price/new-list/dff9d441e1fc59f793d5c3b68461b3ea.png'

r = requests.get(url)

path = r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如\result\20220817\test_pic.jpeg'
with open(path, 'wb') as f:
    f.write(r.content)

#%%
from matplotlib import image
from matplotlib import pyplot as plt
from io import BytesIO

import urllib
from PIL import Image

url = 'https://static8.ziroom.com/phoenix/pc/images/price/new-list/dff9d441e1fc59f793d5c3b68461b3ea.png'
r = requests.get(url)
c = r.content

# t = image.imread(url)

t2 = Image.open(urllib.request.urlopen(url))

t3 = plt.imread(BytesIO(c))
price_info_str = 'background-image: url(//static8.ziroom.com/phoenix/pc/images/price/new-list/2e120609b7f35a9ebec0c72c4b7502b2.png);background-position: -64.2px||background-image: url(//static8.ziroom.com/phoenix/pc/images/price/new-list/2e120609b7f35a9ebec0c72c4b7502b2.png);background-position: -149.8px||background-image: url(//static8.ziroom.com/phoenix/pc/images/price/new-list/2e120609b7f35a9ebec0c72c4b7502b2.png);background-position: -128.4px||background-image: url(//static8.ziroom.com/phoenix/pc/images/price/new-list/2e120609b7f35a9ebec0c72c4b7502b2.png);background-position: -192.6px'

#%% 主会场

import pandas as pd
import re

df = pd.read_excel(r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如\result\20220816\info.xlsx')
price_info = df['price_info']

a = price_info[0]
b = [re.findall('background-position: (.*)', i) for i in a.split('||')]

# def get_px_values(s) -> list:
#     """ 根据price_info字符提取px信息 """
#     return re.findall('-*\d+.\d+px', s)

def get_px_values(s) -> list:
    """ 根据price_info字符提取px信息 """
    res = list()
    for i in s.split('||'):
        res += re.findall('background-position: (.*)', i)
    return res

price_info_list = list()
for i in df['price_info']:
    price_info_list += get_px_values(i)

k = list(set(price_info_list))




