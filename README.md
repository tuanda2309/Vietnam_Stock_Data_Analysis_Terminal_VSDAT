# Vietnam Stock Data Analysis Terminal (VSDAT)

A full-stack web application for analyzing Vietnamese stock market data, displaying technical indicators, visualizing historical price movements, and exporting OHLCV data to Excel for data analysis purposes.

> **Disclaimer:** This project is for educational and data analysis purposes only. It is not financial advice.

---

## Project Overview

**Vietnam Stock Data Analysis Terminal (VSDAT)** is a web-based stock data analysis application designed for Vietnamese stock market data. The application allows users to enter a stock symbol, retrieve price data, view current price information, analyze price movement, inspect technical indicators, and export historical data to Excel.

This project was built as a portfolio project to demonstrate skills in:

- Full-stack web development
- REST API development
- Data processing with Python
- Financial data visualization
- Technical indicator calculation
- Excel report generation
- Production deployment on Render

VSDAT is not designed to provide investment recommendations. All insights and indicators are for learning, research, and data analysis practice only.

---

## Key Features

- Search Vietnamese stock symbols
- Display current stock price
- Show price change and percentage change
- Identify stock movement status: up, down, or unchanged
- Technical analysis dashboard
- RSI indicator for momentum analysis
- Moving averages such as MA20, MA50, MA100, and MA200
- MACD indicator for trend analysis
- Bollinger Bands for volatility analysis
- Historical price chart
- OHLCV data processing
- Excel export for historical stock data
- Loading and error handling states
- Input validation for stock symbols and export dates
- Backend API health check endpoint
- Production deployment on Render

---

## Screenshots

| Main Query Interface | Technical Analysis Dashboard |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/07defeb9-a194-4e39-8978-65ba8af11b10" width="100%" alt="VSDAT Home Interface" /> | <img src="https://github.com/user-attachments/assets/0b1b5455-425c-4893-b947-d54d2acbaa49" width="100%" alt="VSDAT Technical Analysis Dashboard" /> |
| Stock symbol input and Excel export controls | Main dashboard with technical analysis cards and charts |

| RSI Indicator Chart | Generated Excel Report |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/30219a3f-dc33-4bb2-bd7a-56bfcf78d824" width="100%" alt="VSDAT RSI Indicator Chart" /> | <img src="https://github.com/user-attachments/assets/a5f6e01f-8570-42f9-b69f-19b377dc01d8" width="100%" alt="VSDAT Generated Excel Sheet" /> |
| RSI visualization for momentum analysis | Exported OHLCV Excel file for further analysis |

---

## Tech Stack

### Frontend

- React
- Vite
- Tailwind CSS
- Axios
- JavaScript

### Backend

- Python 3.10.12
- Flask
- Flask-CORS
- Gunicorn
- Flask-Limiter

### Data Processing

- Pandas
- NumPy
- vnstock / Vietnamese stock data API

### Excel Export

- openpyxl
- BytesIO for in-memory file generation

### Deployment

- Render

---

## System Architecture

```txt
User Browser
    |
    |  React/Vite Frontend
    |  https://vsdat-frontend.onrender.com
    |
    |  Axios HTTP Requests
    v
Flask Backend API
    |
    |  Stock data fetching and processing
    |  Technical indicator calculation
    |  Excel report generation
    |
    v
Vietnamese Stock Data Source
    |
    v
Processed JSON Response / Excel File
```

The frontend communicates with the backend through REST API endpoints. The backend retrieves stock data, processes it using Pandas and NumPy, calculates indicators, and returns structured JSON data to the frontend.

---

## Folder Structure

```txt
VSDAT/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── config.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── config/
│   └── .env.example
│
├── render.yaml
├── .gitignore
└── README.md
```

---

## Installation and Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.10.12
- Node.js
- npm
- Git

---

## Environment Variables

### Frontend

Create a `.env` file inside the `frontend/` directory:

```env
VITE_API_URL=https://vsdat-backend-1.onrender.com
```

For local development:

```env
VITE_API_URL=http://127.0.0.1:5000
```

### Backend

Environment variables for production:

```env
FRONTEND_URL=https://vsdat-frontend.onrender.com
FLASK_ENV=production
PYTHON_VERSION=3.10.12
```

Optional backend variables:

```env
CORS_EXTRA_ORIGINS=
STOCK_CACHE_TTL_SECONDS=60
RATELIMIT_DEFAULT=120 per minute
RATELIMIT_DAILY=1000 per day
```

Do not commit real `.env` files to GitHub.

---

## Running Locally

### Backend Setup

```bash
cd backend
python -m venv venv
```

Activate virtual environment on Windows:

```bash
venv\Scripts\activate
```

Activate virtual environment on macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Flask backend:

```bash
python app.py
```

The backend should run at:

```txt
http://127.0.0.1:5000
```

Test backend health check:

```bash
curl http://127.0.0.1:5000/health
```

---

### Frontend Setup

```bash
cd frontend
npm install
```

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

For Windows PowerShell:

```powershell
copy .env.example .env
```

Run frontend development server:

```bash
npm run dev
```

Build frontend for production:

```bash
npm run build
```

---

## Deployment

### Backend on Render

Create a new Render Web Service for the backend.

Recommended backend settings:

```txt
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Python Version: 3.10.12
```

Environment variables:

```env
FRONTEND_URL=https://vsdat-frontend.onrender.com
FLASK_ENV=production
PYTHON_VERSION=3.10.12
```

Backend production URL:

```txt
https://vsdat-backend-1.onrender.com
```

---

### Frontend on Render

Create a new Render Static Site for the frontend.

Recommended frontend settings:

```txt
Build Command: npm install && npm run build
Publish Directory: dist
```

Environment variable:

```env
VITE_API_URL=https://vsdat-backend-1.onrender.com
```

Frontend production URL:

```txt
https://vsdat-frontend.onrender.com
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

---

### Get Stock Analysis

```http
GET /stock/<symbol>
```

Example:

```http
GET /stock/VIC
```

Example response:

```json
{
  "symbol": "VIC",
  "currentPrice": 218700,
  "referencePrice": 226700,
  "previousClose": 226700,
  "priceChange": -8000,
  "percentChange": -3.53,
  "status": "down",
  "color": "red",
  "rsi": 45.2,
  "ma20": 220000,
  "data": []
}
```

Status and color logic:

```txt
priceChange > 0  -> status = "up", color = "green"
priceChange < 0  -> status = "down", color = "red"
priceChange == 0 -> status = "unchanged", color = "yellow" or "gray"
```

---

### Export Historical Data to Excel

```http
GET /export/<symbol>/<start_date>/<end_date>
```

Example:

```http
GET /export/VIC/2024-01-01/2024-12-31
```

The API returns an Excel file containing historical OHLCV data.

Date format:

```txt
YYYY-MM-DD
```

---

## Excel Export Feature

The Excel export feature allows users to download historical stock data for further analysis.

The exported file may include:

- Stock symbol
- Date
- Open price
- High price
- Low price
- Close price
- Volume
- Basic formatting for readability
- Educational disclaimer

The Excel file is generated in memory using `BytesIO`, which avoids writing temporary files to the server disk.

---

## Data Analysis Features

VSDAT processes Vietnamese stock data and provides common data analysis indicators.

Main analysis features include:

- OHLCV data cleaning
- Missing value handling
- Date and numeric type normalization
- Price change calculation
- Percentage change calculation
- Moving averages
- RSI indicator
- MACD indicator
- Bollinger Bands
- Historical chart data preparation
- Basic reference insights for analysis practice

These indicators are intended to support learning and analytical exploration, not investment decision-making.

---

## Limitations

- Stock data availability depends on the external Vietnamese stock data source.
- Real-time accuracy may vary depending on the data provider.
- The application may be affected by API rate limits or temporary provider downtime.
- Render free tier services may sleep after inactivity.
- Technical indicators are for reference only.
- The project does not provide buy, sell, or hold recommendations.
- Historical performance does not guarantee future results.

---

## Disclaimer

This project is for educational and data analysis purposes only. It is not financial advice.

The information, charts, indicators, and exported data are provided for learning, research, and portfolio demonstration purposes. Users should not rely on this application as a source of financial, investment, or trading advice.

---

## Future Improvements

Possible future improvements:

- Add user authentication
- Add watchlist feature
- Add more advanced chart interactions
- Add Redis cache for production scalability
- Add automated testing
- Add CI/CD pipeline
- Add more technical indicators
- Add market overview dashboard
- Add comparison between multiple stock symbols
- Add downloadable PDF reports
- Improve mobile UI and accessibility
- Add monitoring and error tracking

---

## Author

**Đoàn Anh Tuấn**

- Email: doananhtuan77qn@gmail.com
- GitHub: [Your GitHub Profile](https://github.com/tuanda2309)

---

<br />

# Vietnam Stock Data Analysis Terminal (VSDAT) - Tiếng Việt

Ứng dụng web full-stack dùng để phân tích dữ liệu chứng khoán Việt Nam, hiển thị chỉ báo kỹ thuật, trực quan hóa biến động giá lịch sử và xuất dữ liệu OHLCV ra file Excel phục vụ mục đích phân tích dữ liệu.

> **Lưu ý rủi ro:** Dự án chỉ phục vụ mục đích học tập và phân tích dữ liệu, không phải khuyến nghị đầu tư.

---

## Tên dự án

**Vietnam Stock Data Analysis Terminal (VSDAT)**

---

## Tổng quan dự án

**VSDAT** là ứng dụng web phân tích dữ liệu chứng khoán Việt Nam. Ứng dụng cho phép người dùng nhập mã cổ phiếu, lấy dữ liệu giá, xem giá hiện tại, trạng thái tăng/giảm, các chỉ báo kỹ thuật, biểu đồ phân tích và xuất dữ liệu lịch sử ra file Excel.

Dự án được xây dựng nhằm thể hiện các kỹ năng:

- Phát triển web full-stack
- Xây dựng REST API với Flask
- Xử lý dữ liệu bằng Python
- Trực quan hóa dữ liệu tài chính
- Tính toán chỉ báo kỹ thuật
- Xuất báo cáo Excel
- Deploy ứng dụng production basic trên Render

VSDAT không phải là công cụ đưa ra khuyến nghị đầu tư. Các chỉ báo và nhận xét trong ứng dụng chỉ phục vụ học tập, nghiên cứu và thực hành phân tích dữ liệu.

---

## Tính năng chính

- Tra cứu mã cổ phiếu Việt Nam
- Hiển thị giá hiện tại
- Hiển thị mức tăng/giảm và phần trăm thay đổi
- Xác định trạng thái cổ phiếu: tăng, giảm hoặc không đổi
- Dashboard phân tích kỹ thuật
- Chỉ báo RSI để phân tích động lượng
- Đường trung bình động như MA20, MA50, MA100 và MA200
- Chỉ báo MACD để phân tích xu hướng
- Bollinger Bands để phân tích biến động giá
- Biểu đồ giá lịch sử
- Xử lý dữ liệu OHLCV
- Xuất dữ liệu lịch sử ra Excel
- Trạng thái loading và error rõ ràng
- Validate mã cổ phiếu và ngày xuất dữ liệu
- API kiểm tra trạng thái backend
- Deploy production trên Render

---

## Hình ảnh giao diện

| Giao diện tra cứu chính | Dashboard phân tích kỹ thuật |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/07defeb9-a194-4e39-8978-65ba8af11b10" width="100%" alt="VSDAT Home Interface" /> | <img src="https://github.com/user-attachments/assets/0b1b5455-425c-4893-b947-d54d2acbaa49" width="100%" alt="VSDAT Technical Analysis Dashboard" /> |
| Nhập mã cổ phiếu và điều khiển xuất Excel | Dashboard chính với thẻ phân tích kỹ thuật và biểu đồ |

| Biểu đồ chỉ báo RSI | File Excel được tạo |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/30219a3f-dc33-4bb2-bd7a-56bfcf78d824" width="100%" alt="VSDAT RSI Indicator Chart" /> | <img src="https://github.com/user-attachments/assets/a5f6e01f-8570-42f9-b69f-19b377dc01d8" width="100%" alt="VSDAT Generated Excel Sheet" /> |
| Trực quan hóa RSI để phân tích động lượng | File Excel OHLCV được xuất để tiếp tục phân tích |

---

## Công nghệ sử dụng

### Frontend

- React
- Vite
- Tailwind CSS
- Axios
- JavaScript

### Backend

- Python 3.10.12
- Flask
- Flask-CORS
- Gunicorn
- Flask-Limiter

### Xử lý dữ liệu

- Pandas
- NumPy
- vnstock / API dữ liệu chứng khoán Việt Nam

### Xuất Excel

- openpyxl
- BytesIO để tạo file trong bộ nhớ

### Deploy

- Render

---

## Kiến trúc hệ thống

```txt
Trình duyệt người dùng
    |
    |  React/Vite Frontend
    |  https://vsdat-frontend.onrender.com
    |
    |  Gửi request bằng Axios
    v
Flask Backend API
    |
    |  Lấy và xử lý dữ liệu chứng khoán
    |  Tính toán chỉ báo kỹ thuật
    |  Tạo file Excel
    |
    v
Nguồn dữ liệu chứng khoán Việt Nam
    |
    v
JSON Response / File Excel
```

Frontend giao tiếp với backend thông qua REST API. Backend lấy dữ liệu chứng khoán, xử lý bằng Pandas và NumPy, tính toán các chỉ báo kỹ thuật, sau đó trả dữ liệu dạng JSON cho frontend hoặc file Excel cho người dùng tải về.

---

## Cấu trúc thư mục

```txt
VSDAT/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── config.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── config/
│   └── .env.example
│
├── render.yaml
├── .gitignore
└── README.md
```

---

## Cài đặt và chạy project

### Yêu cầu trước khi chạy

Bạn cần cài đặt:

- Python 3.10.12
- Node.js
- npm
- Git

---

## Biến môi trường

### Frontend

Tạo file `.env` trong thư mục `frontend/`:

```env
VITE_API_URL=https://vsdat-backend-1.onrender.com
```

Khi chạy local:

```env
VITE_API_URL=http://127.0.0.1:5000
```

### Backend

Biến môi trường cho production:

```env
FRONTEND_URL=https://vsdat-frontend.onrender.com
FLASK_ENV=production
PYTHON_VERSION=3.10.12
```

Biến môi trường tùy chọn:

```env
CORS_EXTRA_ORIGINS=
STOCK_CACHE_TTL_SECONDS=60
RATELIMIT_DEFAULT=120 per minute
RATELIMIT_DAILY=1000 per day
```

Không commit file `.env` thật lên GitHub.

---

## Chạy local

### Chạy Backend

```bash
cd backend
python -m venv venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
venv\Scripts\activate
```

Kích hoạt môi trường ảo trên macOS/Linux:

```bash
source venv/bin/activate
```

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

Chạy Flask backend:

```bash
python app.py
```

Backend sẽ chạy tại:

```txt
http://127.0.0.1:5000
```

Kiểm tra backend:

```bash
curl http://127.0.0.1:5000/health
```

---

### Chạy Frontend

```bash
cd frontend
npm install
```

Tạo file `.env` từ `.env.example`:

```bash
cp .env.example .env
```

Với Windows PowerShell:

```powershell
copy .env.example .env
```

Chạy frontend:

```bash
npm run dev
```

Build frontend:

```bash
npm run build
```

---

## Deploy

### Deploy Backend trên Render

Tạo Web Service mới trên Render cho backend.

Cấu hình đề xuất:

```txt
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Python Version: 3.10.12
```

Biến môi trường:

```env
FRONTEND_URL=https://vsdat-frontend.onrender.com
FLASK_ENV=production
PYTHON_VERSION=3.10.12
```

Backend production URL:

```txt
https://vsdat-backend-1.onrender.com
```

---

### Deploy Frontend trên Render

Tạo Static Site mới trên Render cho frontend.

Cấu hình đề xuất:

```txt
Build Command: npm install && npm run build
Publish Directory: dist
```

Biến môi trường:

```env
VITE_API_URL=https://vsdat-backend-1.onrender.com
```

Frontend production URL:

```txt
https://vsdat-frontend.onrender.com
```

---

## API endpoints

### Health Check

```http
GET /health
```

Ví dụ response:

```json
{
  "status": "ok"
}
```

---

### Lấy dữ liệu phân tích cổ phiếu

```http
GET /stock/<symbol>
```

Ví dụ:

```http
GET /stock/VIC
```

Ví dụ response:

```json
{
  "symbol": "VIC",
  "currentPrice": 218700,
  "referencePrice": 226700,
  "previousClose": 226700,
  "priceChange": -8000,
  "percentChange": -3.53,
  "status": "down",
  "color": "red",
  "rsi": 45.2,
  "ma20": 220000,
  "data": []
}
```

Logic trạng thái và màu:

```txt
priceChange > 0  -> status = "up", color = "green"
priceChange < 0  -> status = "down", color = "red"
priceChange == 0 -> status = "unchanged", color = "yellow" hoặc "gray"
```

---

### Xuất dữ liệu lịch sử ra Excel

```http
GET /export/<symbol>/<start_date>/<end_date>
```

Ví dụ:

```http
GET /export/VIC/2024-01-01/2024-12-31
```

API sẽ trả về file Excel chứa dữ liệu lịch sử OHLCV.

Định dạng ngày:

```txt
YYYY-MM-DD
```

---

## Chức năng xuất Excel

Chức năng xuất Excel cho phép người dùng tải dữ liệu lịch sử của cổ phiếu để tiếp tục phân tích.

File Excel có thể bao gồm:

- Mã cổ phiếu
- Ngày giao dịch
- Giá mở cửa
- Giá cao nhất
- Giá thấp nhất
- Giá đóng cửa
- Khối lượng giao dịch
- Định dạng bảng dễ đọc
- Disclaimer phục vụ mục đích học tập và phân tích

File Excel được tạo trong bộ nhớ bằng `BytesIO`, giúp tránh việc ghi file tạm lên ổ đĩa server.

---

## Tính năng phân tích dữ liệu

VSDAT xử lý dữ liệu chứng khoán Việt Nam và cung cấp các chỉ báo phân tích phổ biến.

Các tính năng phân tích chính gồm:

- Làm sạch dữ liệu OHLCV
- Xử lý missing value
- Chuẩn hóa kiểu dữ liệu ngày và số
- Tính toán thay đổi giá
- Tính toán phần trăm thay đổi
- Đường trung bình động
- Chỉ báo RSI
- Chỉ báo MACD
- Bollinger Bands
- Chuẩn bị dữ liệu cho biểu đồ lịch sử
- Nhận xét tham khảo phục vụ thực hành phân tích dữ liệu

Các chỉ báo này chỉ hỗ trợ học tập và phân tích tham khảo, không dùng để ra quyết định đầu tư.

---

## Hạn chế

- Dữ liệu chứng khoán phụ thuộc vào nguồn dữ liệu bên ngoài.
- Độ chính xác realtime có thể thay đổi tùy theo nhà cung cấp dữ liệu.
- Ứng dụng có thể bị ảnh hưởng bởi giới hạn request hoặc lỗi tạm thời từ API dữ liệu.
- Render free tier có thể sleep sau một thời gian không hoạt động.
- Chỉ báo kỹ thuật chỉ mang tính tham khảo.
- Dự án không đưa ra khuyến nghị mua, bán hoặc nắm giữ cổ phiếu.
- Hiệu suất trong quá khứ không đảm bảo kết quả trong tương lai.

---

## Lưu ý rủi ro

Dự án chỉ phục vụ mục đích học tập và phân tích dữ liệu, không phải khuyến nghị đầu tư.

Thông tin, biểu đồ, chỉ báo và dữ liệu xuất ra từ ứng dụng chỉ phục vụ học tập, nghiên cứu và trình bày năng lực cá nhân trong portfolio. Người dùng không nên xem ứng dụng này là nguồn tư vấn tài chính, đầu tư hoặc giao dịch.

---

## Hướng phát triển

Một số hướng phát triển trong tương lai:

- Thêm đăng nhập người dùng
- Thêm danh sách cổ phiếu theo dõi
- Cải thiện tương tác biểu đồ
- Thêm Redis cache cho production
- Thêm automated testing
- Thêm CI/CD pipeline
- Bổ sung nhiều chỉ báo kỹ thuật hơn
- Thêm dashboard tổng quan thị trường
- So sánh nhiều mã cổ phiếu
- Xuất báo cáo PDF
- Cải thiện giao diện mobile và accessibility
- Thêm monitoring và error tracking

---

## Tác giả

**Đoàn Anh Tuấn**

- Email: doananhtuan77qn@gmail.com
- GitHub: [Your GitHub Profile](https://github.com/tuanda2309)