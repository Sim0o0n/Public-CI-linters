import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10
MAX_TICKETS: int = 20
THRESHOLD: int = 3

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info(f'Seller {self.name} started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        while True:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} sold one; {TOTAL_TICKETS} left')

        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.uniform(0.1, 0.5))


class Director(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore, lock: threading.Lock) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.lock: threading.Lock = lock

    def run(self) -> None:
        global TOTAL_TICKETS
        while True:
            with self.lock:
                if TOTAL_TICKETS > 0 and TOTAL_TICKETS <= THRESHOLD:
                    additional_tickets = min(MAX_TICKETS - TOTAL_TICKETS, 6)
                    if additional_tickets > 0:
                        TOTAL_TICKETS += additional_tickets
                        logger.info(f'Director added {additional_tickets} tickets; {TOTAL_TICKETS} available now')

            if TOTAL_TICKETS >= MAX_TICKETS:
                logger.info("No more tickets can be added. Director finished work.")
                break
            time.sleep(1)


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore(3)
    lock: threading.Lock = threading.Lock()

    sellers: List[Seller] = [Seller(semaphore) for _ in range(3)]
    director: Director = Director(semaphore, lock)

    director.start()
    for seller in sellers:
        seller.start()

    for seller in sellers:
        seller.join()
    director.join()

    logger.info("All sellers and the director have finished.")


if __name__ == '__main__':
    main()

