# 参考文档： 
       https://www.celerycn.io/jian-jie
       http://v5blog.cn/pages/1281a5/
## celery4.0+ 不再支持windows
# Celery 分布式任务队列
## 1. Celery是什么
    
    1. Celery 是一款非常简单、灵活、可靠的分布式系统，可用于处理大量消息
    
    2. Celery 是一款消息队列工具，可用于处理实时数据以及任务调度
    
## 2. Celery作用：

    1. 实现异步任务（async task）和定时任务（crontab）
    
    2. 时间和速率的限制
        
        可以控制每秒/分钟/小时执行任务的次数，或者任务执行的最长时间
        
    3. 高可用
        
        如果出现丢失连接或连接失败，职程（Worker）和客户端会自动重试，并且中间人通过 主/主 主/从 的方式来进行提高可用性。
    
    4. 快速
        
        单个 Celery 进行每分钟可以处理数以百万的任务，而且延迟仅为亚毫秒
    
## 3. Celery架构：

![avatar](https://img-blog.csdn.net/20161213105123227?)

### Celery 主要包含以下几个模块：

    1. 任务模块 Task
    
        包含异步任务和定时任务。其中，异步任务通常在业务逻辑中被触发并发往任务队列，而定时任务由 Celery Beat 进程周期性地将任务发往任务队列。
    
    2. 消息中间件 Broker
    
        Broker，即为任务调度队列，接收任务生产者发来的消息（即任务），将任务存入队列。Celery 本身不提供队列服务，
        官方推荐使用 RabbitMQ 和 Redis 等
        
        RabbitMQ：
            
            Celery默认的中间人Broker， 功能比较齐全、稳定 
            
            配置：broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
        
        Redis：
            
            功能比较全，但是如果突然停止运行或断电会造成数据丢失
            
            配置：broker_url = 'redis://localhost:6379/0'
                  有密码：'redis://:password@hostname:port/db_number'
    
    3. 任务执行单元 Worker
    
        Worker 是执行任务的处理单元，它实时监控消息队列，获取队列中调度的任务，并执行它。
    
    4. 任务结果存储 Backend
    
        Backend 用于存储任务的执行结果，以供查询。同消息中间件一样，存储也可使用 RabbitMQ, Redis 和 MongoDB 等
        
        AMQP、 Redis
        Memcached
        SQLAlchemy、Django ORM
        Apache Cassandra、Elasticsearch
        
# Celery 使用
## 1. 异步任务：
    
    1.定义worker:tasks.py
        
        app = Celery('tasks', broker='redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379')
        @app.task
        def demo(x, y):pass
    
    2. 测试环境下运行worker
         
         celery -A tasks worker -l info
         
         tasks: 定义的worker所在的文件名称
         
    3. put 任务
        
        from tasks import demo
        
        1.立即执行
            
            result = demo.delay(10, 20)
            
            task_id = result.id                 # 任务id
            
            # ready() 可以检测是否已经处理完毕 结果：True 或 False
            
            result.ready()
        
        2.任务在未来的某一时刻执行
             
             result = demo.apply_async(args=[10, 20], countdown=60)
             
             task_id = result.id
             
    4.携带ID取结果
    
        from celery.result import AsyncResult
        from tasks import app
        
        res = AsyncResult(id="380d56b0-b869-480d-86d4-342d4e38272f", app=app)
        
        if res.successful():
            
            result = res.get()
            
            res.forget()            # 将结果删除

    
# 定时任务的配置：
    
    crontab()                                                           每分钟执行一次
    
    crontab(minute='*/15')                                              每15分钟执行一次。
    
    crontab(minute=0, hour=0)                                           每天午夜执行 00:00
    
    crontab(minute=0, hour='*/3')                                       每三个小时执行一次：午夜，凌晨3点，6am，9am，中午，3pm，6pm，9pm
    
    crontab(minute=0, hour='0,3,6,9,12,15,18,21')                       凌晨, 3点，6点的时候执行
    
    crontab(hour=7, minute=30, day_of_week=1)                           每周一早晨07:30执行  值为0-6, Sunday = 0 and Saturday = 6
                                                                        如果 day_of_week值为字符串，只能是周一至周五 mon-fri
                                                                
    crontab(minute='*/10', hour='3,17,22', day_of_week='thu,fri')       每十分钟执行一次，但仅在周四或周五的凌晨3-4点，
                                                                        下午5-6点以及晚上10-11点之间执行
                                                                        
    crontab(0, 0, day_of_month='2')                                     在每个月的第二天执行
    
    crontab(0, 0, day_of_month='2-30/2')                                在每个偶数天执行
    
    crontab(0, 0, day_of_month='1-7,15-21')                             在每月的第一和第三周执行
    
    crontab(0, 0, day_of_month='11', month_of_year='5')                 每年5月11日执行
    
    crontab(0, 0, month_of_year='*/3')                                  在每个季度的第一个月每天执行一次

    


# 实时Celery的web 监控工具 - Flower
## 1. 安装Flower
    
    pip install flower

## 2. 运行flower
    
    celery -A myCeleryProj.app flower
    
    指定端口：celery -A myCeleryProj.app flower --port=5555
    
# celery_schedule使用
## py文件

    __init__.py                           定义celery_app
    
    1. celery_config.py                   Celery配置文件
    
    2. async_schedule.py                  异步任务集
    
    3. cycle_schedule.py                  周期任务集 
    
    4. crontab_schedule.py                定时任务集
    
## 启动 Worker
    
    1. 测试环境启动 
        
        控制台打印信息：
            celery -A celery_schedule worker -l info
        
        控制台不打印信息：
            celery -A celery_schedule worker
    
    2. 生产环境中启动
    
        celery multi start w1 -A celery_schedule 
     
    3. 重启
        
        celery  multi restart w1 -A celery_schedule 
    
    4. 停止运行
        
        celery multi stop w1 -A celery_schedule 
        
        stop 命令是异步的，所以不会等待职程（Worker）关闭。可以通过 stopwait 命令进行停止运行，可以保证在退出之前完成当前正在执行的任务：
        
        celery multi stopwait w1 -A celery_schedule 

## 启动 Beat(定时任务)
    
     1. 测试环境启动
        
        celery -A celery_schedule worker -l info
        
        celery -A celery_schedule  beat  -l info
        
        启动 Worker 进程和 Beat 进程，也可以将它们放在一个命令中：
        
            celery  -A celery_schedule worker  -B -l info
  


# Celery并发方式

    并发方式： Prefork, Eventlet, gevent, threads/single threaded
    
    1. 默认使用进程池并发
        
        EX: celery worker -A celery_task.main --concurrency=4
        
    2. 使用协程方式并发
    
        EX:
            
            # 安装eventlet模块
                
                pip install eventlet

            # 启用 Eventlet 池
                
                celery -A celery_task.main worker -l info -P eventlet -c 1000

 # Question
 
 ## celery丢失任务
    
    修改配置如下：
        task_reject_on_worker_lost = True    # 作用是当worker进程意外退出时，task会被放回到队列中
        task_acks_late = True                # 作用是只有当worker完成了这个task时，任务才被标记为ack状态
        
## celery重复执行
    
    系统负载较高，消息队列里堵了太多东西的情况下，Celery容易出现重复执行一个Task，甚至不止一次的情况。
    
    Message超过1小时未被消费的情况下，Celery会重新发一个一模一样的（task_id相同）
    
    
    解决办法：
        
       1.  Celery Once 是利用 Redis 加锁来实现
           该类提供了任务去重的功能
           
       2. 增大未消费时间          
  
# 使用supervisor管理
    
    Supervisor是一个让进程可以在unix进程后台运行的python库
    
## 1.安装
    pip install supervisor
    
## 2.查看supervisor安装后的二进制可执行文件在哪里

    [root@localhost demoserver]# find / -name "*supervi*" -ls | grep python3 | grep bin
    17041457    4 -rwxr-xr-x   1 root     root          237 Sep  2 19:00 /usr/local/python3/bin/echo_supervisord_conf
    18649919    4 -rwxr-xr-x   1 root     root          242 Sep  2 19:00 /usr/local/python3/bin/supervisorctl
    17041458    4 -rwxr-xr-x   1 root     root          240 Sep  2 19:00 /usr/local/python3/bin/supervisord

## 3. 创建软连接
    
    将 supervisorctl、echo_supervisord_conf 和 supervisord 添加软链到执行目录下/usr/bin
    
    ln -s /usr/local/python3/bin/echo_supervisord_conf /usr/bin/echo_supervisord_conf
    ln -s /usr/local/python3/bin/supervisord /usr/bin/supervisord
    ln -s /usr/local/python3/bin/supervisorctl /usr/bin/supervisorctl
    
## 4. 创建配置文件
    
    celery配置所在目录：
        [root@localhost celery_schedule]# pwd
        /root/workfile/demoserver/celery_schedule
    
    1. 在celery_schedule目录下新建visord_conf文件夹，用来存放配置文件
    
        [root@localhost celery_schedule]# mkdir visord_conf
    
    2. 生成配置文件
    
        [root@localhost celery_schedule]# echo_supervisord_conf > visord_conf/supervisord.conf
        
    3. 修改配置文件
    
        1.开启管理服务页面：去掉以下代码前面的；
            ;[inet_http_server]         ; inet (TCP) server disabled by default
            ;port=127.0.0.1:9001        ; (ip_address:port specifier, *:port for all iface)
        
        2.开启supervisorctl：去掉serverurl前面的；
            [supervisorctl]
            serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket
            ;serverurl=http://127.0.0.1:9001 ; use an http:// url to specify an inet socket
        
        3.开启include：去掉；并修改files为files = *.ini
            ;[include]
            ;files = relative/directory/*.ini
            
## 5. 创建worker beat 配置文件
     
     日志文件需要提前创建/var/log/supervisor/celery_worker.log  /var/log/supervisor/celery_beat.log
     
     1.在visord_conf下新建
            
            [root@localhost visord_conf]# touch celery_wb.ini
     
     2.添加如下内容：
        [program:spv_cw]
        directory=/root/workfile/demoserver/
        command=/usr/local/python3/bin/celery -A celery_schedule worker
        stdout_logfile=/var/log/supervisor/celery_worker.log
        stderr_logfile=/var/log/supervisor/celery_worker.log
        autostart=true
        autorestart=true
        startsecs=10
        stopwatisecs=60
        priority=998
        
        [program:spv_bt]
        directory=/root/workfile/demoserver/
        command=/usr/local/python3/bin/celery -A celery_schedule  beat
        stdout_logfile=/var/log/supervisor/celery_beat.log
        stderr_logfile=/var/log/supervisor/celery_beat.log
        autostart=true
        autorestart=true
        startsecs=10
        stopwatisecs=60
        priority=998
        
        
 ## 6. 启动
 
     [root@localhost visord_conf]# supervisord -c supervisord.conf
     
     supervisorctl 命令查看supervisor的运行状态
        [root@localhost visord_conf]#  supervisorctl status 
    
     查看spv_cw：
          supervisorctl tail spv_cw # 查看最后的日志
          supervisorctl tail -f spv_cw # 持续
          supervisorctl restart spv_cw
          supervisorctl status spv_cw
          supervisorctl start spv_cw
          supervisorctl stop spv_cw

