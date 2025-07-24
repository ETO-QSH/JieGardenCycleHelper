import os
import json
from datetime import datetime


def log(msg, log_file):
    timestamp = datetime.now().strftime('%Y/%m/%d %H-%M-%S')
    log_file.write(f"[{timestamp}] {msg}\n")
    log_file.flush()


def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # 获取项目根目录

config_path = os.path.join(project_root, 'config.json')
config = load_config(config_path)
