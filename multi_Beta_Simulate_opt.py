# ✅ MÔ HÌNH CẠNH TRANH NGOÀI VỚI NHIỀU BETA - GÁN ALPHA 1 LẦN, LAN TRUYỀN LIÊN TIẾP
# ✅ Tính tổng hỗ trợ sau khi hội tụ bằng cách đếm node dương và âm
# ✅ Cập nhật: xử lý song song vòng lặp Alpha để tăng tốc độ
# ✅ Dùng tqdm để theo dõi tiến độ xử lý Alpha nodes

import os
import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm
from joblib import Parallel, delayed
from multiprocessing import cpu_count

INF = 10000
EPSILON = 0.1
DELTA = 0.2
MAX_ITER = 200
TOL = 1e-6
N_BETA = 2

# ✅ B1: Đọc mạng từ file
def import_network(file_path):
    with open(file_path, "r") as f:
        data = f.readlines()[1:]
    G = nx.DiGraph()
    for line in data:
        from_node, to_node, direction, weight = line.strip().split("\t")
        direction = int(direction)
        weight = float(weight)
        G.add_edge(from_node, to_node, weight=weight)
        if direction == 0:
            G.add_edge(to_node, from_node, weight=weight)
    return G

# ✅ B2: Ma trận kề và hàng xóm
def build_adjacency(G, node_order):
    n = len(node_order)
    node_index = {node: i for i, node in enumerate(node_order)}
    A = np.zeros((n, n))
    neighbors = {i: [] for i in range(n)}
    for u, v, data in G.edges(data=True):
        i, j = node_index[u], node_index[v]
        A[i, j] += data.get("weight", 1.0)
        neighbors[j].append(i)
    return A, neighbors, node_index

# ✅ B3: Cập nhật trạng thái
def update_states_multi_beta(x, A, neighbors, beta_indices, beta_weights, fixed_nodes):
    n = len(x)
    x_new = x.copy()
    beta_diff = np.zeros((len(beta_indices), len(x)))
    for i, b in enumerate(beta_indices):
        beta_diff[i, :] = x[b] - x
    beta_matrix = np.array(beta_weights) @ beta_diff  # (n, n_beta) @ (n_beta, n) -> (n,)
    beta_matrix = beta_matrix.flatten()  # ✅ Đảm bảo là mảng 1 chiều

    for u in range(n):
        if u in fixed_nodes:
            continue
        influence = EPSILON * sum(A[v, u] * (x[v] - x[u]) for v in neighbors[u])
        beta_influence = DELTA * beta_matrix[u]
        x_new[u] = x[u] + influence + beta_influence
    x_new = np.clip(x_new, -1000, 1000)
    return x_new

# ✅ B4: Mô phỏng cạnh tranh ngoài với Alpha ban đầu, sau đó gán Beta tích lũy
def simulate_competition(G, attach_nodes, x_prev=None, alpha_idx=None):
    node_order = list(G.nodes()) + [f"Beta{i}" for i in range(len(attach_nodes))]
    A, neighbors, node_index = build_adjacency(G, node_order)
    n = len(node_order)

    if x_prev is None:
        x_prev = np.zeros(n)
        if alpha_idx is not None:
            alpha_node_name = list(G.nodes())[alpha_idx]
            alpha_idx = node_order.index(alpha_node_name)
            x_prev[alpha_idx] = 1

    x = x_prev.copy()
    # ✅ Vá lỗi: mở rộng x nếu chưa đủ chiều
    if x.shape[0] < len(node_order):
        x = np.pad(x, (0, len(node_order) - x.shape[0]), mode='constant')

    beta_indices = []
    fixed_nodes = set()
    beta_weights = [[0] * len(attach_nodes) for _ in range(n)]

    for i, attach_node in enumerate(attach_nodes):
        beta_name = f"Beta{i}"
        beta_idx = node_index[beta_name]
        A[beta_idx, node_index[attach_node]] = 1.0
        neighbors[node_index[attach_node]].append(beta_idx)
        x[beta_idx] = -1
        beta_indices.append(beta_idx)
        fixed_nodes.add(beta_idx)
        beta_weights[node_index[attach_node]][i] = 1.0

    for _ in range(MAX_ITER):
        x_new = update_states_multi_beta(x, A, neighbors, beta_indices, beta_weights, fixed_nodes)
        if np.linalg.norm(x_new - x) < TOL:
            break
        x = x_new

    return x[:len(G.nodes())]

# ✅ B5: Tính tổng hỗ trợ cho node Alpha đã biết
def compute_total_support(x_state, alpha_idx):
    support = 0
    for j in range(len(x_state)):
        if j == alpha_idx:
            continue
        if x_state[j] > 0:
            support += 1
        elif x_state[j] < 0:
            support -= 1
    return support

# ✅ B6: Hàm xử lý cho từng node Alpha riêng biệt
def process_alpha(alpha_node, G, all_nodes):
    node_order = list(G.nodes())
    alpha_idx = node_order.index(alpha_node)
    x_state = np.zeros(len(node_order))
    x_state[alpha_idx] = 1
    for i in range(0, len(all_nodes), N_BETA):
        beta_nodes = all_nodes[i:i+N_BETA]
        if alpha_node in beta_nodes:
            continue
        x_state = simulate_competition(G, beta_nodes, x_state, alpha_idx)
    support = compute_total_support(x_state, alpha_idx)
    return {"Alpha_Node": alpha_node, "Total_Support": support}

# ✅ B7: Main
def main():
    input_folder = "data_2"
    output_folder = "output_multi_beta_opt"
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if not file.endswith(".txt"):
            continue
        path = os.path.join(input_folder, file)
        G = import_network(path)
        all_nodes = list(G.nodes())

        all_results = Parallel(n_jobs=cpu_count() // 2)(
            delayed(process_alpha)(alpha_node, G, all_nodes)
            for alpha_node in tqdm(all_nodes, desc=f"🔁 Đang xử lý file: {file}")
        )

        df = pd.DataFrame(all_results)
        file_base = os.path.splitext(file)[0]
        out_path = os.path.join(output_folder, file_base + ".csv")
        df.to_csv(out_path, index=False)
        print(f"✅ Đã lưu kết quả vào {out_path}")

if __name__ == "__main__":
    main()
