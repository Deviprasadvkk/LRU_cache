class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None  # Pointer to the previous node
        self.next = None  # Pointer to the next node
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # Hash Map: {key: Node}
        
        # Dummy nodes to mark the boundaries
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Removes a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node):
        """Adds a new node right after the head (Most Recently Used)."""
        temp = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = temp
        temp.prev = node
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            # It's been used, so move it to the front (MRU)
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key, value):
        # If the key already exists, delete the old node first
        if key in self.cache:
            self._remove(self.cache[key])
        
        # Create a new node and add it to the front
        new_node = Node(key, value)
        self._add(new_node)
        self.cache[key] = new_node
        
        # If we are over capacity, throw away the oldest (at the tail)
        if len(self.cache) > self.capacity:
            oldest = self.tail.prev
            self._remove(oldest)
            del self.cache[oldest.key]
# --- Test Script ---
my_cache = LRUCache(2)  # Create a tray that holds only 2 files

my_cache.put(1, "A")    # Tray: [A]
my_cache.put(2, "B")    # Tray: [B, A]
print(f"Value for key 1: {my_cache.get(1)}") # Tray: [A, B] (1 is now newest)

my_cache.put(3, "C")    # Tray: [C, A]. (B was the oldest, so it was evicted!)

print(f"Is 2 still there? {my_cache.get(2)}") # Should print -1 (not found)
print(f"Is 3 there? {my_cache.get(3)}")       # Should print 'C'
