import threading
from .. import logger, work_q, redis_db
from app.docker import jobs


class StartThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.queue = q

    def run(self):
        while True:
            docker_run = self.queue.get()
            job_id = docker_run.pop['job_id']
            logger.debug(f'starting docker {docker_run}')
            contain_id = jobs.start(**docker_run)
            redis_db.set(job_id, contain_id)
            redis_db.expire(job_id, 3600)
            self.queue.task_done()


def allocate_worker(thread_num=10):
    """
    用来处理摄像头获取的信息，线程池默认共10个线程
    :return:
    """

    for threads_pool in range(thread_num):
        t = StartThread(work_q)
        t.setDaemon(True)
        t.start()
