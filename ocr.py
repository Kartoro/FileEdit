import aircv
from PIL import Image, ImageEnhance
import pytesseract
import os

def matchImg(imgsrc, imgobj, confidence=0.2):
    """
     图片对比识别imgobj在imgsrc上的相对位置（批量识别统一图片中需要的部分）
    :param imgsrc: 原始图片路径(str)
    :param imgobj: 待查找图片路径（模板）(str)
    :param confidence: 识别度（0<confidence<1.0）
    :return: None or dict({'confidence': 相似度(float), 'rectangle': 原始图片上的矩形坐标(tuple), 'result': 中心坐标(tuple)})
    """
    imsrc = aircv.imread(imgsrc)
    imobj = aircv.imread(imgobj)

    match_result = aircv.find_template(imsrc, imobj, confidence)  # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽

    return match_result


def cutImg(imgsrc, out_img_name, coordinate):
    """
     根据坐标位置剪切图片
    :param imgsrc: 原始图片路径(str)
    :param out_img_name: 剪切输出图片路径(str)
    :param coordinate: 原始图片上的坐标(tuple) egg:(x, y, w, h) ---> x,y为矩形左上角坐标, w,h为右下角坐标
    :return:
    """
    image = Image.open(imgsrc)
    region = image.crop(coordinate)
    region = ImageEnhance.Contrast(region).enhance(1.5)
    region.save(out_img_name)


def getFileList(dir, Filelist, ext=None):
    """
    获取文件夹及其子文件夹中文件列表
    输入 dir：文件夹根目录
    输入 ext: 扩展名
    返回： 文件路径列表
    """
    newDir = dir
    if os.path.isfile(dir):
        if ext is None:
            Filelist.append(dir)
        else:
            if ext in dir[-3:]:
                Filelist.append(dir)

    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            getFileList(newDir, Filelist, ext)

    return Filelist

imgFolder = './' # image folder dir
imgList = getFileList(imgFolder, [], 'png')

for imgpath in imgList:
    cutImg(imgpath, 'tmp.png', (142, 177, 314, 203))
    cut = Image.open(cutImg)
    code = pytesseract.image_to_string(cut, lang='chi_sim') # 需要下载tesseract-OCR和简体中文语言包
    os.rename(imgpath, code+'.png')
