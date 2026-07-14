# BeautifulSoup Documentation Analytics System

Hệ thống tự động thu thập, trích xuất cấu trúc văn bản, phân loại liên kết và phân tích ví dụ mã nguồn từ trang tài liệu chính thức của BeautifulSoup.

---

## 1. Hướng dẫn cài đặt nhanh (Quick Setup)

* **Bước 1: Clone dự án và truy cập thư mục**
  ```bash
  git clone https://github.com/nghiahaodl2019/PDS310m_Project_Group2.git
  cd PDS301m_Project_Group2
  ```

* **Bước 2: Tạo và kích hoạt môi trường ảo**
  * *Trên Windows (PowerShell):*
    ```bash
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```
  * *Trên macOS/Linux:*
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

* **Bước 3: Cài đặt thư viện dependencies**
  ```bash
  pip install -r requirements.txt
  ```

* **Bước 4: Chạy toàn bộ hệ thống (Pipeline)**
  ```bash
  python src/main.py
  ```

---

## 2. Luồng hoạt động tổng quan (Operational Pipeline Flow)

* **Bước 1: Thu thập (Collection):** Tải mã nguồn HTML thô từ trang chủ BeautifulSoup và lưu trữ cục bộ.
* **Bước 2: Phân tích cú pháp (Parsing):** Dựng cây cấu trúc tài liệu DOM từ file HTML đã tải.
* **Bước 3: Trích xuất (Extraction):** Bóc tách thông tin thành 3 bảng dữ liệu có cấu trúc: Phân mục (`sections.csv`), Liên kết (`links.csv`), và Ví dụ mã nguồn (`code_examples.csv`).
* **Bước 4: Thống kê & Phân tích (Analytics):** Đọc các file CSV vào Pandas DataFrame để thực hiện tính toán số liệu và trả lời 10 câu hỏi nghiên cứu.
* **Bước 5: Trực quan hóa (Visualization):** Vẽ và xuất 4 biểu đồ phân tích thống kê dưới dạng hình ảnh.
* **Bước 6: Xuất báo cáo (Reporting):** Tạo báo cáo phân tích tổng hợp định dạng PDF và chạy tài liệu tương tác trên Jupyter Notebook.

---

## 3. Quản lý thông tin & Vai trò công cụ (Information Management & Tooling)

### 3.1. Phân biệt luồng quản lý dữ liệu giữa Python và Jupyter
* **Mã nguồn Python (`src/*.py`):**
  * Quản lý thông tin theo cơ chế **"Tách biệt qua tệp tin" (File-based Stateless)**.
  * Mỗi bước trong luồng xử lý ghi đầu ra xuống đĩa cứng (như file `.html`, `.csv`, `.json`). Bước tiếp theo sẽ đọc file này lên để xử lý tiếp.
  * Giúp hệ thống hoạt động độc lập, dễ bảo trì, dễ viết kiểm thử tự động và có thể tích hợp chạy định kỳ không cần sự can thiệp của con người.
* **Jupyter Notebook (`notebooks/*.ipynb`):**
  * Quản lý thông tin theo cơ chế **"Trạng thái trong bộ nhớ" (Stateful In-Memory)**.
  * Toàn bộ biến số, nội dung HTML thô và các bảng dữ liệu (DataFrames) được lưu giữ liên tục trong bộ nhớ RAM trong suốt phiên làm việc.
  * Cho phép người lập trình chạy thử từng ô code nhỏ để kiểm tra kết quả ngay lập tức, rất phù hợp cho giai đoạn nghiên cứu ban đầu (EDA) và viết thuyết minh báo cáo.

### 3.2. Vai trò chuyên biệt của Pandas và NumPy
* **Thư viện Pandas:**
  * Đóng vai trò là **"Quản lý bảng dữ liệu"**.
  * Chuyên dùng để đọc các file CSV trung gian, quản lý dữ liệu dưới dạng bảng hàng/cột (DataFrame), thực hiện lọc dữ liệu, nối bảng và gom nhóm thống kê (`groupby`).
* **Thư viện NumPy:**
  * Đóng vai trò là **"Công cụ tính toán số học"** làm nền tảng bên dưới Pandas.
  * Dùng để xử lý các mảng số liệu hiệu năng cao, đại diện các giá trị trống (`np.nan`) và thực hiện các biểu thức điều kiện vector hóa nhanh chóng (như gắn nhãn hoặc tính toán phân phối tần suất từ khóa).

### 3.3. Các điểm code mấu chốt trong quản lý thông tin
* **Quản lý đường dẫn gốc tuyệt đối (`PROJECT_ROOT`):**
  * Code sử dụng thư viện `pathlib.Path` để thiết lập đường dẫn gốc tuyệt đối của dự án:
    ```python
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    ```
  * Điểm code này đảm bảo rằng dù người dùng đứng ở bất kỳ thư mục nào để chạy lệnh (như đứng ở thư mục gốc, thư mục `src/`, hay chạy từ bên trong Jupyter Notebook), các file dữ liệu vẫn luôn được đọc và ghi chính xác vào các thư mục `data/` và `output/` của dự án mà không bị lỗi `FileNotFoundError`.
* **Tệp trao đổi dữ liệu phân tích (`analysis_results.json`):**
  * Toàn bộ kết quả thống kê của Feature 6 được đóng gói vào một tệp JSON chung. 
  * File JSON này đóng vai trò là "cầu nối thông tin", giúp module vẽ biểu đồ (Feature 7) và module xuất báo cáo PDF (Feature 8) có thể tái sử dụng ngay lập tức mà không cần phải thực hiện lại các phép tính toán phức tạp trên các bảng dữ liệu gốc.

---

## 4. Đặc tả chi tiết giải pháp cho từng Feature (Technical Specifications)

* **Feature 1: Web Page Collector (Thu thập HTML thô)**
  * *Mục tiêu:* Tải toàn bộ nội dung trang web chính thức của BeautifulSoup về máy.
  * *Giải pháp:* Sử dụng thư viện `requests.get()` với tham số `timeout=20` để chống treo luồng khi mạng lỗi. Gửi kèm header `User-Agent` giả lập trình duyệt Chrome để tránh bị máy chủ web chặn truy cập (lỗi HTTP 403). Ghi nội dung nhận được bằng bộ mã hóa `utf-8` để bảo toàn các ký tự đa ngôn ngữ.

* **Feature 2: HTML Parser (Phân tích cú pháp)**
  * *Mục tiêu:* Phân tích mã nguồn HTML thô để sẵn sàng bóc tách.
  * *Giải pháp:* Sử dụng thư viện `BeautifulSoup` kết hợp với trình phân tích cú pháp `lxml` giúp tối ưu hóa tốc độ xử lý và bóc tách các thẻ HTML nhanh hơn nhiều so với trình phân tích mặc định.

* **Feature 3: Section Extractor (Thuật toán duyệt phần tử kế cận)**
  * *Mục tiêu:* Tách tài liệu thành các phân mục rõ ràng dựa trên tiêu đề.
  * *Giải pháp:* Tìm kiếm tất cả các thẻ tiêu đề (`h1`, `h2`, `h3`). Với mỗi tiêu đề, code sử dụng thuộc tính `next_elements` để duyệt qua các thẻ kế tiếp trong văn bản. Quá trình duyệt sẽ liên tục đếm số thẻ `<pre>` (khối code), thẻ `<a>` (liên kết) và tích lũy chữ thô. Quá trình này sẽ dừng lại ngay khi chạm tới một thẻ tiêu đề khác có cấp độ tương đương hoặc cao hơn. Lưu kết quả vào `data/processed/sections.csv`.

* **Feature 4: Link Extractor & Classifier (Thuật toán phân loại liên kết)**
  * *Mục tiêu:* Thu thập toàn bộ thẻ `<a>` và phân loại.
  * *Giải pháp:* Tìm tất cả thẻ `<a>` bằng `soup.find_all('a')`. Dùng hàm `find_previous()` để tìm ngược về tiêu đề gần nhất trước nó nhằm xác định liên kết thuộc phân mục nào. Phân loại liên kết dựa trên các quy tắc:
    * `internal_anchor`: Thuộc tính `href` bắt đầu bằng ký tự `#`.
    * `image_link`: `href` kết thúc bằng các đuôi định dạng ảnh (`.png`, `.jpg`, `.gif`...).
    * `documentation_link`: `href` chứa từ khóa `bs4/doc` hoặc là đường dẫn tương đối dẫn tới các trang hướng dẫn khác.
    * `external_link`: `href` chứa tên miền bên ngoài (bắt đầu bằng `http` hoặc `https` không thuộc domain chính).
    * `empty_or_invalid`: `href` bị thiếu, trống hoặc chứa mã script `javascript:`.
    * Lưu kết quả vào `data/processed/links.csv`.

* **Feature 5: Code Example Extractor (Bóc tách mã ví dụ)**
  * *Mục tiêu:* Trích xuất các đoạn code Python minh họa.
  * *Giải pháp:* Tìm các thẻ `<pre>` chứa mã nguồn. Số lượng dòng code được đếm bằng cách tách chuỗi theo ký tự xuống dòng (`\n`). Chuyển toàn bộ đoạn mã về chữ thường (`.lower()`) rồi áp dụng toán tử `in` để kiểm tra nhanh sự xuất hiện của các từ khóa đặc biệt (`find_all`, `find`, `select`, `get_text`, `requests`) giúp tăng tốc độ xử lý chuỗi. Lưu kết quả vào `data/processed/code_examples.csv`.

* **Feature 6: Documentation Analytics (Phân tích Pandas/NumPy)**
  * *Mục tiêu:* Trả lời 8 câu hỏi bắt buộc và 2 câu hỏi mở rộng.
  * *Giải pháp:* Đọc 3 file CSV đã trích xuất vào các Pandas DataFrame. Áp dụng các hàm tính toán vector hóa của Pandas và NumPy như `.groupby()`, `.idxmax()`, `.value_counts()` để xử lý tính toán số liệu thống kê một cách tối ưu mà không sử dụng các vòng lặp `for` thủ công chậm chạp.

* **Feature 7: Data Visualization (Trực quan hóa)**
  * *Mục tiêu:* Vẽ 4 biểu đồ phân tích thống kê.
  * *Giải pháp:* Sử dụng thư viện `matplotlib.pyplot` vẽ biểu đồ cột nằm ngang cho số từ và số ví dụ code, vẽ biểu đồ phân phối tần suất (Histogram) cho số dòng code. Riêng biểu đồ tròn (Pie chart) của liên kết: ẩn các nhãn trực tiếp trên hình tròn để tránh chồng chữ lên nhau, tạo một bảng chú thích (Legend) nằm bên phải hình tròn và thiết lập chỉ hiển thị phần trăm (%) trực tiếp nếu tỉ lệ lớn hơn hoặc bằng 2%.

* **Feature 8: Final Report Generator (Xuất báo cáo PDF)**
  * *Mục tiêu:* Tạo báo cáo phân tích định dạng PDF hoàn chỉnh.
  * *Giải pháp:* Sử dụng thư viện `reportlab` xây dựng tài liệu qua cấu trúc `SimpleDocTemplate`. Để ngăn chặn chữ bị tràn ra ngoài viền bảng (lỗi overflow), tất cả các văn bản hiển thị trong bảng đều được bóc tách và bọc trong đối tượng `Paragraph` có định dạng font size và khoảng đệm (padding) rõ ràng, giúp chữ tự động xuống dòng khi cột bị hẹp. Đồng thời sử dụng hàm callback `onLaterPages` để tự động vẽ số trang ở chân trang.

---

## 5. Đặc tả cấu trúc Dữ liệu đầu ra (Data Schemas)

* **Bảng `sections.csv` (113 dòng):**
  * `section_id`: Số thứ tự phân mục (khóa chính).
  * `section_level`: Cấp độ tiêu đề (`h1`, `h2`, `h3`).
  * `section_title`: Tên tiêu đề phân mục.
  * `section_text`: Văn bản thô của phân mục.
  * `word_count`: Số từ.
  * `code_block_count`: Số đoạn code ví dụ.
  * `link_count`: Số liên kết.

* **Bảng `links.csv` (504 dòng):**
  * `link_text`: Văn bản hiển thị của link.
  * `href`: Đường dẫn liên kết.
  * `link_type`: Phân loại liên kết (`internal_anchor`, `external_link`, `documentation_link`, `image_link`, `empty_or_invalid`).
  * `section_title`: Tiêu đề phân mục chứa link này.

* **Bảng `code_examples.csv` (220 dòng):**
  * `example_id`: Số thứ tự ví dụ code.
  * `section_title`: Tiêu đề phân mục chứa ví dụ code.
  * `code_text`: Mã nguồn Python.
  * `line_count`: Số dòng code.
  * `contains_find_all` / `contains_find` / `contains_select` / `contains_get_text` / `contains_requests`: Trạng thái chứa từ khóa tương ứng (`1` là có, `0` là không).

---

## 6. Quy trình làm việc trên Git (Git Workflow)

* **Quy ước đặt tên Branch:** Mỗi thành viên phát triển tính năng trên branch riêng, đặt tên trùng với mã tính năng:
  * Thu thập dữ liệu: `feature1/web-page-collector`
  * Phân tích cú pháp: `feature2/html-parser`
  * Trích xuất phân mục: `feature3/section-extractor`
  * Trích xuất liên kết: `feature4/link-extractor`
  * Trích xuất mã ví dụ: `feature5/code-example-extractor`
  * Phân tích dữ liệu: `feature6/documentation-analytics`
  * Trực quan hóa: `feature7/data-visualization`
  * Báo cáo cuối kỳ: `feature8/final-report-generator`
  * Ứng dụng giao diện: `feature-advanced/local-analytics-app`
  * Sửa lỗi: `fix/tên-lỗi`

* **Quy ước viết Commit Messages:**
  * `feat`: Thêm tính năng mới (ví dụ: `feat: add web collector module`).
  * `fix`: Sửa lỗi phát sinh (ví dụ: `fix: resolve empty link type error`).
  * `docs`: Cập nhật tài liệu hướng dẫn (ví dụ: `docs: update setup guide`).
  * `refactor`: Tối ưu cấu trúc code (ví dụ: `refactor: optimize sections parsing`).

* **Quy tắc bỏ qua tệp tin (`.gitignore`):**
  * Không push các file HTML gốc, file CSV kết quả, file ảnh biểu đồ, file PDF báo cáo và môi trường ảo cá nhân lên kho chứa GitHub để tránh xung đột dữ liệu giữa các máy.
  * Các đường dẫn bị chặn bao gồm: `.venv/`, `__pycache__/`, `data/raw/*.html`, `data/processed/*.csv`, `output/charts/*.png`, và `output/final_report.pdf`.
