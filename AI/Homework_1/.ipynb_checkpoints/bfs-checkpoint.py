import csv
from collections import deque

edgeFile = 'edges.csv'

def load_graph(filename):
    """ 讀取 CSV 檔案並建立鄰接表 """
    graph = {}
    distances = {}
    
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 跳過標題列
        
        for row in reader:
            start, end, dist = int(row[0]), int(row[1]), float(row[2])
            
            if start not in graph:
                graph[start] = []
            if end not in graph:
                graph[end] = []
            
            graph[start].append(end)
            # graph[end].append(start)  # 無向圖
            
            distances[(start, end)] = dist
            # distances[(end, start)] = dist  # 無向圖
    
    return graph, distances

def bfs(start, end):
    graph, distances = load_graph(edgeFile)
    queue = deque([(start, [start], 0)])  # (當前節點, 路徑, 總距離)
    visited = set()
    num_visited = 0
    
    while queue:
        node, path, total_dist = queue.popleft()
        
        if node in visited:
            continue
        
        visited.add(node)
        num_visited += 1
        
        if node == end:
            return path, total_dist, num_visited
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor], total_dist + distances[(node, neighbor)]))
    
    return [], 0, num_visited  # 無法到達時回傳空路徑

if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
