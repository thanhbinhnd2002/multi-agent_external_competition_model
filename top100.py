# 🧪 Ý tưởng:
# Đọc 2 file csv:
# - csv1 chứa thông tin Alpha_Node và Total_Support
# - csv2 chứa danh sách các gene đã biết là Oncogene hoặc Tumor Suppressor Gene
# Ta lọc top 100 Alpha_Node có Total_Support cao nhất và đối chiếu Alpha_Node đó với Hugo Symbol trong file csv2

import pandas as pd
import os

# 📥 Bước 1: Đọc dữ liệu từ 2 file csv
csv1_path = "./output_multi_beta/Human Gene Regulatory Network - Input.csv"
csv2_path = "Cancer gene OncoKB30012025.xlsx"

df1 = pd.read_csv(csv1_path)
df2 = pd.read_excel(csv2_path, usecols=["Hugo Symbol", "Is Oncogene", "Is Tumor Suppressor Gene"])

# 📊 Bước 2: Lọc top 50 Alpha_Node có tổng hỗ trợ lớn nhất
df1_sorted = df1.sort_values(by="Total_Support", ascending=False).head(100)

# 🔁 Chuẩn hóa tên Alpha_Node và Hugo Symbol
df1_sorted['Alpha_Node'] = df1_sorted['Alpha_Node'].str.upper()
df2['Hugo Symbol'] = df2['Hugo Symbol'].str.upper()

# 🔍 Bước 3: Lọc các Alpha_Node có mặt trong danh sách Hugo Symbol
matched = df1_sorted[df1_sorted['Alpha_Node'].isin(df2['Hugo Symbol'])]

# 🧬 Bước 4: Nối thêm thông tin từ gene list
merged = matched.merge(df2, left_on='Alpha_Node', right_on='Hugo Symbol')

# 📁 Bước 5: Tạo thư mục và tên file output
csv1_name = os.path.splitext(os.path.basename(csv1_path))[0]
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"matched_top100_Alpha_Nodes_{csv1_name}.csv")

# 💾 Bước 6: Ghi kết quả
merged.to_csv(output_path, index=False)
print(f"✅ Hoàn tất! Kết quả đã được lưu vào: {output_path}")
