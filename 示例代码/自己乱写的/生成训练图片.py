from PIL import Image
import os

# 读取下载的图片
image_file = r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如\data\测试价格图片.png'    
image = Image.open(image_file)

# 分割图片数字
images = []
image_width=30
for i in range(10):
    im = image.crop((image_width*i, 0, image_width *
                     (i+1), image.size[1]))
    im_grey = im.getchannel(3)  # 生成灰度训练图片
    images.append(im_grey)

# 输出训练图片数字
train_pic_path = r'D:\Learn\学习入口\大项目\爬他妈的\住房问题\自如\data'
for n, i in enumerate(images):
    i.save(os.path.join(train_pic_path, '{}.jpg'.format(n)))
    
# 手动更改训练图片名称
