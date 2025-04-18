# ✅ Phiên bản GPU hoá của net.py - Tăng tốc bằng CuPy, giữ nguyên toàn bộ logic
# ✅ Mô hình cạnh tranh ngoài (Outside Competition) với 1 Beta
# ✅ Giữ nguyên phương pháp tính tổng hỗ trợ (Phương pháp 1)
# ✅ Không dùng ma trận ảnh hưởng nghịch đảo
# ✅ Yêu cầu: pip install cupy-cuda12x numpy networkx pandas tqdm joblib

import os
import cupy as cp
import numpy as np
import pandas as pd
import networkx as nx
from tqdm import tqdm
from joblib import Parallel, delayed
import multiprocessing

INF = 10000

def import_network(filename):
    with open(filename, "r") as f:
        data = f.readlines()
    net = nx.MultiDiGraph()
    for line in data[1:]:
        from_node, to_node, direction, weight = line.strip().split("\t")
        direction, weight = int(direction), int(weight)
        net.add_edge(from_node, to_node, weight=weight)
        if direction == 0:
            net.add_edge(to_node, from_node, weight=weight)
    return net

def get_node_edge(net):
    return list(net.nodes()), list(net.edges())

def extract_adj_matrix(nodes, edges):
    n = len(nodes)
    node_dict = {node: i for i, node in enumerate(nodes)}
    adj_matrix = cp.zeros((n, n), dtype=cp.int32)
    neighbors = {}
    for u, v in edges:
        i, j = node_dict[u], node_dict[v]
        adj_matrix[i, j] += 1
        neighbors.setdefault(v, set()).add(u)
    return adj_matrix, neighbors, node_dict

def compete(alpha, adj_matrix, neighbors, node_dict, n_edges):
    alpha_id = node_dict[alpha]
    beta_id = len(node_dict)
    n_nodes = len(node_dict)
    deg_max = int(cp.sum(adj_matrix, axis=1).max().item())
    epsilon = 1 / deg_max
    states = {i: 0.0 for i in range(n_nodes + 1)}
    states[alpha_id] = 1.0
    states[beta_id] = -1.0
    n_steps = n_nodes * n_edges

    for node, idx in node_dict.items():
        if idx in (alpha_id, beta_id):
            continue
        neighbors.setdefault(node, set()).add("Beta")
        t, converging = 0, float("inf")
        while converging > epsilon and t < n_steps:
            converging = 0
            updated_states = states.copy()
            for u, u_id in node_dict.items():
                if u_id in (alpha_id, beta_id): continue
                if not neighbors.get(u): continue
                s = 0.0
                for v in neighbors[u]:
                    if v == "Beta":
                        s += states[beta_id] - states[u_id]
                    else:
                        v_id = node_dict[v]
                        s += adj_matrix[v_id, u_id].item() * (states[v_id] - states[u_id])
                updated_states[u_id] += epsilon * s
                converging += abs(updated_states[u_id] - states[u_id])
            states = updated_states
            t += 1
        neighbors[node].remove("Beta")

    return alpha_id, states

def compute_distance_matrix(dataset, adj_matrix, node_dict):
    n = len(node_dict)
    A = adj_matrix.get().astype(np.int32)
    d = np.where(A > 0, 1, INF)
    np.fill_diagonal(d, 0)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i, j] = min(d[i, j], d[i, k] + d[k, j])
    return d

def compute_influence_matrix(states, distance_matrix, node_dict):
    n = len(node_dict)
    influence_matrix = np.zeros((n, n))
    for u, v in [(u, v) for u in node_dict for v in node_dict]:
        uid, vid = node_dict[u], node_dict[v]
        d = distance_matrix[vid][uid]
        if d != 0 and d != INF:
            influence_matrix[uid][vid] = states[vid] / (d ** 2)
    return influence_matrix

def compute_total_support(alpha_id, influence_matrix, node_dict, states):
    def sign(x): return 1 if x > 0 else -1 if x < 0 else 0
    return sum(
        sign(influence_matrix[alpha_id][node_dict[n]] - states[node_dict[n]])
        for n in node_dict if node_dict[n] != alpha_id
    )

def main():
    datasets = os.listdir("data_2")
    data_objects = [(os.path.join("data_2", f), f.replace(".txt", "")) for f in datasets]
    n_jobs = max(1, multiprocessing.cpu_count() // 2)

    for path, name in data_objects:
        G = import_network(path)
        nodes, edges = get_node_edge(G)
        adj_matrix, neighbors, node_dict = extract_adj_matrix(nodes, edges)
        distance_matrix = compute_distance_matrix(name, adj_matrix, node_dict)
        n_edges = len(edges)

        states = Parallel(n_jobs=n_jobs)(
            delayed(compete)(alpha, adj_matrix, neighbors.copy(), node_dict, n_edges)
            for alpha in tqdm(node_dict.keys(), desc=f"🔁 Đang xử lý {name}")
        )

        results = []
        for alpha_id, state in states:
            infl = compute_influence_matrix(state, distance_matrix, node_dict)
            score = compute_total_support(alpha_id, infl, node_dict, state)
            results.append((alpha_id, score))

        id_to_node = {v: k for k, v in node_dict.items()}
        os.makedirs("gpu_output", exist_ok=True)
        with open(f"gpu_output/{name}_total_supports.csv", "w") as f:
            f.write("Node_ID,Node,Total_Support\n")
            for nid, support in results:
                f.write(f"{nid},{id_to_node[nid]},{support}\n")

        print(f"✅ Đã xử lý xong: {name}")

if __name__ == "__main__":
    main()
