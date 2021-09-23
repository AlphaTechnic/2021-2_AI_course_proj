###### Write Your Library Here ###########
from collections import deque
from heapq import *

INF = 10 ** 9
CACHE = dict()
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
    path = list()

    ####################### Write Your Code Here ################################
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
    while pq:
        _, cy, cx = heappop(pq)
        if (cy, cx) == (ey, ex):
            path = get_path(pre, sy, sx, ey, ex)
            break

        for ny, nx in maze.neighborPoints(cy, cx):
            new_dist = g[cy][cx] + 1
            if g[ny][nx] <= new_dist: continue  # edge cost가 모두 1

            g[ny][nx] = new_dist
            f[ny][nx] = g[ny][nx] + h[ny][nx]
            heappush(pq, (f[ny][nx], ny, nx))
            pre[ny][nx] = (cy, cx)

        f[cy][cx] = -1

    return path

    ############################################################################


# -------------------- Stage 02: Four circles - A* Algorithm  ------------------------ #


def delete_ele_in_arr(cy, cx, arr):
    new = list()
    for y, x in arr:
        if (y, x) != (cy, cx):
            new.append((y, x))
    return tuple(new)


def find_min_dist(oy, ox, others):
    min_val = INF
    pos_of_min_val = (-1, -1)
    for y, x in others:
        if manhatten_dist((oy, ox), (y, x)) < min_val:
            min_val = manhatten_dist((oy, ox), (y, x))
            pos_of_min_val = (y, x)
    return min_val, pos_of_min_val


def stage2_heuristic(cy, cx, end_points):
    vis = list()
    un_vis = list(end_points)

    tot = 0
    while len(un_vis) != 0:
        min_dist, pos_of_min_val = find_min_dist(cy, cx, un_vis)
        tot += min_dist

        vis.append(pos_of_min_val)
        un_vis = delete_ele_in_arr(pos_of_min_val[0], pos_of_min_val[1], un_vis)
        cy, cx = pos_of_min_val
    return tot


def get_path2(pre, init_state, final_state):
    path = deque()
    _, _, cy, cx, _ = cur_state = final_state
    path.appendleft((cy, cx))
    while cur_state != init_state:
        cur_state = pre[cur_state]
        _, _, cy, cx, _ = cur_state
        if path[0] == (cy, cx): continue

        path.appendleft((cy, cx))
    return list(path)


def update_g(g, ny, nx, cy, cx, goals):
    if (ny, nx, goals) not in g:
        return g[(cy, cx, goals)] + 1
    if g[(ny, nx, goals)] > g[(cy, cx, goals)] + 1:
        return g[(cy, cx, goals)] + 1
    return g[(ny, nx, goals)]


def update_h(h, ny, nx, goals):
    if (ny, nx, goals) not in h:
        return stage2_heuristic(ny, nx, goals)
    return h[(ny, nx, goals)]


def decrease_goals(goals, cy, cx, g, h, f, pre):
    old_goals = tuple([tup for tup in goals])
    goals = delete_ele_in_arr(cy, cx, old_goals)
    g[(cy, cx, goals)] = g[(cy, cx, old_goals)]
    h[(cy, cx, goals)] = h[(cy, cx, old_goals)]
    f[(cy, cx, goals)] = f[(cy, cx, old_goals)]
    old_state = (f[(cy, cx, old_goals)], g[(cy, cx, old_goals)], cy, cx, old_goals)
    new_state = (f[(cy, cx, goals)], g[(cy, cx, goals)], cy, cx, goals)
    pre[new_state] = old_state
    return goals, g, h, f, pre


def astar_four_circles(maze):
    """
    [문제 03] 제시된 stage2의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage2_heuristic function을 직접 정의하여 사용해야 한다.)
    """

    start_point = maze.startPoint()
    end_points = tuple(maze.circlePoints())

    path = []

    ####################### Write Your Code Here ################################
    sy, sx = start_point

    pre = dict()
    g = dict()
    h = dict()
    f = dict()

    #  h를 결정하는 인자 = (위치 요소) + (남은 목적지들이 어떤게 있는지)
    g[(sy, sx, end_points)] = 0
    h[(sy, sx, end_points)] = stage2_heuristic(sy, sx, end_points)
    f[(sy, sx, end_points)] = g[(sy, sx, end_points)] + h[(sy, sx, end_points)]

    pq = list()
    init_state = (f[(sy, sx, end_points)], g[(sy, sx, end_points)], sy, sx, end_points)
    heappush(pq, init_state)
    while pq:
        cur_state = heappop(pq)
        _, _, cy, cx, goals = cur_state
        if (cy, cx) in goals:
            # goals에서 원소 하나 제거 후, 상태 이어 받음
            goals, g, h, f, pre = decrease_goals(goals, cy, cx, g, h, f, pre)
            cur_state = (f[(cy, cx, goals)], g[(cy, cx, goals)], cy, cx, goals)

        if len(goals) == 0:
            path = get_path2(pre, init_state, cur_state)
            break

        for ny, nx in maze.neighborPoints(cy, cx):
            g[(ny, nx, goals)] = update_g(g, ny, nx, cy, cx, goals)
            h[(ny, nx, goals)] = update_h(h, ny, nx, goals)

            f[(ny, nx, goals)] = g[(ny, nx, goals)] + h[(ny, nx, goals)]
            nxt_state = (f[(ny, nx, goals)], g[(ny, nx, goals)], ny, nx, goals)
            if nxt_state in pq: continue
            if nxt_state in pre: continue

            heappush(pq, nxt_state)
            pre[nxt_state] = cur_state
    return path
    # return astar_many_circles(maze)

    ############################################################################


# -------------------- Stage 03: Many circles - A* Algorithm -------------------- #

def path_length_between(maze, start, end):
    if (start, end) in CACHE:
        return CACHE[(start, end)]

    path = list()

    sy, sx = start
    ey, ex = end
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
    while pq:
        _, cy, cx = heappop(pq)
        if (cy, cx) == (ey, ex):
            path = get_path(pre, sy, sx, ey, ex)
            break

        for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            ny, nx = cy + dy, cx + dx
            if not (0 <= ny < R and 0 <= nx < C): continue
            if maze.isWall(ny, nx): continue

            new_dist = g[cy][cx] + 1
            if g[ny][nx] <= new_dist: continue  # edge cost가 모두 1

            g[ny][nx] = new_dist
            f[ny][nx] = g[ny][nx] + h[ny][nx]
            heappush(pq, (f[ny][nx], ny, nx))
            pre[ny][nx] = (cy, cx)

        f[cy][cx] = -1

    CACHE[(start, end)] = CACHE[(end, start)] = len(path)
    return CACHE[(start, end)]


def find_min_cost_edge(maze, selected, un_selected):
    min_val = INF
    pos_of_min_val = (-1, -1)
    for vy, vx in selected:
        for unvy, unvx in un_selected:
            path_len = path_length_between(maze, (vy, vx), (unvy, unvx))
            if path_len < min_val:
                min_val = path_len
                pos_of_min_val = (unvy, unvx)
    return min_val, pos_of_min_val


def heuristic_using_mst_cost(maze, cy, cx, end_points):
    selected = list()
    un_selected = list(end_points)

    selected.append((cy, cx))
    mst_cost = 0
    while len(un_selected) != 0:
        min_dist, pos_of_min_val = find_min_cost_edge(maze, selected, un_selected)
        mst_cost += min_dist

        selected.append(pos_of_min_val)
        un_selected = delete_ele_in_arr(pos_of_min_val[0], pos_of_min_val[1], un_selected)
    return mst_cost


def update_h2(maze, h, ny, nx, goals):
    if (ny, nx, goals) not in h:
        return heuristic_using_mst_cost(maze, ny, nx, goals)
    return h[(ny, nx, goals)]


def astar_many_circles(maze):
    """
    [문제 04] 제시된 stage3의 맵 세가지를 A* Algorithm을 통해 최단 경로를 return하시오.(30점)
    (단 Heurstic Function은 위의 stage3_heuristic function을 직접 정의하여 사용해야 하고, minimum spanning tree
    알고리즘을 활용한 heuristic function이어야 한다.)
    """

    start_point = maze.startPoint()
    end_points = tuple(maze.circlePoints())

    path = []

    ####################### Write Your Code Here ################################
    print("Searching.. remaining goals :", len(end_points))
    sy, sx = start_point

    pre = dict()
    g = dict()
    h = dict()
    f = dict()

    #  h를 결정하는 인자 = (위치 요소) + (남은 목적지들이 어떤게 있는지)
    g[(sy, sx, end_points)] = 0
    h[(sy, sx, end_points)] = heuristic_using_mst_cost(maze, sy, sx, end_points)
    f[(sy, sx, end_points)] = g[(sy, sx, end_points)] + h[(sy, sx, end_points)]

    pq = list()
    init_state = (f[(sy, sx, end_points)], g[(sy, sx, end_points)], sy, sx, end_points)
    heappush(pq, init_state)
    while pq:
        cur_state = heappop(pq)
        _, _, cy, cx, goals = cur_state
        if (cy, cx) in goals:
            # goals에서 원소 하나 제거 후, 상태 이어 받음
            goals, g, h, f, pre = decrease_goals(goals, cy, cx, g, h, f, pre)
            cur_state = (f[(cy, cx, goals)], g[(cy, cx, goals)], cy, cx, goals)

        if len(goals) == 0:
            path = get_path2(pre, init_state, cur_state)
            break

        for ny, nx in maze.neighborPoints(cy, cx):
            g[(ny, nx, goals)] = update_g(g, ny, nx, cy, cx, goals)
            h[(ny, nx, goals)] = update_h2(maze, h, ny, nx, goals)

            f[(ny, nx, goals)] = g[(ny, nx, goals)] + h[(ny, nx, goals)]
            nxt_state = (f[(ny, nx, goals)], g[(ny, nx, goals)], ny, nx, goals)
            if nxt_state in pq: continue
            if nxt_state in pre: continue

            heappush(pq, nxt_state)
            pre[nxt_state] = cur_state

            if len(h) % 1000 == 0:
                print("Searching.. remaining goals :", len(goals))
    return path
    ############################################################################
