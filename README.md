# Vietnam Stock Data Analysis Terminal - VSDAT

**Vietnam Stock Data Analysis Terminal - VSDAT** là ứng dụng web hỗ trợ tra cứu, phân tích và xuất báo cáo dữ liệu chứng khoán Việt Nam.

Dự án cho phép người dùng nhập mã cổ phiếu, xem thông tin giá, phân tích kỹ thuật, biểu đồ trực quan và xuất báo cáo Excel theo khoảng thời gian tùy chọn.

> Dự án được xây dựng phục vụ mục đích học tập, thực hành lập trình, phân tích dữ liệu và tham khảo thông tin thị trường. Nội dung phân tích trong ứng dụng không phải là khuyến nghị đầu tư.

---

## Demo

- **Live Demo:** https://vsdat-frontend.onrender.com/
- **GitHub Repository:** https://github.com/tuanda2309/Vietnam_Stock_Data_Analysis_Terminal_VSDAT.git

---

## Demo giao diện

Dưới đây là một số hình ảnh minh họa giao diện và kết quả xuất báo cáo của dự án.

---

### 1. Giao diện tổng quan

![Giao diện tổng quan](img\image.png)

---

### 2. Kết quả phân tích cổ phiếu

| Kết quả phân tích | Chi tiết chỉ số |
|---|---|
| ![Kết quả phân tích cổ phiếu 1](img\image-3.png) | ![Kết quả phân tích cổ phiếu 2](img\image-4.png) |

![Kết quả phân tích cổ phiếu 3](img\image-5.png)

---

### 3. Biểu đồ giá và chỉ báo kỹ thuật

| Biểu đồ giá | Chỉ báo kỹ thuật |
|---|---|
| ![Biểu đồ giá và chỉ báo kỹ thuật 1](img\image-1.png) | ![Biểu đồ giá và chỉ báo kỹ thuật 2](img\image-2.png) |

---

### 4. File Excel sau khi export

File Excel được xuất ra dưới dạng báo cáo phân tích gồm nhiều sheet như Executive Summary, Dashboard quản trị, Phân tích, Dữ liệu sạch, Data Issues, Change Log và Phương pháp.

| Tổng quan Excel | Dashboard |
|---|---|
| ![File Excel sau khi export 1](img\image-6.png) | ![File Excel sau khi export 2](img\image-7.png) |

| Phân tích | Dữ liệu |
|---|---|
| ![File Excel sau khi export 3](img\image-8.png) | ![File Excel sau khi export 4](img\image-9.png) |

---

## Tính năng chính

- Tra cứu và phân tích cổ phiếu Việt Nam theo mã chứng khoán.
- Hiển thị thông tin giá, biến động giá và khối lượng giao dịch.
- Phân tích dữ liệu giá lịch sử theo khoảng thời gian.
- Tính toán và hiển thị các chỉ báo kỹ thuật phổ biến.
- Vẽ biểu đồ giá, khối lượng và các chỉ báo kỹ thuật.
- Phân tích xu hướng tăng/giảm của cổ phiếu.
- Xác định vùng hỗ trợ và kháng cự tham khảo.
- Đưa ra nhận xét tổng quan dựa trên dữ liệu kỹ thuật.
- Thống kê các phiên tăng mạnh nhất và giảm mạnh nhất.
- Thống kê dữ liệu giao dịch theo tháng.
- Xuất báo cáo phân tích cổ phiếu ra file Excel.
- Hỗ trợ chạy local và deploy online.
- Giao diện web đơn giản, dễ sử dụng.

---

## Các chỉ báo và nội dung phân tích

Ứng dụng có thể xử lý và hiển thị một số nhóm thông tin như:

- Giá mở cửa
- Giá cao nhất
- Giá thấp nhất
- Giá đóng cửa
- Khối lượng giao dịch
- Thay đổi giá
- Phần trăm thay đổi giá
- Lợi suất ngày
- Lợi suất lũy kế
- MA5
- MA10
- MA20
- RSI14
- Drawdown
- Đỉnh lũy kế
- Biến động 5 phiên
- Biến động 20 phiên
- Volume MA5
- Volume/MA5
- Tín hiệu kỹ thuật
- Thống kê các phiên tăng mạnh
- Thống kê các phiên giảm mạnh
- Thống kê dữ liệu theo tháng
- Báo cáo Excel tổng hợp

---

## Công nghệ sử dụng

### Backend

- Python
- Flask
- Flask-CORS
- Flask-Limiter
- Pandas
- NumPy
- OpenPyXL
- vnstock3
- Gunicorn

### Frontend

- React
- Vite
- Tailwind CSS
- Axios
- Recharts
- Lucide React

### Deploy

- Render

---

## Cấu trúc thư mục

```text
Vietnam_Stock_Data_Analysis_Terminal_VSDAT/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── constants.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── stock_routes.py
│   │   └── export_routes.py
│   ├── services/
│   │   ├── stock_service.py
│   │   ├── analysis_service.py
│   │   ├── market_service.py
│   │   ├── export_service.py
│   │   └── export/
│   │       ├── __init__.py
│   │       ├── constants.py
│   │       ├── data_preparation.py
│   │       ├── excel_helpers.py
│   │       ├── formatters.py
│   │       ├── naming.py
│   │       ├── service.py
│   │       ├── sheet_writers.py
│   │       ├── stock_api.py
│   │       ├── template_loader.py
│   │       └── workbook_builder.py
│   └── utils/
│       ├── dataframe_utils.py
│       ├── helpers.py
│       ├── indicators.py
│       ├── risk.py
│       ├── support_resistance.py
│       └── validators.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── utils/
│   │   └── i18n/
│
├── render.yaml
├── README.md
└── LICENSE
```

---

## Cài đặt project

### 1. Clone repository

```bash
git clone https://github.com/tuanda2309/Vietnam_Stock_Data_Analysis_Terminal_VSDAT.git
```

```bash
cd Vietnam_Stock_Data_Analysis_Terminal_VSDAT
```

---

## Chạy Backend

Di chuyển vào thư mục backend:

```bash
cd backend
```

Tạo môi trường ảo Python:

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
.venv\Scripts\activate
```

Kích hoạt môi trường ảo trên macOS/Linux:

```bash
source .venv/bin/activate
```

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

Chạy backend:

```bash
python app.py
```

Backend mặc định chạy tại:

```text
http://127.0.0.1:5000
```

Kiểm tra backend:

```text
http://127.0.0.1:5000/health
```

Kết quả mẫu:

```json
{
  "status": "ok",
  "service": "VSDAT backend"
}
```

---

## Chạy Frontend

Mở terminal mới, di chuyển vào thư mục frontend:

```bash
cd frontend
```

Cài đặt package:

```bash
npm install
```

Tạo file `.env` trong thư mục `frontend`:

```env
VITE_API_URL=http://127.0.0.1:5000
```

Chạy frontend:

```bash
npm run dev
```

Frontend mặc định chạy tại:

```text
http://localhost:5173
```

---

## API chính

### Kiểm tra trạng thái backend

```http
GET /health
```

### Lấy dữ liệu phân tích cổ phiếu

```http
GET /stock/<symbol>
```

Ví dụ:

```http
GET /stock/VIC
```

### Xuất báo cáo Excel

```http
GET /export/<symbol>/<start_date>/<end_date>
```

Ví dụ:

```http
GET /export/VIC/2026-01-01/2026-05-25
```

---

## Export Excel

Chức năng export Excel cho phép tạo báo cáo phân tích cổ phiếu theo mã chứng khoán và khoảng thời gian người dùng chọn.

File Excel được thiết kế theo dạng **báo cáo phân tích hoàn chỉnh**, không chỉ là bảng dữ liệu thô. Báo cáo có nhiều sheet, bao gồm phần tóm tắt cho quản lý, dashboard trực quan, phân tích chi tiết, dữ liệu sạch và ghi chú về chất lượng dữ liệu.

Ví dụ file Excel sau khi export:

```text
VIC_VSDAT_2026-01-01_2026-05-25.xlsx
```

Trong đó:

```text
VIC        = Mã cổ phiếu
VSDAT      = Tên hệ thống / loại báo cáo
2026-01-01 = Ngày bắt đầu
2026-05-25 = Ngày kết thúc
```

### Các sheet trong file Excel

File Excel export có thể gồm các sheet sau:

```text
1. Executive Summary
2. Dashboard quản trị
3. Phân tích
4. Dữ liệu sạch
5. Data Issues
6. Change Log
7. Phương pháp
```

### 1. Executive Summary

Sheet **Executive Summary** là phần tóm tắt nhanh dành cho người đọc báo cáo hoặc cấp quản lý.

Nội dung chính gồm:

- Tên mã cổ phiếu.
- Giai đoạn phân tích.
- Số phiên giao dịch.
- Ngày hoàn thiện báo cáo.
- Giá cuối kỳ.
- Hiệu suất trong kỳ.
- Thanh khoản trung bình.
- Mức rủi ro.
- Tình hình hiện tại của cổ phiếu.
- Điểm nổi bật hoặc vấn đề cần chú ý.
- Đề xuất hành động.
- Ghi chú về phạm vi sử dụng báo cáo.

Sheet này giúp người đọc nắm nhanh tình hình cổ phiếu mà không cần xem toàn bộ dữ liệu chi tiết.

---

### 2. Dashboard quản trị

Sheet **Dashboard quản trị** trình bày dữ liệu dưới dạng dashboard trực quan.

Nội dung chính gồm:

- KPI cards về giá cuối kỳ, drawdown, khối lượng trung bình và RSI14.
- Biểu đồ xu hướng giá đóng cửa và MA20.
- Biểu đồ hiệu suất theo tháng.
- Biểu đồ thanh khoản bình quân theo tháng.
- Nhận xét nhanh cho quản lý.

Sheet này phù hợp để xem nhanh xu hướng, biến động, rủi ro và thanh khoản của cổ phiếu trong kỳ phân tích.

---

### 3. Phân tích

Sheet **Phân tích** chứa các bảng phân tích chi tiết hơn.

Nội dung chính gồm:

- Giá đầu kỳ.
- Giá cuối kỳ.
- Hiệu suất kỳ.
- Thay đổi giá.
- Thanh khoản trung bình.
- Giá cao nhất kỳ.
- Giá thấp nhất kỳ.
- Drawdown lớn nhất.
- RSI14 cuối kỳ.
- Thống kê hiệu suất theo tháng.
- Top 5 phiên tăng mạnh nhất.
- Top 5 phiên giảm mạnh nhất.

Sheet này giúp kiểm tra các chỉ số quan trọng và các phiên giao dịch có biến động lớn trong kỳ.

---

### 4. Dữ liệu sạch

Sheet **Dữ liệu sạch** chứa dữ liệu đã được xử lý và chuẩn hóa để phục vụ phân tích.

Các cột dữ liệu có thể bao gồm:

- Ngày
- Mở cửa
- Cao nhất
- Thấp nhất
- Đóng cửa
- Thay đổi giá
- % thay đổi
- Khối lượng
- Lợi suất ngày
- Lợi suất lũy kế
- MA5
- MA10
- MA20
- Biến động 5 phiên
- Biến động 20 phiên
- Đỉnh lũy kế
- Drawdown
- RSI14
- Volume MA5
- Volume/MA5
- Tín hiệu
- Ngày biểu đồ

Sheet này dùng để kiểm tra dữ liệu gốc đã được làm sạch, lọc dữ liệu, đối chiếu kết quả phân tích và phục vụ biểu đồ trong báo cáo.

---

### 5. Data Issues

Sheet **Data Issues** ghi chú các vấn đề hoặc đặc điểm dữ liệu trong quá trình xử lý.

Nội dung có thể gồm:

- Mức độ vấn đề.
- Vấn đề dữ liệu.
- Trạng thái kiểm tra.
- Mô tả hoặc tác động.
- Hành động xử lý.

Ví dụ:

- Các chỉ số rolling như MA5, MA10, MA20, volatility, RSI14 cần đủ số phiên nên các dòng đầu kỳ có thể bị trống.
- Nguồn dữ liệu nên được đối chiếu thêm nếu dùng cho quyết định đầu tư thực tế.
- Kiểm tra ngày giao dịch trùng lặp.
- Kiểm tra lỗi công thức thường gặp trong workbook.

Sheet này giúp báo cáo minh bạch hơn, đặc biệt khi người dùng cần biết dữ liệu có giới hạn hoặc điểm cần lưu ý hay không.

---

### 6. Change Log

Sheet **Change Log** ghi lại các thay đổi hoặc bước xử lý chính trong file Excel.

Nội dung có thể gồm:

- Ngày thay đổi.
- Sheet bị ảnh hưởng.
- Nội dung thay đổi.
- Lý do thay đổi.

Sheet này giúp theo dõi quá trình tạo báo cáo, chỉnh layout, chuẩn hóa dữ liệu và cải thiện khả năng đọc của workbook.

---

### 7. Phương pháp

Sheet **Phương pháp** giải thích cách hiểu một số chỉ số trong báo cáo.

Nội dung có thể gồm:

- Hiệu suất kỳ.
- Drawdown.
- MA5, MA10, MA20.
- RSI14.
- Thanh khoản trung bình.
- Giới hạn của báo cáo.

Sheet này giúp người dùng hiểu ý nghĩa các chỉ số thay vì chỉ xem kết quả cuối cùng.

---

## Giới hạn export mặc định

Để tránh lỗi timeout, treo server hoặc tạo file Excel quá nặng, project hiện đang đặt giới hạn export mặc định:

```text
Thời gian export tối đa: 10 năm
Số dòng dữ liệu tối đa: 10.000 dòng
```

Các giới hạn này phù hợp hơn khi chạy trên môi trường deploy online như Render, đặc biệt là gói miễn phí hoặc server có tài nguyên thấp.

---

## Cảnh báo khi export Excel trên Render

Khi chạy project ở môi trường local, chức năng export Excel có thể xử lý được khoảng thời gian dài hơn tùy cấu hình máy.

Tuy nhiên, khi deploy project lên **Render**, đặc biệt với gói miễn phí hoặc server có tài nguyên thấp, chức năng export Excel có thể **không xuất được dữ liệu trong nhiều năm** nếu khoảng thời gian quá dài.

Nguyên nhân có thể đến từ:

- Dữ liệu lịch sử quá nhiều dòng.
- File Excel tạo ra quá nặng.
- Thời gian xử lý dữ liệu quá lâu.
- Server deploy bị giới hạn CPU hoặc RAM.
- Request bị timeout trước khi file Excel được tạo xong.
- Nguồn dữ liệu bên ngoài phản hồi chậm hoặc không ổn định.
- Render có giới hạn tài nguyên tùy theo gói sử dụng.

Vì vậy, khi sử dụng bản deploy online trên Render, nên export dữ liệu theo khoảng thời gian vừa phải, ví dụ:

```text
3 tháng
6 tháng
1 năm
```

Không nên export một lần quá nhiều năm trên bản deploy Render.

Ví dụ nên dùng:

```text
VIC từ 2024-01-01 đến 2024-12-31
```

Hạn chế dùng:

```text
VIC từ 2015-01-01 đến 2024-12-31
```

Nếu cần export dữ liệu trong nhiều năm, nên chạy project ở môi trường local để có tài nguyên ổn định hơn.

> Lưu ý: Đây là giới hạn khi chạy trên môi trường deploy có tài nguyên hạn chế, không phải lỗi mất chức năng export Excel của project.

---

## Tùy chỉnh giới hạn export khi chạy local

Mặc định project đang giới hạn export tối đa **10 năm** và **10.000 dòng** để đảm bảo an toàn khi deploy online.

Nếu người dùng tải project về máy cá nhân, máy có cấu hình mạnh hơn hoặc chạy trên server/VPS có tài nguyên tốt hơn, có thể tự tăng giới hạn export lên mức cao hơn, ví dụ:

```text
20 năm
30 năm
20.000 dòng
30.000 dòng
```

Tuy nhiên, việc tăng giới hạn có thể làm:

- Thời gian export lâu hơn.
- File Excel nặng hơn.
- Tốn nhiều RAM hơn.
- Tốn nhiều CPU hơn.
- Dễ bị timeout nếu chạy trên server yếu.
- Trình duyệt có thể phải chờ lâu khi tải file.

### Vị trí chỉnh giới hạn ở Backend

Mở file:

```text
backend/utils/validators.py
```

Tìm các dòng tương tự:

```python
MAX_EXPORT_DAYS = 365 * 10
MAX_EXPORT_ROWS = 10000
```

Nếu muốn tăng lên khoảng 20 năm và 20.000 dòng:

```python
MAX_EXPORT_DAYS = 365 * 20
MAX_EXPORT_ROWS = 20000
```

Nếu muốn tăng lên khoảng 30 năm và 30.000 dòng:

```python
MAX_EXPORT_DAYS = 365 * 30
MAX_EXPORT_ROWS = 30000
```

### Vị trí chỉnh giới hạn ở Frontend

Mở file:

```text
frontend/src/hooks/useStockAnalysis.js
```

Tìm dòng tương tự:

```javascript
const MAX_EXPORT_DAYS = 365 * 10;
```

Nếu muốn tăng lên 20 năm:

```javascript
const MAX_EXPORT_DAYS = 365 * 20;
```

Nếu muốn tăng lên 30 năm:

```javascript
const MAX_EXPORT_DAYS = 365 * 30;
```

### Khuyến nghị

Nếu chạy trên Render hoặc server yếu:

```text
Nên giữ mặc định: 10 năm / 10.000 dòng
```

Nếu chạy local trên máy mạnh hơn:

```text
Có thể thử: 20 năm / 20.000 dòng
```

Nếu chạy trên máy rất mạnh hoặc server riêng:

```text
Có thể thử: 30 năm / 30.000 dòng
```

Sau khi tăng giới hạn, nên test lại chức năng export Excel với từng khoảng thời gian nhỏ trước, sau đó mới tăng dần.

---

## Deploy lên Render

Project có sẵn file `render.yaml` để hỗ trợ deploy lên Render.

### Backend

Backend sử dụng Flask và có thể chạy bằng Gunicorn:

```bash
gunicorn --workers 2 --threads 4 --timeout 60 app:app
```

### Frontend

Frontend sử dụng Vite và có thể build bằng lệnh:

```bash
npm install && npm run build
```

Thư mục build mặc định:

```text
dist
```

---

## Biến môi trường

### Backend

Có thể cấu hình các biến môi trường sau:

```env
FRONTEND_URL=http://localhost:5173
CORS_EXTRA_ORIGINS=http://127.0.0.1:5173
STOCK_CACHE_TTL_SECONDS=60
RATELIMIT_DEFAULT=120 per minute
RATELIMIT_DAILY=1000 per day
LOG_LEVEL=INFO
```

### Frontend

Tạo file `.env` trong thư mục `frontend`:

```env
VITE_API_URL=http://127.0.0.1:5000
```

Khi deploy online, thay `VITE_API_URL` bằng URL backend thật.

Ví dụ:

```env
VITE_API_URL=https://your-backend-url.onrender.com
```

---

## Một số lệnh hữu ích

### Chạy backend local

```bash
cd backend
python app.py
```

### Cài lại thư viện backend

```bash
cd backend
pip install -r requirements.txt
```

### Chạy frontend local

```bash
cd frontend
npm run dev
```

### Cài lại package frontend

```bash
cd frontend
npm install
```

### Build frontend

```bash
cd frontend
npm run build
```

### Kiểm tra lint frontend

```bash
cd frontend
npm run lint
```

---

## Lưu ý sử dụng

- Dữ liệu phụ thuộc vào nguồn dữ liệu bên ngoài nên có thể bị trễ, thiếu hoặc không phản hồi ở một số thời điểm.
- Một số mã cổ phiếu có thể không có đủ dữ liệu lịch sử để phân tích đầy đủ.
- Một số chỉ báo rolling như MA5, MA10, MA20, RSI14 cần đủ số phiên lịch sử nên các dòng đầu kỳ có thể bị trống. Đây là đặc điểm tính toán bình thường, không phải lỗi dữ liệu.
- Các chỉ báo kỹ thuật chỉ mang tính tham khảo.
- Kết quả phân tích không phải là khuyến nghị mua bán chứng khoán.
- Người dùng cần tự chịu trách nhiệm với quyết định đầu tư của mình.
- Khi export Excel trên môi trường deploy online, nên chọn khoảng thời gian vừa phải để tránh lỗi timeout.
- Nếu muốn export nhiều năm dữ liệu, nên chạy local hoặc dùng server có tài nguyên mạnh hơn.

---

## Định hướng phát triển thêm

Một số tính năng có thể phát triển thêm trong tương lai:

- Thêm nhiều nguồn dữ liệu chứng khoán.
- Thêm chức năng so sánh nhiều mã cổ phiếu.
- Thêm đăng nhập người dùng.
- Lưu lịch sử phân tích.
- Tối ưu export Excel cho dữ liệu nhiều năm.
- Tối ưu hiệu năng khi deploy online.
- Thêm dashboard tổng quan thị trường.
- Thêm bộ lọc cổ phiếu theo ngành hoặc nhóm chỉ số.
- Cho phép cấu hình giới hạn export bằng biến môi trường.

---

## Tác giả

**Đoàn Anh Tuấn**

- GitHub: https://github.com/tuanda2309
- Repository: https://github.com/tuanda2309/Vietnam_Stock_Data_Analysis_Terminal_VSDAT.git

---

## License

Dự án này được phát hành theo giấy phép **MIT License**.

Bạn có thể xem chi tiết trong file [LICENSE](LICENSE).

---

## Tuyên bố miễn trừ trách nhiệm

Dự án này chỉ phục vụ mục đích học tập, nghiên cứu và tham khảo dữ liệu.

Các kết quả phân tích, chỉ báo kỹ thuật, vùng giá tham khảo hoặc nhận xét trong ứng dụng **không phải là khuyến nghị đầu tư**.

Người dùng cần tự nghiên cứu và tự chịu trách nhiệm với mọi quyết định đầu tư của mình.