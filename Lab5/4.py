import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    K = int(data[idx]); N = int(data[idx+1]); idx += 2

    taxis = []
    for _ in range(K):
        x = int(data[idx]); y = int(data[idx+1]); idx += 2
        taxis.append((x, y))

    passengers = []
    for _ in range(N):
        px = int(data[idx]); py = int(data[idx+1])
        ti = int(data[idx+2]); Ti = int(data[idx+3]); wi = int(data[idx+4])
        idx += 5
        passengers.append((px, py, ti, Ti, wi))

    S = 0
    SINK = 1 + K + N
    V = K + N + 2
    graph = [[] for _ in range(V)]

    def add_edge(u, v, cap, cost):
        graph[u].append([v, cap, cost, len(graph[v])])
        graph[v].append([u, 0, -cost, len(graph[u]) - 1])

    for v in range(K):
        add_edge(S, 1 + v, 1, 0)
    for i in range(N):
        add_edge(1 + K + i, SINK, 1, 0)

    for v in range(K):
        tx, ty = taxis[v]
        for i in range(N):
            px, py, ti, Ti, wi = passengers[i]
            dx = tx - px; dy = ty - py
            if dx * dx + dy * dy <= Ti * Ti:        # arrival distance <= deadline
                add_edge(1 + v, 1 + K + i, 1, -wi)  # cost = -priority

    # Min-cost max-flow (SPFA / Bellman-Ford, handles negative costs)
    INF = float('inf')
    total_flow = 0
    total_cost = 0
    while True:
        dist = [INF] * V
        inq = [False] * V
        prevv = [-1] * V
        preve = [-1] * V
        dist[S] = 0
        dq = deque([S]); inq[S] = True
        while dq:
            u = dq.popleft(); inq[u] = False
            du = dist[u]
            for ei, e in enumerate(graph[u]):
                to, cap, cost, _ = e
                if cap > 0 and du + cost < dist[to]:
                    dist[to] = du + cost
                    prevv[to] = u; preve[to] = ei
                    if not inq[to]:
                        dq.append(to); inq[to] = True
        if dist[SINK] == INF:
            break
        # bottleneck (always 1 here, but kept general)
        d = INF; node = SINK
        while node != S:
            d = min(d, graph[prevv[node]][preve[node]][1])
            node = prevv[node]
        node = SINK
        while node != S:
            e = graph[prevv[node]][preve[node]]
            e[1] -= d
            graph[node][e[3]][1] += d
            node = prevv[node]
        total_flow += d
        total_cost += d * dist[SINK]

    print(total_flow, -total_cost)

main()