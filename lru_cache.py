import threading
from fastapi import FastAPI, HTTPException
from typing import Optional

# 1. The "Surgery" Tools: Node and Doubly Linked List
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # The Hash Map for O(1) lookups
        self.lock = threading.Lock()  # THE LOCK: Ensures thread safety
        
        # Dummy nodes to make "stitching" the list easier
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """The Pointer Surgery: Removing a node from the middle"""
        prev = node.prev
        new_next = node.next
        prev.next = new_next
        new_next.prev = prev

    def _add(self, node):
        """The Pointer Surgery: Adding a node to the very front (MRU)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: str):
        with self.lock:  # Enter the Kitchen - Only one person allowed!
            if key in self.cache:
                node = self.cache[key]
                self._remove(node)
                self._add(node)
                return node.value
            return None

    def put(self, key: str, value: str):
        with self.lock:
            if key in self.cache:
                self._remove(self.cache[key])
            
            new_node = Node(key, value)
            self._add(new_node)
            self.cache[key] = new_node
            
            if len(self.cache) > self.capacity:
                # Eviction: Snipping the 'Least Recently Used' node (at the tail)
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

# 2. The API: The "Waiter" serving the Cache
app = FastAPI()
my_micro_redis = LRUCache(capacity=100)

@app.get("/get/{key}")
async def get_item(key: str):
    result = my_micro_redis.get(key)
    if result is None:
        # Step 7: Cache Miss - In a real app, you'd check the DB here!
        raise HTTPException(status_code=404, detail="Key not found in Cache")
    return {"key": key, "value": result, "status": "Cache Hit"}

@app.post("/set")
async def set_item(key: str, value: str):
    my_micro_redis.put(key, value)
    return {"message": f"Key '{key}' stored in Micro-Redis"}