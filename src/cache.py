from collections import OrderedDict

lruCache = OrderedDict()


# Cache Frame capacity

config = {
	
	'capacity': 10,
}

# Checking for the cache file

def isCached(file_name: str):
	if file_name in lruCache:
		return True
	else:
		return False

# Returing the cache file name string

def getCachedFile(file_name: str) -> str:
	lruCache.move_to_end(file_name)
	return lruCache[file_name]

# Putting the cache file into lruCache dict

def putCacheFile(file_name: str, cacheFile: str):
	lruCache[file_name] = cacheFile
	lruCache.move_to_end(file_name)
	if len(lruCache) > config['capacity']:
		lruCache.popitem(last = False)


# print(lruCache) -> Used for testing purpose
