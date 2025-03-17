import csv
import heapq
edgeFile = 'edges.csv'
heuristicFile = 'heuristic_values.csv'

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

def load_heuristics(filename):
    """ 讀取啟發式函數值 """
    heuristics = {}
    
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # 讀取標題列，包含所有終點 ID
        targets = [int(target) for target in headers[1:]]  # 提取終點節點 ID
        
        for row in reader:
            node = int(row[0])
            heuristics[node] = {targets[i]: float(row[i+1]) for i in range(len(targets))}
    
    return heuristics

def astar(start, end):
    graph = load_graph(edgeFile)
    heuristics = load_heuristics(heuristicFile)
    pq = [(heuristics.get(start, 0), start, [start], 0)]  # (f值(key), 當前節點, 路徑, 總距離)
    visited = {}
    num_visited = 0
    
    while pq:
        _, node, path, total_dist = heapq.heappop(pq) # 取出第一個
        
        if node in visited and visited[node] <= total_dist: # 沒走過或是原先的近
            continue
        
        visited[node] = total_dist
        num_visited += 1
        
        if node == end:
            return path, round(total_dist, 3), num_visited
        
        for neighbor, cost in graph.get(node, []): # priority queue更新所有neighbor
            new_cost = total_dist + cost
            f_value = new_cost + heuristics.get(neighbor, {}).get(end, 0) # 找到neighbor, 回傳能到的點(沒找到回傳空字串), 從中找到end, 回傳hueristic(沒找到回傳0)
            if neighbor not in visited or new_cost < visited[neighbor]:
                heapq.heappush(pq, (f_value, neighbor, path + [neighbor], new_cost))
    
    return [], 0, num_visited  # 無法到達時回傳空路徑

if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
