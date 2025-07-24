import os

from public_object import log, config, project_root
from adb_service import check_adb_path, check_adb_device, take_screenshot


if __name__ == "__main__":

    log_path = os.path.join(project_root, config['log_file'])
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log(log_file=log_file, msg="-" * 100)
        log(log_file=log_file, msg=f"读取到配置：{config}")

        adb_path = config['adb_path']
        screenshot_dir = os.path.join(project_root, config['screenshot_dir'])

        check_adb_path(adb_path, log_file)

        # 检查adb服务
        if not check_adb_device(adb_path, log_file):
            log("未检测到已连接的模拟器或设备，请先启动MuMu模拟器并确保adb可用。", log_file)
            exit(1)

        take_screenshot(adb_path, screenshot_dir, log_file)
