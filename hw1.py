from heapq import heappop, heappush, heapify
parent = {}
g = {}
x_moves = [(-1,7),  (0,5),  (1,7), (-1,5), (1,5), (-1,7), (0,5), (1,7)]
y_moves = [(-1,7), (-1,5), (-1,7), (0,5),  (0,5),  (1,7), (1,5), (1,7)]  
        

def inGrid(x,y):
    if (0<=x<H) and (0<=y<W):
        return True
    return False

def printPath(i):
    a = ''
    stack = []
    while i:
        stack.append(i)
        i = parent[i]
    while stack:
        i = stack.pop()
        a += str(i[1])+','+str(i[0])+' '
    return a

def printQueue(q):
    for i in q:
        g = i[0]
        x = i[1][0]
        y = i[1][1]
        print(x,y,grid[x][y],g,parent[i[1]])

def BFS(start, target):
    parent[start] = None
    g[start] = 0
    q = []
    q.append(start)

    visited = set()
    visited.add(start) 
    
    while q:
        current = q.pop(0)
        current_x = current[0]
        current_y = current[1]

        if current == target:
            return current
        
        for move in range(8):
            new_x = current_x + x_moves[move][0]
            new_y = current_y + y_moves[move][0]

            if inGrid(new_x,new_y):
                if abs(grid[new_x][new_y]-grid[current_x][current_y]) <= Z:
                    child = (new_x,new_y)
                    if child not in visited:
                        parent[child] = current
                        g[child] = g[current] + 1    
                        q.append(child)
                        visited.add(child) 
    return None

def UCS(start,target):
    parent[start] = None
    g[start] = 0
    
    q = []
    heappush(q, (g[start],start))

    closed = []
    
    visited = set()
    visited.add(start)

    while q:
        dist, current = heappop(q)
        current_x = current[0]
        current_y = current[1]

        if current == target:
            return current

        if current in closed:
            continue

        closed.append(current)

        for move in range(8):
            new_x = current_x + x_moves[move][0]
            new_y = current_y + y_moves[move][0]

            if inGrid(new_x,new_y):
                if abs(grid[new_x][new_y]-grid[current_x][current_y]) <= Z:
                    child = (new_x,new_y)
                    new_d = dist + x_moves[move][1] + y_moves[move][1]
                    if child not in visited or (child in visited and g[child] > new_d):
                        parent[child] = current
                        g[child] = new_d    
                        heappush(q,(g[child],child))
                        visited.add(child)
    return None

def findHeuristic(current, target):
    x1 = abs(current[0] - target[0])
    y1 = abs(current[1] - target[1])
    return min(x1,y1)*14 + abs(x1-y1)*10 + x1 + y1 - 10 + abs(grid[current[0]][current[1]]  -  grid[target[0]][target[1]]) + 10 - x1 - y1

def Astar(start,target):
    parent[start] = None
    g[start] = 0
    
    q = []
    h = g[start]
    heappush(q, (h,start))

    closed = []
    
    visited = set()
    visited.add(start)

    while q:
        h_current, current = heappop(q)
        current_x = current[0]
        current_y = current[1]

        if current == target:
            return current

        if current in closed:
            continue

        closed.append(current)


        for move in range(8):
            new_x = current_x + x_moves[move][0]
            new_y = current_y + y_moves[move][0]
            if inGrid(new_x,new_y):
                if abs(grid[new_x][new_y]-grid[current_x][current_y]) <= Z:
                    child = (new_x,new_y)
                    new_d = g[current] + x_moves[move][1] + y_moves[move][1] 
                    h = new_d + abs(grid[new_x][new_y]-grid[current_x][current_y])
                    if child not in visited or (child in visited and g[child] > new_d):
                        parent[child] = current
                        g[child] = new_d    
                        heappush(q,(h,child))
                        visited.add(child)
                    
    return None

for k in range(1,51):
    f = open('input' + str(k) + '.txt', 'r')
    if f.mode == 'r':
        f1 = f.read().split('\n')
        method = f1[0]

        cols = W = int(f1[1].split()[0])
        rows = H = int(f1[1].split()[1]) 

        start_y = int(f1[2].split()[0])
        start_x = int(f1[2].split()[1])
        start = (start_x,start_y)

        Z = int(f1[3])

        n_targets = int(f1[4])

        targets = []
        i = 5
        j = 0
        while j < (n_targets):
            targets.append((int(f1[i].split()[1]), int(f1[i].split()[0])))
            i += 1
            j += 1

        grid = []
        for j in range(rows):
            a = f1[i].split()
            i+=1
            grid.append(list(map(int, a)))
    f.close()
    ans = ''
    answer = ''
    for t in targets:
        if method == 'BFS':
            i = BFS(start,t)
            answer = printPath(i)
        if method == 'UCS':
            i = UCS(start,t)
            answer = printPath(i)
        if method == 'A*':
            i = Astar(start,t)
            answer = printPath(i)
        if answer:
            ans += answer + '\n'
        if not answer:
            ans += 'FAIL\n'
    f = open('my_output/output' + str(k) + '.txt','w+')
    f.write(ans[:-1])
    f.close()