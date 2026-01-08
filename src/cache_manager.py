from collections import OrderedDict
import time

class CacheManager:
    def __init__(self, max_entries=50):
        self.cache = OrderedDict()
        self.max_entries = max_entries
        print(f"CacheManager initialized with max_entries={max_entries}")

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]['response']
        return None

    def put(self, key, response):
        if len(self.cache) >= self.max_entries:
            self.cache.popitem(last=False)
        self.cache[key] = {"response": response, "timestamp": time.time()}
        self.cache.move_to_end(key)
    
    # ADD THIS DEBUG METHOD
    def debug_info(self):
        """Debug method to print cache contents"""
        print(f"\n=== CACHE DEBUG INFO ===")
        print(f"Total entries: {len(self.cache)}")
        print(f"Max entries: {self.max_entries}")
        for i, (key, value) in enumerate(self.cache.items(), 1):
            print(f"{i}. Key: '{key}'")
            print(f"   Response length: {len(value['response']) if value['response'] else 0} bytes")
            print(f"   Timestamp: {time.ctime(value['timestamp'])}")
        print("=======================\n")