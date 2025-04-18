# 🧪 Ý tưởng:
# Đọc 2 file csv:
# - csv1 chứa thông tin Alpha_Node và Total_Support
# - csv2 chứa danh sách các gene đã biết là Oncogene hoặc Tumor Suppressor Gene + Gene Aliases
# Ta lọc top 100 Alpha_Node có Total_Support cao nhất và đối chiếu Alpha_Node đó với Hugo Symbol hoặc Gene Aliases

import pandas as pd
import os

# 📥 Bước 1: Đọc dữ liệu từ 2 file csv
csv1_path = "./output_multi_beta/Human Gene Regulatory Network - Input.csv"
csv2_path = "Cancer gene OncoKB30012025.xlsx"

df1 = pd.read_csv(csv1_path)
df2 = pd.read_excel(csv2_path, usecols=["Hugo Symbol", "Is Oncogene", "Is Tumor Suppressor Gene", "Gene Aliases"])

# 📊 Bước 2: Lọc top 100 Alpha_Node có tổng hỗ trợ lớn nhất
df1_sorted = df1.sort_values(by="Total_Support", ascending=False).head(100)

# 🔁 Chuẩn hóa tên để so khớp
df1_sorted['Alpha_Node'] = df1_sorted['Alpha_Node'].str.upper()
df2['Hugo Symbol'] = df2['Hugo Symbol'].str.upper()

# 📌 Tạo ánh xạ từ Hugo Symbol và từng alias tới thông tin gene
gene_map = {}
for _, row in df2.iterrows():
    hugo = row["Hugo Symbol"]
    entry = {
        "Hugo Symbol": hugo,
        "Is Oncogene": row["Is Oncogene"],
        "Is Tumor Suppressor Gene": row["Is Tumor Suppressor Gene"]
    }
    gene_map[hugo] = {**entry, "Match Source": "Hugo Symbol"}
    if pd.notna(row["Gene Aliases"]):
        aliases = [alias.strip().upper() for alias in str(row["Gene Aliases"]).split(",")]
        for alias in aliases:
            if alias not in gene_map:
                gene_map[alias] = {**entry, "Match Source": "Gene Alias"}

# 🔍 Bước 3: Đối chiếu Alpha_Node với Hugo Symbol hoặc Gene Aliases
matched_rows = []
for _, row in df1_sorted.iterrows():
    alpha = row["Alpha_Node"]
    if alpha in gene_map:
        matched_info = gene_map[alpha]
        matched_rows.append({
            "Alpha_Node": alpha,
            "Total_Support": row["Total_Support"],
            **matched_info
        })

# 📄 Bước 4: Tạo DataFrame kết quả
merged = pd.DataFrame(matched_rows)

# 📁 Bước 5: Tạo thư mục và tên file output
csv1_name = os.path.splitext(os.path.basename(csv1_path))[0].replace(" ", "_")
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"matched_top100_Alpha_Nodes_{csv1_name}.csv")

# 💾 Bước 6: Ghi kết quả
merged.to_csv(output_path, index=False)
print(f"✅ Hoàn tất! Kết quả đã được lưu vào: {output_path}")
