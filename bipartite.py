#!/usr/bin/env python3
"""bipartite: Bipartite check and maximum matching (Hopcroft-Karp)."""
from collections import deque
import sys

def is_bipartite(adj, n):
    color = [-1] * n
    for start in range(n):
        if color[start] != -1: continue
        color[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj.get(u, []):
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return False, None
    left = [i for i in range(n) if color[i] == 0]
    right = [i for i in range(n) if color[i] == 1]
    return True, (left, right)

def max_matching(adj, left, right):
    match_l = {u: None for u in left}
    match_r = {v: None for v in right}
    right_set = set(right)

    def bfs():
        dist = {}
        queue = deque()
        for u in left:
            if match_l[u] is None:
                dist[u] = 0
                queue.append(u)
        found = False
        while queue:
            u = queue.popleft()
            for v in adj.get(u, []):
                if v not in right_set: continue
                w = match_r[v]
                if w is None:
                    found = True
                elif w not in dist:
                    dist[w] = dist[u] + 1
                    queue.append(w)
        return found, dist

    def dfs(u, dist):
        for v in adj.get(u, []):
            if v not in right_set: continue
            w = match_r[v]
            if w is None or (w in dist and dist[w] == dist[u] + 1 and dfs(w, dist)):
                match_l[u] = v
                match_r[v] = u
                return True
        dist.pop(u, None)
        return False

    matching = 0
    while True:
        found, dist = bfs()
        if not found: break
        for u in left:
            if match_l[u] is None:
                if dfs(u, dist):
                    matching += 1
    return matching, {u: v for u, v in match_l.items() if v is not None}

def test():
    # Bipartite check
    adj = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}
    ok, parts = is_bipartite(adj, 4)
    assert ok
    # Odd cycle = not bipartite
    adj2 = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    ok2, _ = is_bipartite(adj2, 3)
    assert not ok2
    # Max matching: K3,3
    adj3 = {0: [3,4,5], 1: [3,4,5], 2: [3,4,5], 3: [0,1,2], 4: [0,1,2], 5: [0,1,2]}
    size, pairs = max_matching(adj3, [0,1,2], [3,4,5])
    assert size == 3
    # Simple matching
    adj4 = {0: [2], 1: [2,3], 2: [0,1], 3: [1]}
    size2, pairs2 = max_matching(adj4, [0,1], [2,3])
    assert size2 == 2
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: bipartite.py test")
