import csv
from collections import deque

edgeFile = 'edges.csv'

def load_graph(filename):
    "建表"
    graph = {}
    
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 跳過標題
        
        for row in reader:
            start, end, dist = int(row[0]), int(row[1]), float(row[2])
            
            if start not in graph:
                graph[start] = []
            
            graph[start].append((end, dist)) # 有向圖
    
    return graph

def dfs(start, end):
    graph = load_graph(edgeFile)
    stack = [(start, [start], 0)]  # (當前節點, 路徑, 總距離) FILO
    visited = set()
    num_visited = 0
    
    while stack:
        node, path, total_dist = stack.pop() # 取出stack第一個
        
        if node in visited:
            continue
        
        visited.add(node)
        num_visited += 1
        
        if node == end:
            return path, round(total_dist, 3), num_visited
        
        for neighbor, cost in graph.get(node, []): # stack加入所有neighbor
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor], total_dist + cost))
    
    return [], 0, num_visited  # 無法到達時回傳空路徑

if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')