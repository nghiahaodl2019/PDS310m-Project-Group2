# BeautifulSoup Documentation Analytics System

Dự án thu thập, phân tích dữ liệu và trực quan hóa tài liệu chính thức của BeautifulSoup nhằm phân tích cấu trúc tài liệu, liên kết và ví dụ mã nguồn Python.

# WARNING: NHỚ KÍCH HOẠT VIRTUAL ENVIRONMENT (.venv) TRƯỚC KHI CHẠY CODE NHA AE !!!!!!!!!!!!!!!!!

### Cách xài github
https://www.youtube.com/watch?v=wFKu81ZMEcg

## 0. Checklist trước khi code (SET UP XONG ĐỌC CŨNG ĐC)

Trước khi bắt đầu làm task mới:

```bash
git pull origin main
git checkout -b feature/task-name
```
Pull project để update code, checkout để tạo branch mới, không code thẳng vào main nha ae

Trước khi push:

```bash
python src/main.py
git status
```

## 1. Công nghệ sử dụng

- Python (BeautifulSoup4, Pandas, NumPy, Matplotlib, Requests)
- Jupyter Notebook

### Công cụ cần cài
- Python 3.10 trở lên
- Visual Studio Code
- Git

---

## 2. Các luồng chính của hệ thống

### 2.1 Web Page Collector
Thu thập nội dung HTML từ URL chính thức của BeautifulSoup và lưu vào `data/raw/beautifulsoup_doc.html`.

### 2.2 HTML Parser & Section Extractor
Sử dụng BeautifulSoup để phân tích cú pháp HTML và trích xuất danh sách các phần (sections) của tài liệu, lưu vào `data/processed/sections.csv`.

### 2.3 Link Extractor & Classifier
Trích xuất tất cả các siêu liên kết và phân loại chúng thành các nhóm (`internal_anchor`, `external_link`, `documentation_link`, `image_link`, `empty_or_invalid`), lưu vào `data/processed/links.csv`.

### 2.4 Code Example Extractor
Trích xuất các đoạn code ví dụ Python trong tài liệu và kiểm tra sự xuất hiện của các từ khóa quan trọng (`find_all()`, `find()`, v.v.), lưu vào `data/processed/code_examples.csv`.

### 2.5 Documentation Analytics & Visualization
Sử dụng Pandas/NumPy để thực hiện 8+ câu hỏi phân tích dữ liệu và vẽ 4 biểu đồ lưu vào `output/charts/`.

---

## 3. Cấu trúc thư mục đề xuất

```txt
PDS301m_Project_Group2/
  data/
    raw/
      beautifulsoup_doc.html        # Raw HTML downloaded from the web
    processed/
      sections.csv                  # Extracted sections metadata
      links.csv                     # Extracted hyperlinks
      code_examples.csv             # Extracted Python code examples
  notebooks/
    analysis.ipynb                  # Jupyter Notebook for exploratory analytics
  output/
    charts/
      word_count_by_section.png     # Bar chart: Top 10 sections by word count
      code_examples_by_section.png  # Bar chart: Number of code examples by section
      link_type_distribution.png    # Pie chart: Link type distribution
      code_linecount_hist.png       # Histogram: Code example line count distribution
    final_report.pdf                # Compiled PDF report
  src/
    collector.py                    # Feature 1: Downloads HTML
    parser.py                       # Feature 2: Parses HTML using BeautifulSoup
    extractor.py                    # Features 3, 4, 5: Extracts CSV tables
    analyzer.py                     # Feature 6: Executes analytics
    visualizer.py                   # Feature 7: Generates charts
    main.py                         # Feature 8: Orchestrates the pipeline
  README.md
  requirements.txt
```

Lưu ý: nếu project thực tế đang đặt tên thư mục khác, thành viên trong nhóm cần sửa lại lệnh `cd` cho đúng.

---

## 4. Cách clone project

```bash
git clone <repo-url>
cd PDS301m_Project_Group2
```

Ví dụ:

```bash
git clone https://github.com/<owner>/PDS301m_Project_Group2.git
cd PDS301m_Project_Group2
```

---

## 5. Cấu hình chạy dự án

**AE NHỚ CÀI PYTHON 3.10+ NHA NHA NHA !!!!!**
Link: https://www.python.org/downloads/

Đi vào thư mục root của dự án:

```bash
cd PDS301m_Project_Group2
```

Tạo và kích hoạt Virtual Environment:

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt trên Windows PowerShell:
.venv\Scripts\Activate.ps1

# Kích hoạt trên Windows CMD:
.venv\Scripts\activate.bat

# Kích hoạt trên macOS/Linux:
source .venv/bin/activate
```

Cài đặt các thư viện cần thiết (dependencies):

```bash
pip install -r requirements.txt
```

Chạy toàn bộ pipeline thu thập và phân tích dữ liệu:

```bash
python src/main.py
```

Chạy Jupyter Notebook để kiểm tra hoặc viết báo cáo:

```bash
jupyter notebook notebooks/analysis.ipynb
```

---

## 6. Quy trình làm việc với Git

Không push trực tiếp lên `main`.

Tạo branch riêng cho từng task:

```bash
git checkout -b feature/collector
```

Commit code:

```bash
git add .
git commit -m "feat: add web collector module"
```

Push branch:

```bash
git push -u origin feature/collector
```

Sau đó tạo Pull Request trên GitHub để merge vào `main`.

---

## 7. Quy ước đặt tên branch

```txt
feature/collector
feature/parser
feature/extractor
feature/analyzer
feature/visualizer
fix/parser-bug
docs/setup-guide
```

---

## 8. Quy ước commit message

```txt
feat: add web collector module
feat: add link extraction functionality
fix: resolve empty link type error
docs: update setup guide
refactor: optimize sections parsing
```

Ý nghĩa:
- `feat`: thêm chức năng mới
- `fix`: sửa lỗi
- `docs`: cập nhật tài liệu
- `refactor`: chỉnh lại code nhưng không đổi behavior
- `chore`: việc phụ như config, format, dependency

---

## 9. File không được commit

Các file và thư mục sau không được push lên GitHub:

```txt
.venv/
venv/
__pycache__/
.ipynb_checkpoints/
data/raw/*.html
data/processed/*.csv
output/charts/*.png
```

Nên có file `.gitignore` ở root project:

```gitignore
# Virtual Environment
.venv/
venv/
env/
ENV/

# Python cache files
__pycache__/
*.py[cod]
*$py.class

# Jupyter Notebook checkpoints
.ipynb_checkpoints/

# Data files & generated outputs (Run scripts locally to generate them)
data/raw/*.html
data/processed/*.csv
output/charts/*.png
output/final_report.pdf

# OS files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/
```

---

## 10. Lỗi thường gặp

### 10.1 Lỗi ModuleNotFoundError

Lỗi do chưa active virtual environment hoặc chưa cài đủ thư viện.
Khắc phục: chạy kích hoạt `.venv` trước rồi mới cài đặt thư viện:

```bash
pip install -r requirements.txt
```

### 10.2 Lỗi FileNotFoundError khi chạy src/main.py

Lỗi do terminal đang đứng sai thư mục (không phải thư mục root của dự án).
Khắc phục: Sử dụng lệnh `cd` để chuyển terminal về đúng thư mục `PDS301m_Project_Group2` trước khi chạy code.

### 10.3 Lỗi HTTP 403 / Timeout khi collect raw HTML

Lỗi do trang web chặn request hoặc kết nối mạng không ổn định.
Khắc phục: Kiểm tra kết nối internet hoặc thêm headers giả lập trình duyệt (User-Agent) trong file `src/collector.py`.

### 10.4 Lỗi Jupyter Notebook không nhận kernel .venv

Lỗi do Jupyter chưa nhận môi trường ảo mới.
Khắc phục: Cài `ipykernel` trong `.venv`:

```bash
pip install ipykernel
python -m ipykernel install --user --name=pds301m_env
```
Sau đó mở file `.ipynb` và chọn kernel `pds301m_env` để chạy.

---

## 11. Ghi chú cho team

- Luôn kích hoạt `.venv` trước khi phát triển hoặc chạy thử.
- Không sửa trực tiếp trên branch `main`.
- Không push thư mục `.venv`.
- Không push dữ liệu raw/processed và biểu đồ lên GitHub.
- Mỗi task nên có một branch riêng.
- Code xong tạo Pull Request để cả team review.
