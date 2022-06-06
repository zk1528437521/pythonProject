import sys
from celery import Celery

sys.path.append('..')
from lib import read_config

d = read_config('rabbitmq')
# 消息中间件引用的库
broker = 'amqp://%s:%s@%s:%s/%s' % (d.get('user'), d.get('password'),
                                    d.get('host'), d.get('port'),
                                    d.get('v_host'))
backend = 'rpc://'  # 运行结果引用的库
cel = Celery('celery_tasks',
             broker=broker,
             backend=backend,
             include=['celery_tasks.curb',
                      'celery_tasks.draw_picture.draw'
                      ])

# 时区
cel.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
cel.conf.enable_utc = False

# 定时任务
cel.conf.beat_schedule = {
    'add-every-1-hours': {
        'task': 'celery_tasks.draw_picture.draw.task',
        'schedule': 3600.0,
    },
}

