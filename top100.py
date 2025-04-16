# 🧪 Ý tưởng:
# Đọc 2 file csv:
# - csv1 chứa thông tin  Alpha_Node và Total_Support
# - csv2 chứa danh sách các gene đã biết là Oncogene hoặc Tumor Suppressor Gene
# Ta lọc top 100  Alpha_Node có Total_Support cao nhất và đối chiếu  Alpha_Node đó với Hugo Symbol trong file csv2

import pandas as pd

# 📥 Bước 1: Đọc dữ liệu từ 2 file csv
csv1_path = "./output_multi_beta/Human Gene Regulatory Network - Input.csv"  # file chứa  Alpha_Node, Total_Support
csv2_path = "Cancer gene OncoKB30012025.xlsx"    # file chứa Hugo Symbol, Is Oncogene, Is Tumor Suppressor Gene

df1 = pd.read_csv(csv1_path)
print(df1.columns)

df2 = pd.read_excel(csv2_path,usecols=["Hugo Symbol", "Is Oncogene", "Is Tumor Suppressor Gene"])
print(df2.columns)

# 📊 Bước 2: Lọc top 100  Alpha_Node có tổng hỗ trợ lớn nhất
df1_sorted = df1.sort_values(by="Total_Support", ascending=False).head(100)

# 🔁 Chuẩn hóa tên  Alpha_Node và symbol để dễ đối chiếu
df1_sorted['Alpha_Node'] = df1_sorted['Alpha_Node'].str.upper()
df2['Hugo Symbol'] = df2['Hugo Symbol'].str.upper()

# 🔍 Bước 3: Lọc các  Alpha_Node có mặt trong danh sách Hugo Symbol
matched = df1_sorted[df1_sorted['Alpha_Node'].isin(df2['Hugo Symbol'])]

# 🧬 Bước 4: Nối thông tin từ file 2
merged = matched.merge(df2, left_on='Alpha_Node', right_on='Hugo Symbol')

# 💾 Bước 5: Xuất kết quả
merged.to_csv("matched_top100_ Alpha_Nodes.csv", index=False)

print("✅ Hoàn tất! Kết quả đã được lưu vào file: matched_top100_ Alpha_Nodes.csv")
