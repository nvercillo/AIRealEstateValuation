from .linked_list import LinkedList
from abc import ABC, abstractmethod


class LRUCache(ABC):  # inheriting ABC makes class abstract
    @abstractmethod
    def __init__(self, capacity: int):
        pass

    @abstractmethod
    def get_type(self):
        pass

    def initialize(self, capacity: int):
        self.cache = {}
        self.persistent_cache = {}
        self.capacity = capacity
        self.ll = LinkedList()

    def get(self, key):
        if key not in self.persistent_cache and key not in self.cache:
            raise Exception(f"Key {key} not in {self.get_type()} Cache")

        node = self.cache[key]
        self.ll.remove(node)

        self.ll.append(node)  # replace MRU
        return node.data[1]  # data[1] is value

    def pop(self) -> bool:  # success or failure

        lru = self.ll.pop_head()  # pop LRU
        if lru is None:
            return False

        self.cache.pop(lru.data[0])  # [0] is key [1] is value

        return True

    def put(self, key, value, persistent=False) -> None:

        if persistent:
            if self.size() + 1 > self.capacity:
                result = self.pop()

                if not result:
                    raise Exception("LRU cache is full, cannot add persistent data")

            self.persistent_cache[key] = value
        else:
            if key in self.cache:
                node = self.cache[key]
                node.data[1] = value
                self.ll.remove(node)

                self.ll.append(node)  # replace MRU

            else:
                if self.size() + 1 > self.capacity:
                    result = self.pop()

                    if not result:
                        raise Exception(
                            "LRU cache is full of persistent data, cannot update"
                        )

                new_node = LinkedList.Node(data=[key, value])
                self.ll.append(new_node)
                self.cache[key] = new_node

    def size(self) -> int:
        return len(self.cache) + len(self.persistent_cache)

    def contains(self, key) -> bool:
        return key in self.cache

    def __str__(self):
        return f"<LRU:  {str(self.ll)}  >"

    def __repr__(self):
        return self.__str__

    def print(self):
        print(self.__str__)
