# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:32:51 2022

@author: 47176
"""
# Environment

import requests
import pandas as pd
import numpy as np
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import json
import time
from multiprocessing import Pool
import re


#%% Functions
# Init Func
def get_one_page_html(url):
    """ 获取网站每一页的html """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/85.0.4183.121 Safari/537.36"
        }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None

# Self Define Func
def get_house_base_info(html):
    """ 根据首页返回房源的基础信息和网页ID """
    


#%%



#%% Test

url = 'https://sh.ziroom.com/z/z2-u14%7C13-r0/?p=a1|2|3&cp=0TO7000&isOpen=1'

t = get_one_page_html(url)












