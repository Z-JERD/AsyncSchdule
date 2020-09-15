import traceback
from celery_schedule import schedule_task, logger


def recursion_tool(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return recursion_tool(n - 1) + recursion_tool(n - 2)


def recursion(n):
    result_list = []
    for i in range(1, n + 1):
        result_list.append(recursion_tool(i))

    return result_list


@schedule_task.task
def async_demo(num):
    """异步调用示例 斐波那契数列"""
    logger.info(" request: num is %s " % num)
    res = []

    if isinstance(num, int):
        res = recursion(num)

    logger.info(" response: res is %s " % res)

    return res


@schedule_task.task(bind=True, default_retry_delay=60, max_retries=3)
def async_retry(self, num):
    """重试机制
    bind=True 绑定task对象
    default_retry_delay=60 60秒后重试
    max_retries=3 最大重试次数
    self.retry() 内置重试函数
    """

    logger.info(" request: num is %s " % num)

    try:
        num["age"]
        res = recursion(num)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise self.retry()

    logger.info(" response: res is %s " % res)

    return res

