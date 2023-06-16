from typing import Optional, List

class RAM:
    def __init__(self, size: int):
        self.size: int = size
        self.memory: List[int] = [0] * size
        
    def read(self, address: int) -> int:
        return self.memory[address]
    
    def write(self, address: int, data: int) -> None:
        self.memory[address] = data

class CacheLine:
    def __init__(self, block_size: int) -> None:
        self.valid: bool = False
        self.tag: Optional[int] = None
        self.data: List[int] = [0] * block_size
        
    def set_data(self, tag: int, data: List[int]) -> None:
        self.valid = True
        self.tag = tag
        self.data = data
        
    def get_data(self) -> List[int]:
        return self.data
        
    def is_valid(self) -> bool:
        return self.valid
        
    def get_tag(self) -> Optional[int]:
        return self.tag

class FullyAssociativeCache:
    def __init__(self, num_cache_lines: int, block_size: int, ram: RAM):
        self.num_cache_lines = num_cache_lines
        self.block_size = block_size
        self.cache = [CacheLine(block_size) for _ in range(num_cache_lines)]
        self.ram = ram
        
    def get_block_index(self, address: int) -> int:
        return address // self.block_size
        
    def get_tag(self, address: int) -> int:
        return address // (self.block_size * self.num_cache_lines)
    
    def get_offset(self, address: int) -> int:
        return address % self.block_size
    
    def read(self, address: int) -> int:
        block_index = self.get_block_index(address)
        tag = self.get_tag(address)
        offset = self.get_offset(address)
        
        for cache_line in self.cache:
            if cache_line.is_valid() and cache_line.get_tag() == tag:
                print("Cache hit")
                return cache_line.get_data()[offset]
            
        print("Cache miss")
        data = [self.ram.read(i) for i in range(block_index * self.block_size, 
                                                (block_index + 1) * self.block_size)]
        evict_index = self._get_evict_index()
        self.cache[evict_index].set_data(tag, data)
        return data[offset]
    
    def _get_evict_index(self) -> int:
        for i, cache_line in enumerate(self.cache):
            if not cache_line.is_valid():
                return i
        return 0


ram = RAM(2048)
cache = FullyAssociativeCache(num_cache_lines=16, block_size=4, ram=ram)

for i in range(2048):
    ram.write(i, i)

for i in range(0, 2048, 11):
    print(cache.read(i))