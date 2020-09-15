import json
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
def cycle_demo(num1, num2):
    """周期任务示例, 对传过来的数值 取值斐波那契数列
    获取task_id 任务名.request.id

    <Context: {'lang': 'py', 'task': 'celery_schedule.cycle_schedule.cycle_demo',
     'id': 'dc339408-d916-41d6-a231-79d9a6c1fe3d', 'shadow': None, 'eta': None,
     'expires': None, 'group': None, 'group_index': None,
     'retries': 0, 'timelimit': [None, None],
      'root_id': 'dc339408-d916-41d6-a231-79d9a6c1fe3d', 'parent_id': None,
      'argsrepr': '[5, 8]', 'kwargsrepr': '{}',
      'origin': 'gen7172@localhost', 'reply_to': '3e553646-b1e3-3b42-b368-fcf1e04fb8c1',
      'correlation_id': 'dc339408-d916-41d6-a231-79d9a6c1fe3d', 'hostname': 'celery@localhost',
       'delivery_info': {'exchange': '', 'routing_key': 'cycle_queue', 'priority': 0, 'redelivered': None},
       'args': [5, 8], 'kwargs': {}, 'is_eager': False, 'callbacks': None, 'errbacks': None,
       'chain': None, 'chord': None, 'called_directly': False, '_protected': 1}>

    """

    logger.info(" request: num1 is %s num2 is %s task_id is %s " % (num1, num2, cycle_demo.request.id))

    res = dict()

    if isinstance(num1, int):
        r = recursion(num1)
        res[num1] = r

    if isinstance(num2, int):
        r = recursion(num2)
        res[num2] = r

    logger.info(" response: res is %s " % json.dumps(res, ensure_ascii=False, default=str))

    return res
