import sys
path = r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如'
if path not in sys.path:
    sys.path.append(path)

from script.html_service import get_one_page_html
from pyquery import PyQuery as pq
import re
from script.utils import print_time
import numpy as np
import time
from script.io_service import save_info_to_local, save_info_to_mongodb
from multiprocessing import Process, Pool


class RoomInfoCatching:
    def __init__(self):
        self.url_base = 'https://sh.ziroom.com/'
        self.url_selectoin = 'https://sh.ziroom.com/z/z2-r0/?cp=4000TO8000'  # 4k-8k TODO 改成动态生成
        self.urls_area = None

    def generate_area_urls(self):
        doc = pq(get_one_page_html(self.url_selectoin))
        urls_items = doc('div.opt-type')(' span.opt-name:contains(区域)').parent()('div.wrapper a.item').items()
        res = list()
        for i in urls_items:
            res.append({'area': i.text(),
                        'url': 'https:' + i.attr('href')})
        self.urls_area = res
        return res

    def get_url_by_area(self, area):
        """ 获取某区域的url """
        area_info_list = self.generate_area_urls() if not self.urls_area else self.urls_area
        area_url = dict(zip([i['area'] for i in area_info_list], [i['url'] for i in area_info_list])).get(area)
        return area_url

    def find_page_url(self, url_area) -> [str]:
        """ 根据区域url获取分页url list """
        doc = pq(get_one_page_html(url_area))
        page_num_text = doc('div.Z_pages span:contains(共)').text()
        if not page_num_text:
            return list()
        page_num = int(re.findall('共(\d+)页', page_num_text)[0])
        url_page1 = 'https:' + doc('div.Z_pages a.active').attr('href')
        tmp = re.match('(.*p)\d(.*)', url_page1)
        res = list()
        for i in range(page_num):
            res.append(tmp.group(1) + str(i) + tmp.group(2))
        return res
        
    def find_room_url(self, url_pg) -> [dict]:
        """ 根据分页地址去解析房间url链接 """
        doc = pq(get_one_page_html(url_pg))
        info_items = doc('div.Z_list-box h5.title a').items()
        res = list()
        for i in info_items:
            res.append({'room_name': i.text(),
                        'url': i.attr('href')})
        return res
    
    def get_room_info_page(self, url_pg) -> [dict]:  # 获取一整个页面的房间信息
        """
        根据分页的页面获取房源信息
    
            name: 房间名
            area: 面积
            price: 房间价格
            orientation: 朝向
            types: 房间类型
            floor: 房间楼层
            updated_info: 房间维护信息
        """
    
        doc = pq(get_one_page_html(url_pg))  # doc
        room_info = doc('div.item').items()
        res = list()
        for i in room_info:
            name = i('div.info-box a').text()  # 名称
            url = 'https:' + i('div.info-box a').attr('href')
            area_desc_str = i('div.desc div:nth-of-type(1)').text()
            area_str = area_desc_str.split('|')[0]
            area = float(re.findall('(.*)㎡', area_str)[0])  # 面积
            tmp_types = area_desc_str.split('|')[1]
            if len(tmp_types.split('/')) > 1:
                types = re.findall('.*(\d+居室).*', name)[0]
                floor = int(tmp_types.split('/')[0])
            else:
                types = tmp_types
                floor = ''
            locations = i('div.desc>div.location').text()
            price_info = '||'.join([num.attr('style') for num in i('div.price span.num').items()])  # ||分割改list为str
            tags = '||'.join([tag.text() for tag in i('div.tag span').items()])  # ||分割改list为str

            dict_info = {'name': name, 'room_url': url, 'area_str': area_str, 'price_info': price_info,
                         'area': area, 'room_types': types, 'locations': locations, 'tags': tags, 'floor': floor,
                         }
            res.append(dict_info)

        return res

    def get_room_info_by_area(self, area):
        area_url = self.get_url_by_area(area)
        if not area_url:
            return False, '未获取到该区 {} 的链接，支持的区域为 {}'.format(area, [i['area'] for i in self.generate_area_urls()])
    
        urls_area_pg = self.find_page_url(area_url)
        room_info_total = list()
        print('== 该区域 {} 共有页面 {} 个'.format(area, len(urls_area_pg)))
        n = 0
        for i in urls_area_pg:
            n += 1
            print('== 开始计算第 {} 个页面 =='.format(n))
            room_info_list = self.get_room_info_page(i)
            for room_info in room_info_list:
                room_info['区域'] = area
            room_info_total += room_info_list
        return room_info_total

    @print_time
    def get_room_info_total(self):
        urls_area_list = self.generate_area_urls()
        room_info_total = list()
        for i in urls_area_list:
            room_info_total += self.get_room_info_by_area(i['area'])
            print('== 完成 {} 区域'.format(i['area']))
        return room_info_total



#%%
t = RoomInfoCatching()
# url = 'https://sh.ziroom.com/z/z2-d310106-r0-p1/?cp=4000TO8000'
# # html = get_one_page_html(url)
# # doc = pq(html)
# res = t.get_room_info_page(url)
a = t.generate_area_urls()
# res = t.get_room_info_total()
#%%
# url = 'https://sh.ziroom.com/x/745530151.html'
# html = get_one_page_html(url)
# doc = pq(html)
# with open(r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如\html示例\普通房源样例.html', 'w', encoding='utf-8') as f:
#     f.write(html)    
    
# doc = pq(html)    
# a = doc('div.opt-type')(' span.opt-name:contains(区域)')
# b = a.parent()('div.wrapper a.item').items()
# c = list()
# for i in b:
#     c.append(i.attr('href'))

#a = t.generate_area_urls()
#%%
# a = doc('div.item').items()
# b = a.__next__()

# name = b('div.info-box a').text()  # 名称
# url = 'https:' + b('div.info-box a').attr('href')
# area_desc_str = b('div.desc div:nth-of-type(1)').text()
# area_str = area_desc_str.split('|')[0]
# area = float(re.findall('(.*)㎡', area_str)[0])  # 面积
# types = area_desc_str.split('|')[1]
# locations = b('div.desc>div.location').text()
# price_info = [num.attr('style') for num in b('div.price span.num').items()]
# tags = [tag.text() for tag in b('div.tag span').items()]




