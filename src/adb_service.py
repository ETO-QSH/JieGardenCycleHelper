import os
import subprocess
from datetime import datetime

from public_object import log


def check_adb_path(adb_path, log_file):
    if os.path.isfile(adb_path):
        log(f"adb.exe 检查通过: {adb_path}", log_file)
    else:
        log(f"adb.exe 未找到: {adb_path}", log_file)
        exit(1)


def check_adb_device(adb_path, log_file):
    result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()
    for line in lines[1:]:
        if line.strip() and 'device' in line and 'offline' not in line:
            log("adb服务检测：已连接设备", log_file)
            return True
    log("adb服务检测：未检测到已连接的模拟器或设备", log_file)
    return False


def take_screenshot(adb_path, screenshot_dir, log_file):
    os.makedirs(screenshot_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
    screenshot_path = os.path.join(screenshot_dir, f'screen_{timestamp}.png')

    log("开始截图到模拟器... --> ['/sdcard/screen.png']", log_file)
    subprocess.run([adb_path, 'shell', 'screencap', '-p', '/sdcard/screen.png'], check=True)
    log(f"拉取截图到本地: {screenshot_path}", log_file)
    subprocess.run([adb_path, 'pull', '/sdcard/screen.png', screenshot_path], check=True)
    log(f"截图已保存到: {screenshot_path}", log_file)
    return screenshot_path


def adb_tap(adb_path, x, y, log_file):
    log(f"点击操作: tap ({x}, {y})", log_file)
    subprocess.run([adb_path, 'shell', 'input', 'tap', str(x), str(y)], check=True)


def adb_swipe(adb_path, x1, y1, x2, y2, duration_ms=300, log_file=None):
    log(f"滑动操作: swipe ({x1}, {y1}) -> ({x2}, {y2}), 持续 {duration_ms} ms", log_file)
    subprocess.run([adb_path, 'shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration_ms)], check=True)


def adb_input_text(adb_path, text, log_file):
    log(f"输入文本: {text}", log_file)
    subprocess.run([adb_path, 'shell', 'input', 'text', text], check=True)


def adb_key_event(adb_path, keycode, log_file):
    log(f"发送按键事件: keyevent {keycode}", log_file)
    subprocess.run([adb_path, 'shell', 'input', 'keyevent', str(keycode)], check=True)

# 示例：点击屏幕中心
# adb_tap(adb_path, 540, 960, log_file)

# 示例：滑动
# adb_swipe(adb_path, 500, 1000, 500, 500, duration_ms=500, log_file=log_file)

# 示例：输入文本
# adb_input_text(adb_path, "HelloWorld", log_file)

# 示例：发送返回键
# adb_key_event(adb_path, 4, log_file)  # 4是安卓返回键
