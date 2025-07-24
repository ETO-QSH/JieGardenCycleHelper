import re
import cv2
import pytesseract


def match_template(screen_img_path, template_img_path, threshold=0.8):
    """
    在screen_img_path截图中查找template_img_path模板，返回匹配中心坐标和最大相似度
    :param screen_img_path: 屏幕截图路径
    :param template_img_path: 模板图片路径
    :param threshold: 匹配阈值
    :return: (center_x, center_y, max_val) 或 None
    """
    screen = cv2.imread(screen_img_path, cv2.IMREAD_COLOR)
    template = cv2.imread(template_img_path, cv2.IMREAD_COLOR)
    if screen is None or template is None:
        return None

    # 灰度化
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        center = max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2
        return max_loc, template.shape, center, max_val
    else:
        return None


def ocr_image(image_path, lang='chi_sim+eng'):
    """
    对指定图片进行OCR识别，返回识别到的数字和汉字字符串
    :param image_path: 图片路径
    :param lang: 语言包，默认中英文
    :return: 识别到的字符串
    """
    img = cv2.imread(image_path)
    if img is None:
        return ""

    # 可选：转为灰度、二值化等预处理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    str_list = [
        '0123456789', '零壹贰叁肆伍陆', '祸乱', '传说', '杂疑', '故肆', '拾遗', '易与', '常乐', '筹谋',
        '是非境', '洪陆楼', '山水阁', '云瓦亭', '汝吾门', '见字祠', '始末陵', '种因得果', '掷地有声', '三缺一',
        '欣然应许', '消耗获得源石锭', '还是算了', '多一事不如少一事', '确定这么做', '衡如常', '厉如锋', '花如簇',
        '当前持有花衡厉钱枚', '天随人愿', '不尽人意', '什么都没有发生', '收下', '离开', '来就来', '还是算了',
        '剩余烛火', '自选奖励', '要兵器一对', '书一卷', '酒一壶', '钱盒', '，？',
    ]
    custom_config = r'-c tessedit_char_whitelist={} --psm 6'.format(''.join(set(''.join(str_list))))

    text = pytesseract.image_to_string(gray, lang=lang, config=custom_config)
    filtered = ''.join(re.findall(r'[\u4e00-\u9fa5\d]+', text))
    return filtered
