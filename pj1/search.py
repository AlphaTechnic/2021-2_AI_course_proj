###### Write Your Library Here ###########
from collections import deque
from heapq import *
import pprint



INF = 10 ** 9
#########################################


def search(maze, func):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_four_circles": astar_four_circles,
        "astar_many_circles": astar_many_circles
    }.get(func)(maze)


# -------------------- Stage 01: One circle - BFS Algorithm ------------------------ #
def get_path(pre, sy, sx, ey, ex):
    path = deque()
    path.append((ey, ex))
    while (ey, ex) != (sy, sx):
        ey, ex = pre[ey][ex]
        path.appendleft((ey, ex))
    return list(path)


def bfs(maze):
    """
    [문제 01] 제시된 stage1의 맵 세가지를 BFS Algorithm을 통해 최단 경로를 return하시오.(20점)
    """
    start_point = maze.startPoint()

    ####################### Write Your Code Here ################################
    ey, ex = maze.circlePoints()[0]
    R, C = maze.getDimensions()

    que = deque()
    vis = [[False for _ in range(C)] for _ in range(R)]
    pre = [[(-1, -1) for _ in range(C)] for _ in range(R)]
    sy, sx = start_point

    que.append((sy, sx))
    vis[sy][sx] = True
    while que:
        cy, cx = que.popleft()
        for ny, nx in maze.neighborPoints(cy, cx):
            if vis[ny][nx]: continue
            if maze.isWall(ny, nx): continue

            que.append((ny, nx))
            pre[ny][nx] = (cy, cx)
            vis[ny][nx] = True
            if (ny, nx) == (ey, ex):
                break

    path = get_path(pre, sy, sx, ey, ex)

    return path

    ############################################################################


class Node:
    def __init__(self, parent, location):
        self.parent = parent
        self.location = location  # 현재 노드

        self.obj = []

        # F = G+H
        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.location == other.location and str(self.obj) == str(other.obj)

    def __le__(self, other):
        return self.g + self.h <= other.g + other.h

    def __lt__(self, other):
        return self.g + self.h < other.g + other.h

    def __gt__(self, other):
        return self.g + self.h > other.g + other.h

    def __ge__(self, other):
        return self.g + self.h >= other.g + other.h


# -------------------- Stage 01: One circle - A* Algorithm ------------------------ #

def manhatten_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_nearest(f):
    R = len(f)
    C = len(f[0])
    min_val = INF
    ans_y, ans_x = -1, -1
    for r in range(R):
        for c in range(C):
            if min_val > f[r][c] >= 0:
                min_val = f[r][c]
                ans_y, ans_x = r, c
    return ans_y, ans_x


def astar(maze):
    """
    [문제 02] 제시된 stage1의 맵 세가지를 A* Algorithm을 통해 최단경로를 return하시오.(20점)
    (Heuristic Function은 위에서 정의한 manhatten_dist function을 사용할 것.)
    """
    start_point = maze.startPoint()
    end_point = maze.circlePoints()[0]

    ####################### Write Your Code Here ################################
    board = maze.mazeRaw
    sy, sx = start_point
    ey, ex = end_point
    R, C = maze.getDimensions()

    # heuristic function 정의
    h = [[0 for _ in range(C)] for _ in range(R)]
    for r in range(R):
        for c in range(C):
            if not maze.isWall(r, c):
                h_val = manhatten_dist((r, c), (ey, ex))
                h[r][c] = h_val

    g = [[INF for _ in range(C)] for _ in range(R)]
    g[sy][sx] = 0
    f = [[INF for _ in range(C)] for _ in range(R)]
    f[sy][sx] = g[sy][sx] + h[sy][sx]

    pre = [[(-1, -1) for _ in range(C)] for _ in range(R)]
    pq = list()
    heappush(pq, (f[sy][sx], sy, sx))
    for _ in range(R * C):
        _, cy, cx = heappop(pq)
        if (cy, cx) == (ey, ex):
            path = get_path(pre, sy, sx, ey, ex)
            break

        for ny, nx in maze.neighborPoints(cy, cx):
            if g[ny][nx] > g[cy][cx] + 1:  # edge cost가 1
                g[ny][nx] = g[cy][cx] + 1
                f[ny][nx] = g[ny][nx] + h[ny][nx]
                heappush(pq, (f[ny][nx], ny, nx))
                pre[ny][nx] = (cy, cx)
        f[cy][cx] = -1

    return path

    ############################################################################


# -------------------- Stage 02: Four circles - A* Algorithm  ------------------------ #



def stage2_heuristic():
    pass


def astar_four_circles(maze):
    """
    [문제 03] 제시된 stage2의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage2_heuristic function을 직접 정의하여 사용해야 한다.)
    """

    end_points=maze.circlePoints()
    end_points.sort()

    path=[]

    ####################### Write Your Code Here ################################


















    return path

    ############################################################################



# -------------------- Stage 03: Many circles - A* Algorithm -------------------- #

def mst(objectives, edges):

    cost_sum=0
    ####################### Write Your Code Here ################################













    return cost_sum

    ############################################################################


def stage3_heuristic():
    pass


def astar_many_circles(maze):
    """
    [문제 04] 제시된 stage3의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage3_heuristic function을 직접 정의하여 사용해야 하고, minimum spanning tree
    알고리즘을 활용한 heuristic function이어야 한다.)
    """

    end_points= maze.circlePoints()
    end_points.sort()

    path=[]

    ####################### Write Your Code Here ################################





















    return path

    ############################################################################
