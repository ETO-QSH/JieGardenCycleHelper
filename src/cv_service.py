import re
import cv2
import numpy as np
import pytesseract

from public_object import log

pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'


def imread_unicode(path, flags=cv2.IMREAD_COLOR):
    """兼容中文路径的 cv2.imread 封装"""
    with open(path, 'rb') as f:
        buf = np.frombuffer(f.read(), np.uint8)
    img = cv2.imdecode(buf, flags)
    if img is None:
        raise FileNotFoundError(f"无法读取图片：{path}")
    return img


def match_template(screen_img_path, template_img_path, threshold=0.8):
    """
    :param screen_img_path: 屏幕截图路径
    :param template_img_path: 模板图片路径
    :param threshold: 匹配阈值
    """
    # 读取图片
    screen = imread_unicode(screen_img_path)
    template = imread_unicode(template_img_path)

    # 灰度化
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 匹配
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        center = max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2
        roi = screen[max_loc[1]: max_loc[1] + template.shape[0], max_loc[0]: max_loc[0] + template.shape[1]]
        log(f"匹配到：{center}, 匹配值为：{max_val}")
        return center, roi, max_val
    else:
        log(f"未匹配到有效区域, 匹配值为：{max_val}")
        return None, None, max_val


def ocr_image(img):
    str_list = [
        '0123456789', '零壹贰叁肆伍陆', '祸乱', '传说', '杂疑', '故肆', '拾遗', '易与', '常乐', '筹谋',
        '是非境', '洪陆楼', '山水阁', '云瓦亭', '汝吾门', '见字祠', '始末陵', '种因得果', '掷地有声', '三缺一',
        '欣然应许', '消耗获得源石锭', '还是算了', '多一事不如少一事', '确定这么做', '衡如常', '厉如锋', '花如簇',
        '当前持有花衡厉钱枚', '天随人愿', '不尽人意', '什么都没有发生', '收下', '离开', '来就来', '还是算了',
        '剩余烛火', '自选奖励', '要兵器一对', '书一卷', '酒一壶', '钱盒', '，？',
    ]

    # cv2.imshow("ROI", img)
    # cv2.waitKey(0)  # 按任意键关闭
    # cv2.destroyAllWindows()

    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    text = pytesseract.image_to_string(th, lang='chi_sim', config=f'--psm 7').replace(' ', '')
    return text
