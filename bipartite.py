#!/usr/bin/env python3
"""Bipartite graph matching (Hopcroft-Karp simplified)."""
import sys
from collections import defaultdict, deque

def is_bipartite(adj, n):
    color = [-1]*n
    for start in range(n):
        if color[start] != -1: continue
        color[start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False, []
    return True, color

def max_matching(adj_left, n_left, n_right):
    match_l = [-1]*n_left
    match_r = [-1]*n_right
    def dfs(u, visited):
        for v in adj_left[u]:
            if v in visited: continue
            visited.add(v)
            if match_r[v] == -1 or dfs(match_r[v], visited):
                match_l[u] = v
                match_r[v] = u
                return True
        return False
    matching = 0
    for u in range(n_left):
        if dfs(u, set()):
            matching += 1
    return matching, list(zip(range(n_left), match_l))

def test():
    adj = {0:[1,3], 1:[0,2], 2:[1,3], 3:[0,2]}
    ok, colors = is_bipartite(adj, 4)
    assert ok
    adj2 = {0:[1,2], 1:[0,2], 2:[0,1]}
    ok2, _ = is_bipartite(adj2, 3)
    assert not ok2  # triangle
    # Matching: 3 left, 3 right
    adj_l = {0:[0,1], 1:[1,2], 2:[0]}
    m, pairs = max_matching(adj_l, 3, 3)
    assert m == 3
    print("  bipartite: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Bipartite check + max matching")
