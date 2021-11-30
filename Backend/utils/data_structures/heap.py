import sys
import time
import heapq
from threading import Lock, Semaphore
from numpy import append

from sqlalchemy.orm import query

sys.path.insert(0, "../../")  # import parent folder
from utils.abstract import AbstractBaseClass, abstractmethod
from utils.utility_functions import safeprint


# implementation of thread safe heap
class Heap:
    class HeapNode(AbstractBaseClass):
        sortable_value = None
        node_lock = None
        init_failed = False

        @abstractmethod
        def _is_dead(self):
            pass

        def __lt__(self, that):
            return self.sortable_value < that.sortable_value

    def __init__(self, capacity, HeapNodeClass):
        self.queue = []
        for _ in range(capacity):
            node = HeapNodeClass()
            if not node.init_failed:
                self.queue.append(node)

        self.capacity = capacity
        self.items_available = Semaphore(self.capacity)
        self.heap_lock = Lock()
        self.not_all_used = Semaphore()
        self.HeapNodeClass = HeapNodeClass

    def _find_avalible(self):
        self.items_available.acquire()

        timeout = 2
        wait_delay = 0.1
        while timeout > 0:
            self.heap_lock.acquire(blocking=True)
            for ele in self.queue:
                if ele.node_lock.acquire(blocking=False):  # non blocking
                    safeprint(f"found available {id(ele)}!")
                    self.heap_lock.release()
                    return ele
            time.sleep(wait_delay)
            timeout -= wait_delay
            self.heap_lock.release()
            safeprint("searching...")

        safeprint("Unable to find available node during timeout period")
        return None

    def _update_node_val(self, node: HeapNode, new_value) -> bool:
        if self.heap_lock.acquire(blocking=True, timeout=1000):  # 1 second timeout
            # ensure that sortable value const during heapify
            node.sortable_value = new_value

            heapq.heapify(self.queue)
            node.node_lock.release()  # finally release ndoe lock at end of cycle
            self.heap_lock.release()
            self.items_available.release()
            return True
        else:
            node.node_lock.release()
            safeprint("DESIGN ISSUE, QUEUE LOCK TIMING OUT")
            return False

    def _purge_dead_nodes(self) -> bool:  # returns yes if true
        if self.heap_lock.acquire(blocking=False):  # 1 second timeout
            to_delete = []
            for i in range(len(self.queue)):
                if self.queue[i]._is_dead():
                    to_delete.append(i)

            safeprint("to_delete", to_delete)

            for i in range(len(to_delete) - 1, -1, -1):
                popped = self.queue.pop(to_delete[i])
                try:
                    popped.__exit__()
                except:
                    pass

            for i in range(len(to_delete)):
                node = self.HeapNodeClass()
                if not node.init_failed:
                    self.queue.append(node)

            heapq.heapify(self.queue)
            self.heap_lock.release()
            return True
        else:
            safeprint("Already in process of purging, skiping purge")
            return False
