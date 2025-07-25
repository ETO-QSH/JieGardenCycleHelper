import os
import time
from datetime import datetime, timedelta

from adb_service import take_screenshot, adb_tap
from cv_service import match_template, ocr_image
from public_object import adb_path, screenshot_dir, picture_dir, ocr_pic, log, log_file


def match_and_tap(template):
    while True:
        if screenshot := take_screenshot(adb_path, screenshot_dir):
            if center := match_template(screenshot, os.path.join(picture_dir, template))[0]:
                return adb_tap(adb_path, *center)
        time.sleep(1)


def match_and_orc(template, rec):
    if screenshot := take_screenshot(adb_path, screenshot_dir):
        if res := match_template(screenshot, os.path.join(picture_dir, template)):
            center, roi, _ = res
            return ocr_image(roi[rec[1]: rec[3], rec[0]: rec[2]])
    return None


def match_only(template):
    if screenshot := take_screenshot(adb_path, screenshot_dir):
        if match_template(screenshot, os.path.join(picture_dir, template))[0]:
            return True
    return False


def safe_exit(code):
    [os.remove(os.path.join(screenshot_dir, f)) for f in os.listdir(screenshot_dir) if os.path.isfile(os.path.join(screenshot_dir, f))]
    log("屏幕截图已清理，程序退出运行")
    log_file.close()
    exit(code)


def delete_old_screenshots(folder_path=screenshot_dir, minutes=1):
    now = datetime.now()
    cutoff = now - timedelta(minutes=minutes)

    for filename in os.listdir(folder_path):
        if not filename.startswith("screen_") or not filename.endswith(".png"):
            continue

        try:
            timestamp_str = filename[7:-4]
            file_time = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S_%f")
        except ValueError:
            continue

        if file_time < cutoff:
            file_path = os.path.join(folder_path, filename)
            try:
                os.remove(file_path)
                print(f"已删除：{filename}")
            except Exception as e:
                print(f"删除失败：{filename}，原因：{e}")


def do_circle(live_state, policy):
    time.sleep(1)

    if not match_only(ocr_pic['退出']):
        log("未检测到标志物，出于安全考虑拒绝操作")
        return 0

    if match_only(ocr_pic['钱盒']):
        live_state.candle = int(match_and_orc(*ocr_pic['剩余烛火']))
        live_state.prize_count = int(match_and_orc(*ocr_pic['收藏品']))

    live_state.originium = int(match_and_orc(*ocr_pic['源石锭']))
    live_state.tickets = int(match_and_orc(*ocr_pic['票券']))

    choice, sub_choice = policy(live_state)

    if choice == '茧成绢':
        if match_only(ocr_pic['钱盒']):
            match_and_tap(ocr_pic['钱盒'])

        match_and_tap(ocr_pic['重新投钱'])
        match_and_tap(ocr_pic['投钱确认'])
        match_and_tap(ocr_pic['投钱结束确认'])

    else:
        if match_only(ocr_pic['收起']):
            match_and_tap(ocr_pic['收起'])

        match_and_tap(ocr_pic['小常乐'])
        match_and_tap(ocr_pic['前往出发'])

        while True:
            if match_only(ocr_pic['黍']):
                head = '黍'
                break
            if match_only(ocr_pic['年']):
                head = '年'
                break
            if match_only(ocr_pic['令']):
                head = '令'
                break
            time.sleep(1)

        if head != '令':
            log(f"常乐-{head}，不符合要求")
            return 1
