from .linked_list import LinkedList
from abc import ABC, abstractmethod
import sys

sys.path.insert(0, "../../")  # import parent folder
from utils.utility_functions import safeprint


class LRUCache(ABC):  # inheriting ABC makes class abstract
    @abstractmethod
    def __init__(self, capacity: int):
        pass

    @abstractmethod
    def get_type(self):
        pass

    def _initialize(self, capacity: int):
        self.cache = {}
        self.capacity = capacity
        self.ll = LinkedList()

    def get(self, key):
        if key not in self.cache:
            raise Exception(f"Key {key} not in {self.get_type()} Cache")

        node = self.cache[key]
        self.ll.remove(node)

        self.ll.append(node)  # replace MRU
        return node.data[1]  # data[1] is value

    def put(self, key, value) -> None:

        if key in self.cache:
            node = self.cache[key]
            node.data[1] = value
            self.ll.remove(node)

            self.ll.append(node)  # replace MRU

        else:
            if len(self.cache) + 1 > self.capacity:
                lru = self.ll.pop_head()  # pop LRU
                self.cache.pop(lru.data[0])  # [0] is key [1] is value

            new_node = LinkedList.Node(data=[key, value])
            self.ll.append(new_node)
            self.cache[key] = new_node

    def contains(self, key) -> bool:
        return key in self.cache

    def __str__(self):
        return f"<LRU:  {str(self.ll)}  >"

    def __repr__(self):
        return self.__str__

    def print(self):
        safeprint(self.__str__)
