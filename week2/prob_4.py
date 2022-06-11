import sys

# Cache is a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library (e.g., collections.OrderedDict).
#       Implement the data structure yourself.

class Node:
  #双方向リストの各ノード(中身にurlとcontentsを持つ)
  def __init__(self, url, contents):
    self.url = url
    self.contents = contents

class DoubleLinkedList:
  #双方向リスト
  def __init__(self):
    #headの設定
    self.head = Node("","")
    self.head.next = self.head
    self.head.prev = self.head
  
  def insert(self, node):
    #先頭にノード追加
    node.next = self.head.next
    node.prev = self.head
    node.next.prev = node
    self.head.next = node

  def delete(self, node):
    #ノードを削除
    node.next.prev = node.prev
    node.prev.next = node.next
  
  def output_urls(self):
    #ノードに入っているURLをlistで返す
    node = self.head.next
    urls = []
    while (node is not self.head):
      urls.append(node.url)
      node = node.next
    return urls

class Cache:
  # Initializes the cache.
  # |n|: The size of the cache.
  def __init__(self, n):
    ###########################
    # Write your code here :) #
    ###########################
    self.max = n
    self.dict = dict() #辞書(key:url, value:node)
    self.list = DoubleLinkedList()

  # Access a page and update the cache so that it stores the most
  # recently accessed N pages. This needs to be done with mostly O(1).
  # |url|: The accessed URL
  # |contents|: The contents of the URL
  def access_page(self, url, contents):
    ###########################
    # Write your code here :) #
    ###########################

    node = self.dict.get(url)
    if node is not None: 
      #urlが辞書に存在するときリストの先頭にノード移動
      self.list.delete(node)
      self.list.insert(node)
    else:
      if(len(self.dict) == self.max):
        #cacheがmaxの時、古いノード(head.prev)をリストから削除、対応する要素を辞書から削除
        self.dict.pop(self.list.head.prev.url)
        self.list.delete(self.list.head.prev)
        
      #urlが辞書に存在しないとき辞書に追加、リストの先頭にノード追加
      self.dict[url] = Node(url, contents)
      self.list.insert(self.dict[url])


  # Return the URLs stored in the cache. The URLs are ordered
  # in the order in which the URLs are mostly recently accessed.
  def get_pages(self):
    ###########################
    # Write your code here :) #
    ###########################
    return self.list.output_urls()

# Does your code pass all test cases? :)
def cache_test():
  # Set the size of the cache to 4.
  cache = Cache(4)
  # Initially, no page is cached.
  equal(cache.get_pages(), [])
  # Access "a.com".
  cache.access_page("a.com", "AAA")
  # "a.com" is cached.
  equal(cache.get_pages(), ["a.com"])
  # Access "b.com".
  cache.access_page("b.com", "BBB")
  # The cache is updated to:
  #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["b.com", "a.com"])
  # Access "c.com".
  cache.access_page("c.com", "CCC")
  # The cache is updated to:
  #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["c.com", "b.com", "a.com"])
  # Access "d.com".
  cache.access_page("d.com", "DDD")
  # The cache is updated to:
  #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
  # Access "d.com" again.
  cache.access_page("d.com", "DDD")
  # The cache is updated to:
  #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
  # Access "a.com" again.
  cache.access_page("a.com", "AAA")
  # The cache is updated to:
  #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
  equal(cache.get_pages(), ["a.com", "d.com", "c.com", "b.com"])
  cache.access_page("c.com", "CCC")
  equal(cache.get_pages(), ["c.com", "a.com", "d.com", "b.com"])
  cache.access_page("a.com", "AAA")
  equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
  cache.access_page("a.com", "AAA")
  equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
  # Access "e.com".
  cache.access_page("e.com", "EEE")
  # The cache is full, so we need to remove the least recently accessed page "b.com".
  # The cache is updated to:
  #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
  equal(cache.get_pages(), ["e.com", "a.com", "c.com", "d.com"])
  # Access "f.com".
  cache.access_page("f.com", "FFF")
  # The cache is full, so we need to remove the least recently accessed page "c.com".
  # The cache is updated to:
  #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
  equal(cache.get_pages(), ["f.com", "e.com", "a.com", "c.com"])
  # Access "e.com".
  cache.access_page("e.com", "EEE")
  # The cache is updated to:
  #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
  equal(cache.get_pages(), ["e.com", "f.com", "a.com", "c.com"])
  # Access "a.com".
  cache.access_page("a.com", "AAA")
  # The cache is updated to:
  #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
  equal(cache.get_pages(), ["a.com", "e.com", "f.com", "c.com"])
  print("OK!")

# A helper function to check if the contents of the two lists is the same.
def equal(list1, list2):
  assert(list1 == list2)

if __name__ == "__main__":
  cache_test()
