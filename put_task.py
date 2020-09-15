from celery.result import AsyncResult

from celery_schedule import async_schedule, schedule_task


class CeleryDemo(object):
    """调用异步任务示例"""

    @staticmethod
    def get_result(task_id):
        """去存储中取结果 """
        async_res = AsyncResult(id=task_id, app=schedule_task)

        if async_res.state == "PENDING":
            """job did not start yet"""
            response = {
                "state": async_res.state,
                "status": "Pending...",
                "progress": "0%",
                "result": None
            }

        elif async_res.state != "FAILURE":
            progress = int((async_res.info.get('current', 0) / async_res.info.get('total', 1)) * 100)
            progress = "%s" % progress + r"%"

            response = {
                "state": async_res.state,
                "status": async_res.info.get('status', ''),
                "progress": progress,
                "result": None
            }

            if async_res.successful():
                response['result'] = async_res.get()
                response["progress"] = "100%"

        else:
            """something went wrong in the background job"""
            response = {
                "state": async_res.state,
                "progress": "100%",
                "status": str(async_res.info),              # this is the exception raised
                "result": None
            }

        return response

    @staticmethod
    def put_task(num):
        """通过cerely的配置文件的操作celery_app中的任务task1,task2"""
        task_obj = async_schedule.async_demo.delay(num)

        return {
            "task_id": task_obj.id
        }


if __name__ == "__main__":
    celery_obj = CeleryDemo()
    ret = celery_obj.put_task(20)
    print(ret)


