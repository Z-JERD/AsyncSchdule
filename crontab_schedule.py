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
def crontab_demo():
    """定时任务示例, 取值斐波那契数列"""
    res = dict()
    num = 30

    logger.info(" request: num is %s " % num)

    if isinstance(num, int):
        r = recursion(num)
        res[num] = r

    logger.info(" response: res is %s " % res)

    return res

