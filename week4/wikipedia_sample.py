from collections import deque

ans_pass = list() #答えの経路
visited = list() #訪問済みノード
parent_node = {} #key=子ノード,value=親ノードの辞書

def dfs(links, start, target):
  visited.append(start)
  boo = False

  if start == target: #見つかったらTrueを返す
    ans_pass.append(start)
    return True
  else:
    if start in links:
      for i in links[start]:
        try:
          if i not in visited: #訪問済みでなければ探索、再帰
            boo = dfs(links,i,target)
          
          if boo: #子がTrueのとき親を答えの経路に追加
            ans_pass.append(start) 
            return True
        except RecursionError: #再帰上限に達したらそれ以上の探索をstop
          return False
      return False   
    else:
      return False
    
  return None

def bfs(links, start, target):
  queue = deque()
  if start == target:
    ans_pass.append(start)
  else:
    queue.append(start)
    visited.append(start)
    
    while queue:
      key = queue.popleft() #先頭ノードをpop
      if key == target:
        #targetが見つかった時、targetの親ノードを辿って答えの経路を求める
        parent = parent_node[key]
        ans_pass.append(key)
        while parent != start:
          ans_pass.append(parent)
          parent = parent_node[parent]
        ans_pass.append(start)
        break
      else:
        if key in links:
          #keyの子ノードをqueueの後ろに追加
          for value in links[key]:
            if value not in visited:
              queue.append(value)
              visited.append(value)
              parent_node[value] = key #親ノードを記録

  return None


def main():

  with open('data/pages.txt', encoding="utf-8") as f:
    pages = {}
    for data in f.read().splitlines():
      page = data.split('\t')
      # page[0]: id, page[1]: title
      pages[page[0]] = page[1]
    
    print("pages finish")

  with open('data/links.txt', encoding="utf-8") as f:
    links = {}
    for data in f.read().splitlines():
      #print(data)
      link = data.split('\t')
      # link[0]: id (from), links[1]: id (to)
      if link[0] in links:
        links[link[0]].add(link[1])
      else:
        links[link[0]] = {link[1]}
      
      if int(link[0])%300000 == 0:
        print(str(int(link[0])//300000))
    print("links finish")

  start = 0
  target = 0
  #print(links)
  for k, v in pages.items():
    if v == 'Google':
      start = k
      print('Google', k)
    elif v == '渋谷':
      target = k
      print('渋谷', k)
  
  #dfs(links,start,target)
  bfs(links,start,target)
  
  if ans_pass:
    print(ans_pass)
  else:
    print("Not Found")


if __name__ == '__main__':
  main()