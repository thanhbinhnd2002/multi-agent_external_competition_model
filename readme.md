Ah đúng rồi 😄! Dưới đây là nội dung mẫu cho **`README.md`** mô tả đầy đủ về project của bạn – mô phỏng mô hình cạnh tranh ngoài với nhiều Beta để xác định các gene có ảnh hưởng mạnh nhất trong mạng và xác thực với bộ dữ liệu OncoKB.

---

### ✅ **📄 README.md – Mô tả Project**

```markdown
# 🔬 Gene Influence Ranking via Competitive Dynamics Model

Đây là project mô phỏng **mô hình cạnh tranh ngoài với nhiều tác nhân (Beta)** trên mạng phức hợp sinh học, nhằm xác định các gene có ảnh hưởng mạnh nhất trong mạng. Mục tiêu cuối cùng là **đối chiếu với bộ dữ liệu OncoKB** để kiểm chứng độ chính xác và phát hiện các gene mục tiêu tiềm năng cho điều trị ung thư.

---

## 🎯 Mục đích

- Xây dựng mô hình cạnh tranh động lực học với nhiều tác nhân Beta.
- Tính toán **Total Support** cho từng gene trong mạng, đại diện cho sức ảnh hưởng của gene đó.
- Đối chiếu các gene top ảnh hưởng với **cơ sở dữ liệu OncoKB** để tìm các gene đã được công nhận là:
  - `Oncogene`
  - `Tumor Suppressor Gene`

---

## 🧠 Cơ sở lý thuyết

Mô hình dựa trên nghiên cứu trong bài báo:
> **Competitive Dynamics on Complex Networks** – Zhao et al. (2014) [[DOI:10.1038/srep05858]](https://www.nature.com/articles/srep05858)

Cụ thể, mô hình:
- Gán trạng thái cố định cho các tác nhân ngoài (Beta).
- Cho lan truyền trạng thái trong mạng theo nguyên lý đồng thuận phân tán.
- Tính trạng thái hội tụ và từ đó suy ra **Total Support** của từng node.

---

## 🗂️ Cấu trúc thư mục

```bash
├── data_1/                          # Mạng sinh học tập 1
├── data_2/                          # Mạng sinh học tập 2
├── data_3/                          # Mạng sinh học tập 3
│   └── Human PPI network - Input.txt

├── output_multi_beta/              # Kết quả mô phỏng phương pháp nhiều Beta
├── output_multi_beta_opt/          # Kết quả mô phỏng tối ưu hóa (song song, GPU,...)
├── results/                        # Kết quả đã đối chiếu với bộ dữ liệu OncoKB

├── Cancer gene OncoKB30012025.xlsx # Bộ dữ liệu chuẩn về gen ung thư (OncoKB)
├── Cancer gene OncoKB30012025.csv  # Bản CSV của OncoKB dùng để xử lý

├── compare.py                      # Script đối chiếu Alpha_Node với OncoKB
├── convert_excel_to_csv.py         # Script chuyển file excel → csv nếu cần
├── multi_Beta_Simulate_opt.py      # Mô phỏng cạnh tranh ngoài nhiều Beta (song song)
├── net_gpu.py                      # Phiên bản chạy GPU mô phỏng phương pháp 1
├── top100.py                       # Lọc top 100 node và đối chiếu với OncoKB
├── test_1.py, test_2.py            # Các script kiểm thử
├── readme.md                       # 📄 Mô tả project
├── requirements.txt                # 📦 Danh sách thư viện cần thiết
```

---

## ⚙️ Cách chạy mô hình

1. **Tạo dữ liệu mạng:** đặt vào thư mục `data/` với định dạng `.txt`
2. **Chạy mô phỏng tổng support:**

```bash
python multi_Beta_Simulate_opt.py
```

3. **Đối chiếu với oncoKB:**

```bash
python match_to_oncokb.py
```

Trong đó `match_to_oncokb.py` là script xử lý đối chiếu `Alpha_Node` với `Hugo Symbol` và `Gene Aliases` trong `Cancer gene OncoKB30012025.csv`.

---

## 🧪 Ví dụ đầu ra

| Alpha_Node | Total_Support | Hugo Symbol | Is Oncogene | Is Tumor Suppressor Gene |
|------------|----------------|--------------|--------------|---------------------------|
| TP53       | 79             | TP53         | TRUE         | TRUE                      |
| MYC        | 65             | MYC          | TRUE         | FALSE                     |

---

## 📚 Tài liệu tham khảo

- Zhao et al., **Competitive Dynamics on Complex Networks**, _Scientific Reports_, 2014.  
- Tran et al., **Drivergene.net**, _Computers in Biology and Medicine_, 2024.

---

## 👨‍🔬 Tác giả
- **Người thực hiện:** Phạm Thanh Bình
- **Trường:** Đại học Bách Khoa Hà Nội (HUST)
- **GVHD:** Thầy Phạm Văn Hải

```

---

