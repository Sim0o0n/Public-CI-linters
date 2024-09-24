import logging
import random
import time
import threading
from queue import PriorityQueue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Task:
    def __init__(self, priority: int, function: callable, *args) -> None:
        self.priority = priority
        self.function = function
        self.args = args

    def run(self):
        logger.info(f'>running Task(piority={self.priority}).')
        time.sleep(self.function(*self.args))


class Producer(threading.Thread):
    def __init__(self, queue: PriorityQueue) -> None:
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        logger.info('Producer: Running')
        for priority in range(5):

            sleep_time = random.uniform(0.1, 1.0)
            task = Task(priority, lambda x: x, sleep_time)
            self.queue.put((priority, task))
        self.queue.put((5, None))
        logger.info('Producer: Done')

class Consumer(threading.Thread):
    def __init__(self, queue: PriorityQueue) -> None:
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        logger.info('Consumer: Running')
        while True:
            priority, task = self.queue.get()
            if task is None:
                break
            task.run()
            self.queue.task_done()
        logger.info('Consumer: Done')


def main() -> None:
    queue = PriorityQueue()
    producer = Producer(queue)
    consumer = Consumer(queue)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()


if __name__ == '__main__':
    main()
