from .linked_list import LinkedList


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = {}
        self.capacity = capacity
        self.ll = LinkedList()

    def get(self, key: int) -> int:

        if key not in self.cache:
            return -1

        node = self.cache[key]
        self.ll.remove(node)

        self.ll.append(node)  # replace MRU
        return node.data[1]  # data[1] is value

    def put(self, key: int, value: int) -> None:

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
