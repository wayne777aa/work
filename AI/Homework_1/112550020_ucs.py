import csv
import heapq

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

def ucs(start, end):
    graph = load_graph(edgeFile)
    pq = [(0, start, [start])]  # (總距離(key), 當前節點, 路徑)
    visited = {}
    num_visited = 0
    
    while pq:
        total_dist, node, path = heapq.heappop(pq) # 取出第一個
        
        if node in visited and visited[node] <= total_dist: # 沒走過或是原先的近
            continue
        
        visited[node] = total_dist
        num_visited += 1
        
        if node == end:
            return path, round(total_dist, 3), num_visited
        
        for neighbor, cost in graph.get(node, []): # priority queue更新所有neighbor
            new_cost = total_dist + cost
            if neighbor not in visited or new_cost < visited[neighbor]:
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))
    
    return [], 0, num_visited  # 無法到達時回傳空路徑

if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
