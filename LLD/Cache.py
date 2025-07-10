from abc import ABC, abstractmethod

class AbstractCache(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def put(self, key, value):
        pass

    @abstractmethod
    def evict(self, key):
        pass

class EvictionPolicy(ABC):
    @abstractmethod
    def key_accessed(self, key):
        """Update the policy when a key is accessed."""
        pass

    @abstractmethod
    def evict_key(self):
        """Return the key to be evicted based on the policy."""
        pass

class Storage(ABC):
    @abstractmethod
    def get(self, key):
        pass
    
    @abstractmethod
    def put(self, key, value):
        pass

    @abstractmethod
    def remove(self, key):
        pass

    @abstractmethod
    def size(self):
        pass

class Cache(AbstractCache):
    def __init__(self, eviction_policy: EvictionPolicy, storage: Storage, capacity: int):
        self.capacity = capacity
        self.eviction_policy = eviction_policy
        self.storage = storage
    
    def get(self, key):
        value = self.storage.get(key)
        if value is not None:
            self.eviction_policy.key_accessed(key)
        return value
    
    def put(self, key, value):
        if self.storage.size() >= self.capacity:
            key_to_evict = self.eviction_policy.evict_key()
            self.storage.remove(key_to_evict)

        self.storage.put(key, value)
        self.eviction_policy.key_accessed(key)
    
    def evict(self, key):
        self.storage.remove(key)

class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

class LRU(EvictionPolicy):
    def __init__(self):
        self.lru = Node()
        self.mru = Node()
        self.lru.next = self.mru
        self.mru.prev = self.lru
        self.keys = {}

    def key_accessed(self, key):
        mru = self.mru.prev
        if key not in self.keys:
            node = Node(key)
        else:
            node = self.keys[key]
            node.prev.next = node.next
            node.next.prev = node.prev

        mru.next = node
        node.prev = mru
        node.next = self.mru
        self.mru.prev = node
        self.keys[key] = node
    
    def evict_key(self):
        lru = self.lru.next
        self.lru.next = lru.next
        lru.next.prev = self.lru
        evicted_key = lru.data
        lru.next = None
        lru.prev = None
        del self.keys[evicted_key]
        return evicted_key

class HashMap(Storage):
    def __init__(self):
        self.data = {}
    
    def get(self, key):
        return self.data.get(key)
    
    def put(self, key, value):
        self.data[key] = value
    
    def remove(self, key):
        if key in self.data:
            del self.data[key]

    def size(self):
        return len(self.data)

cache = Cache(LRU(), HashMap(), 3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)
print(cache.get("a")) # Accessing 'a' moves it to the most recently used
cache.put("d", 4)  # Evicts 'b' (Least Recently Used)
print(cache.get("b"))  # None, because 'b' was evicted
print(cache.get("a"))  # 1, because 'a' was recently used
