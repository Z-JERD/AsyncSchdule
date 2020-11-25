# APScheduler定时任务框架
    
    pip install apscheduler
    
## 参考文档：https://my.oschina.net/u/4309507/blog/4486881  https://www.jianshu.com/p/4f5305e220f0

# APScheduler 四种组成部分：

    1. triggers（触发器）：
            
            触发器包含调度逻辑，每一个作业有它自己的触发器，用于决定接下来哪一个作业会运行，除了他们自己初始化配置外，触发器完全是无状态的。
        
    2. job stores（作业存储）：
           
           用来存储被调度的作业，默认的作业存储器是简单地把作业任务保存在内存中，其它作业存储器可以将任务作业保存到各种数据库中，
           支持MongoDB、Redis、SQLAlchemy存储方式。当对作业任务进行持久化存储的时候，作业的数据将被序列化，重新读取作业时在反序列化。
    
    3.executors（执行器）：
            
            执行器用来执行定时任务，只是将需要执行的任务放在新的线程或者线程池中运行。当作业任务完成时，执行器将会通知调度器。
            对于执行器，默认情况下选择ThreadPoolExecutor就可以了，但是如果涉及到一下特殊任务如比较消耗CPU的任务则可以选择ProcessPoolExecutor，
            当然根据根据实际需求可以同时使用两种执行器。
            
            
    4. schedulers（调度器）：
        
        调度器是将其它部分联系在一起，一般在应用程序中只有一个调度器，应用开发者不会直接操作触发器、任务存储以及执行器，
        相反调度器提供了处理的接口。通过调度器完成任务的存储以及执行器的配置操作，如可以添加。修改、移除任务作业。
        
# APScheduler 七种调度器：

    BlockingScheduler：适合于只在进程中运行单个任务的情况，通常在调度器是你唯一要运行的东西时使用。
    
    BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用。
    
    AsyncIOScheduler：适合于使用asyncio异步框架的情况
    
    GeventScheduler: 适合于使用gevent框架的情况
    
    TornadoScheduler: 适合于使用Tornado框架的应用
    
    TwistedScheduler: 适合使用Twisted框架的应用
    
    QtScheduler: 适合使用QT的情况
    
 # APScheduler提供了四种存储方式：
     MemoryJobStore
    
     sqlalchemy
    
     mongodb
    
     redis
     
# APScheduler提供了三种任务触发器

## 1.  date固定日期触发器：
    
        任务只运行一次，运行完毕自动清除；若错过指定运行时间，任务不会被创建
        
### 示例：
    
    import time
    from apscheduler.schedulers.blocking import BlockingScheduler
    
    def my_job():
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    
    sched = BlockingScheduler()
    ## 采用dete固定时间模式，在特定时间只执行一次
    sched.add_job(my_job, 'date', run_date='2019-01-01 00:00:00)
    sched.start()

## 2. interval  时间间隔触发器
    
    每隔多长时间触发一次
    
### 示例：
    import time
    from apscheduler.schedulers.blocking import BlockingScheduler
    
    def my_job():
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
   
    #### 采用interval固定间隔模式，每隔五秒只执行一次
    sched.add_job(my_job, 'interval', seconds=5)
    sched.start()

### 间隔调度，参数如下：

    weeks (int)  –  间隔几周 
    days (int)  –  间隔几天 
    hours (int)  –  间隔几小时 
    minutes (int)  –  间隔几分钟 
    seconds (int)  –  间隔多少秒 
    start_date (datetime|str)  –  开始日期 
    end_date (datetime|str)  –  结束日期 
    timezone (datetime.tzinfo|str)  –  时区

## 3. cron：固定时间点执行一次任务

### 示例：
    import time
    from apscheduler.schedulers.blocking import BlockingScheduler
    
    scheduler = BlockingScheduler()
    
    def everyday_crawler_job():
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    
    sched = BlockingScheduler()
   
    #每天早上八点半和十二点半各执行一次抓包程序
    sched.add_job(everyday_crawler_job, 'cron', hour='8, 12', minute='30')
    sched.start()
    
 ### 参数：
    
    (int|str) 表示参数既可以是int类型，也可以是str类型
    (datetime | str) 表示参数既可以是datetime类型，也可以是str类型
    
    year (int|str) – 4-digit year -（表示四位数的年份，如2008年）
    month (int|str) – month (1-12) -（表示取值范围为1-12月）
    day (int|str) – day of the (1-31) -（表示取值范围为1-31日）
    hour (int|str) – hour (0-23) - （表示取值范围为0-23时）
    minute (int|str) – minute (0-59) - （表示取值范围为0-59分）
    second (int|str) – second (0-59) - （表示取值范围为0-59秒）
    week (int|str) – ISO week (1-53) -（格里历2006年12月31日可以写成2006年-W52-7（扩展形式）或2006W527（紧凑形式））
    day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun) - （表示一周中的第几天，既可以用0-6表示也可以用其英语缩写表示）
    start_date (datetime|str) – earliest possible date/time to trigger on (inclusive) - （表示开始时间）
    end_date (datetime|str) – latest possible date/time to trigger on (inclusive) - （表示结束时间）
    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone) -（表示时区取值）
    
### 用法示例：
    #表示2017年3月22日17时19分07秒执行该程序
    sched.add_job(my_job, 'cron', year=2017,month = 3,day = 22,hour = 17,minute = 19,second = 07)
     
    #表示任务在6,7,8,11,12月份的第三个星期五的00:00,01:00,02:00,03:00 执行该程序
    sched.add_job(my_job, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
     
    #表示从星期一到星期五5:30（AM）直到2014-05-30 00:00:00
    sched.add_job(my_job(), 'cron', day_of_week='mon-fri', hour=5, minute=30,end_date='2014-05-30')
     
    #表示每5秒执行该程序一次，相当于interval 间隔调度中seconds = 5
    sched.add_job(my_job, 'cron',second = '*/5')
    
# add_job()

    在add_job()中添加参数：
    
    misfire_grace_time: 主要就是为了解决这个was missed by 这个报错，添加允许容错的时间，单位为：s
    
    coalesce：如果系统因某些原因没有执行任务，导致任务累计，为True则只运行最后一次，为False 则累计的任务全部跑一遍
