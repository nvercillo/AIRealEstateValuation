import sys
import time
import heapq
from threading import Lock

sys.path.insert(0, "../../")  # import parent folder
from utils.abstract import AbstractBaseClass, abstractmethod


# implementation of thread safe heap
class Heap:
    class HeapNode(AbstractBaseClass):

        sortable_value = None
        node_lock = Lock()

        def __lt__(self, that):
            return self.sortable_value < that.sortable_value

    def __init__(self, capacity, HeapNodeClass):
        self.queue = [HeapNodeClass() for _ in range(capacity)]
        self.capacity = capacity
        self.heap_lock = Lock()

    def _find_avalible(self):
        # iterate linearly
        # self.queue will only psedo ordered

        if self.heap_lock.acquire(blocking=True, timeout=5):  # 1 second timeout
            for ele in self.queue:
                if ele.node_lock.acquire(blocking=False):  # non blocking
                    self.heap_lock.release()
                    return ele
            self.heap_lock.release()

        return None

    def _update_node_val(self, node: HeapNode, new_value) -> bool:
        if self.heap_lock.acquire(blocking=True, timeout=5):  # 1 second timeout

            # ensure that sortable value const during heapify
            node.sortable_value = new_value
            heapq.heapify(self.queue)
            node.node_lock.release()  # finally release ndoe lock at end of cycle
            self.heap_lock.release()

            return True
        else:
            return False
