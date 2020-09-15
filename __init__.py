from celery import Celery
from .log_config import *

CELERY_PATH = ""

schedule_task = Celery('celery_schedule')                                # 创建 Celery 实例
schedule_task.config_from_object('celery_schedule.celery_config')        # 通过 Celery 实例加载配置模块
logger = setup_logging(log_path=CELERY_PATH)

