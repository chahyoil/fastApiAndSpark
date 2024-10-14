# utils/logging_utils.py

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(env: str = "dev"):
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_level = logging.DEBUG if env == "dev" else logging.INFO
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # 기존 핸들러 제거
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 콘솔 핸들러 추가
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console_handler)
    
    # 파일 핸들러 추가
    file_handler = RotatingFileHandler(
        f"{log_dir}/app.log", maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(file_handler)

    # py4j 로거 레벨 조정
    logging.getLogger("py4j").setLevel(logging.WARNING)

def get_logger(name: str):
    return logging.getLogger(name)