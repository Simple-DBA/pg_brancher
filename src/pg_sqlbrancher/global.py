import logging
import os
import yaml
from datetime import datetime

log_period = 'month'  # 로그 파일 기록 단위 설정 (month, day, 등)
log_level = logging.INFO  # 로그 레벨 설정
file_handler = None  # 전역 변수로 파일 핸들러 초기화
log_path = '/content'

def pgbrancher_logger(log_classification,log_str):
    global log_path

    # 로그 파일 이름 생성
    if log_period == 'year':
        log_file_name = 'pgbrancher' + datetime.now().strftime('%Y') + '.log'
    elif log_period == 'month':
        log_file_name = 'pgbrancher' + datetime.now().strftime('%Y%m') + '.log'
    elif log_period == 'day':
        log_file_name = 'pgbrancher' + datetime.now().strftime('%Y%m%d') + '.log'
    else:
        log_file_name = 'pgbrancher.log'

    # 파일 핸들러 생성
    file_handler = logging.FileHandler(log_path+'/'+log_file_name)

    # 로거 생성
    logger = logging.getLogger('pgbrancher_logger')
    logger.setLevel(log_level)

    # 파일 핸들러 추가
    logger.addHandler(file_handler)

    # 포멧 지정
    if logger.level >= logging.INFO:
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s] : %(message)s')
    else:
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(funcName)s] : %(message)s')

    file_handler.setFormatter(formatter)

    # 로깅
    if log_classification == 'DEBUG':
      logger.debug(log_str)
    if log_classification == 'INFO':
      logger.info(log_str)
    if log_classification == 'WARNING':
      logger.warning(log_str)
    if log_classification == 'ERROR':
      logger.error(log_str)
    if log_classification == 'CRITICAL':
      logger.critical(log_str)

    # 파일 핸들러 제거
    logger.removeHandler(file_handler)

# # 테스트용 예시
# pgbrancher_logger('ERROR','This is a test log message.')

# YAML 파일 로드
def yaml_loader(yaml_file):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
    return config
