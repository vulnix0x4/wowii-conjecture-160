#!/usr/bin/env python3
"""Constructive verifier for the source-corrected WOWII Conjecture 160.

The theorem verified is
    L_s(G) >= lambda_max(G) + T_max(G) * chi_C4_free(G),
where L_s is the maximum number of leaves in a spanning tree,
lambda(v) = alpha(G[N(v)]), T(v) is the number of triangles incident
with v, and chi_C4_free is 1 iff G contains no 4-cycle as a subgraph.

The script does not optimize L_s.  It implements the spanning-tree
construction from the proof and checks that the constructed tree already
has enough leaves.
"""
from __future__ import annotations

import argparse
import itertools
import random
from collections import Counter
from typing import Hashable, Iterable

import networkx as nx

Vertex = Hashable


def maximum_independent_subset(G: nx.Graph, vertices: Iterable[Vertex]) -> set[Vertex]:
    vertices = list(vertices)
    for k in range(len(vertices), -1, -1):
        for subset in itertools.combinations(vertices, k):
            if all(not G.has_edge(u, v) for u, v in itertools.combinations(subset, 2)):
                return set(subset)
    raise AssertionError("unreachable")


def local_independence_values(G: nx.Graph) -> dict[Vertex, int]:
    return {
        v: len(maximum_independent_subset(G, G.neighbors(v)))
        for v in G.nodes
    }


def triangle_values(G: nx.Graph) -> dict[Vertex, int]:
    # Every edge in G[N(v)] corresponds to exactly one triangle through v.
    return {v: G.subgraph(list(G.neighbors(v))).number_of_edges() for v in G.nodes}


def is_c4_free(G: nx.Graph) -> bool:
    # A simple graph contains a C4 iff some pair of vertices has at least
    # two common neighbors.  Chords are allowed, matching the source statement.
    for u, v in itertools.combinations(G.nodes, 2):
        if len(set(G.neighbors(u)).intersection(G.neighbors(v))) >= 2:
            return False
    return True


def leaf_count(T: nx.Graph) -> int:
    if T.number_of_nodes() == 1:
        return 1
    return sum(degree == 1 for _, degree in T.degree())


def extend_tree_without_losing_leaves(G: nx.Graph, T: nx.Graph) -> nx.Graph:
    """Extend a nonempty tree subgraph T to a spanning tree of connected G."""
    T = T.copy()
    if T.number_of_nodes() == 0:
        raise ValueError("T must be nonempty")
    if not nx.is_tree(T):
        raise ValueError("T must be a tree")

    while T.number_of_nodes() < G.number_of_nodes():
        current = set(T.nodes)
        boundary_edge = next(
            (
                (u, v)
                for u in current
                for v in G.neighbors(u)
                if v not in current
            ),
            None,
        )
        if boundary_edge is None:
            raise ValueError("G is not connected")
        before = leaf_count(T)
        T.add_edge(*boundary_edge)
        after = leaf_count(T)
        assert after >= before

    assert nx.is_tree(T)
    assert set(T.nodes) == set(G.nodes)
    return T


def full_star(G: nx.Graph, center: Vertex) -> nx.Graph:
    T = nx.Graph()
    T.add_node(center)
    T.add_edges_from((center, u) for u in G.neighbors(center))
    return T


def construct_spanning_tree(G: nx.Graph) -> tuple[nx.Graph, dict[str, object]]:
    if G.number_of_nodes() < 2 or not nx.is_connected(G):
        raise ValueError("G must be a nontrivial connected simple graph")

    lam = local_independence_values(G)
    triangles = triangle_values(G)
    x = max(G.nodes, key=lambda v: lam[v])
    y = max(G.nodes, key=lambda v: triangles[v])
    Lambda = lam[x]
    Tau = triangles[y]
    c4_free = is_c4_free(G)

    info: dict[str, object] = {
        "x": x,
        "y": y,
        "lambda_max": Lambda,
        "T_max": Tau,
        "c4_free": c4_free,
    }

    if not c4_free:
        A = maximum_independent_subset(G, G.neighbors(x))
        T = nx.Graph()
        T.add_node(x)
        T.add_edges_from((x, a) for a in A)
        info["case"] = "contains C4: independent-neighborhood star"
        return extend_tree_without_losing_leaves(G, T), info

    tx = triangles[x]
    lambda_y = lam[y]
    info.update({"T_x": tx, "lambda_y": lambda_y})

    if Tau == 0:
        info["case"] = "C4-free, T_max=0: full star at x"
        return extend_tree_without_losing_leaves(G, full_star(G, x)), info

    if x == y:
        info["case"] = "C4-free, same vertex maximizes lambda and T: full star"
        return extend_tree_without_losing_leaves(G, full_star(G, x)), info

    distance = nx.shortest_path_length(G, x, y)
    info["distance_xy"] = distance

    if distance >= 2:
        path = nx.shortest_path(G, x, y)
        if tx == 0 and lambda_y == 1:
            p = path[-2]
            neighbors_y = list(G.neighbors(y))
            assert len(neighbors_y) == 2
            z = neighbors_y[0] if neighbors_y[1] == p else neighbors_y[1]
            assert G.has_edge(p, z)

            T = full_star(G, x)
            T.add_edges_from(zip(path, path[1:]))
            T.add_edge(p, z)
            assert nx.is_tree(T)
            info["case"] = "C4-free, distance>=2: exceptional degree-2 triangle"
            return extend_tree_without_losing_leaves(G, T), info

        T = full_star(G, x)
        T.add_edges_from((y, v) for v in G.neighbors(y))
        T.add_edges_from(zip(path, path[1:]))
        assert nx.is_tree(T)
        info["case"] = "C4-free, distance>=2: two stars joined by geodesic"
        return extend_tree_without_losing_leaves(G, T), info

    # x and y are adjacent.
    common = set(G.neighbors(x)).intersection(G.neighbors(y))
    assert len(common) <= 1

    if not common:
        T = full_star(G, x)
        T.add_edges_from((y, v) for v in G.neighbors(y))
        assert nx.is_tree(T)
        info["case"] = "C4-free, adjacent with no common neighbor: double-star"
        return extend_tree_without_losing_leaves(G, T), info

    z = next(iter(common))
    if tx >= Tau:
        info["case"] = "C4-free, adjacent triangle and T(x)=T_max: full star at x"
        return extend_tree_without_losing_leaves(G, full_star(G, x)), info

    T = full_star(G, x)
    T.add_edges_from((y, v) for v in G.neighbors(y) if v != z)
    assert nx.is_tree(T)
    info["case"] = "C4-free, adjacent triangle: modified double-star"
    return extend_tree_without_losing_leaves(G, T), info


def verify_graph(G: nx.Graph) -> dict[str, object]:
    T, info = construct_spanning_tree(G)
    rhs = int(info["lambda_max"]) + int(info["T_max"]) * int(bool(info["c4_free"]))
    leaves = leaf_count(T)

    assert nx.is_tree(T)
    assert set(T.nodes) == set(G.nodes)
    assert all(G.has_edge(u, v) for u, v in T.edges)
    assert leaves >= rhs

    info["leaves_in_constructed_tree"] = leaves
    info["required_rhs"] = rhs
    return info


def exhaustive_atlas_check() -> Counter[str]:
    cases: Counter[str] = Counter()
    tested = 0
    for G in nx.graph_atlas_g():
        if G.number_of_nodes() >= 2 and nx.is_connected(G):
            info = verify_graph(G)
            cases[str(info["case"])] += 1
            tested += 1
    assert tested == 995, tested
    print(f"Exhaustive atlas check passed: {tested} connected unlabeled graphs (orders 2 through 7).")
    return cases


def deterministic_random_check(samples: int, max_order: int, seed: int) -> Counter[str]:
    rng = random.Random(seed)
    cases: Counter[str] = Counter()
    tested = 0
    for _ in range(samples):
        n = rng.randint(2, max_order)
        p = rng.uniform(max(0.08, 1.5 / n), min(0.85, 6.0 / n + 0.15))
        for _attempt in range(200):
            G = nx.gnp_random_graph(n, p, seed=rng.randrange(2**32))
            if nx.is_connected(G):
                break
        else:
            continue
        info = verify_graph(G)
        cases[str(info["case"])] += 1
        tested += 1
    print(f"Deterministic random check passed: {tested} connected graphs (orders up to {max_order}).")
    return cases


def parse_graph6(value: str) -> nx.Graph:
    return nx.from_graph6_bytes(value.strip().encode("ascii"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph6", help="verify one graph given by a graph6 string")
    parser.add_argument("--random-samples", type=int, default=5000)
    parser.add_argument("--max-order", type=int, default=20)
    parser.add_argument("--seed", type=int, default=160)
    args = parser.parse_args()

    if args.graph6:
        G = parse_graph6(args.graph6)
        info = verify_graph(G)
        print(info)
        return

    cases = exhaustive_atlas_check()
    cases.update(deterministic_random_check(args.random_samples, args.max_order, args.seed))
    print("Construction cases exercised:")
    for name, count in cases.most_common():
        print(f"  {count:6d}  {name}")
    print("All checks passed.")


if __name__ == "__main__":
    main()
