#!/usr/bin/env python3
"""bipartite - Bipartite graph check and maximum bipartite matching."""
import sys
from collections import defaultdict, deque

def is_bipartite(adj, nodes):
    color = {}
    for start in nodes:
        if start in color: continue
        q = deque([start])
        color[start] = 0
        while q:
            u = q.popleft()
            for v in adj.get(u, []):
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False, {}
    return True, color

def max_matching(adj, left, right):
    match_l = {}; match_r = {}
    def augment(u, visited):
        for v in adj.get(u, []):
            if v in visited: continue
            visited.add(v)
            if v not in match_r or augment(match_r[v], visited):
                match_l[u] = v; match_r[v] = u
                return True
        return False
    for u in left:
        augment(u, set())
    return match_l

def test():
    adj = {1: [4, 5], 2: [4], 3: [5, 6], 4: [1, 2], 5: [1, 3], 6: [3]}
    ok, colors = is_bipartite(adj, {1,2,3,4,5,6})
    assert ok
    adj2 = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    ok2, _ = is_bipartite(adj2, {1, 2, 3})
    assert not ok2  # triangle
    adj3 = {"a": ["x", "y"], "b": ["y"], "c": ["x", "z"]}
    m = max_matching(adj3, ["a", "b", "c"], ["x", "y", "z"])
    assert len(m) == 3  # perfect matching exists
    print("bipartite: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: bipartite.py --test")
