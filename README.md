# Vietnam Stock Data Analysis Terminal (VSDAT)

**A Data Analytics Portfolio Project for Time-Series Analysis & Financial Indicator Automation**

[English](#english) | [Tiếng Việt](#tiếng-việt)

---

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind--CSS-3.4+-06B6D4?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com/)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)](#)

---

## 🌐 Live Demo

Experience the application here: **[VSDAT Live Web App](https://vsdat-frontend.onrender.com)**

---

# English

## 📌 Table of Contents

1. [Overview](#overview)
2. [Project Motivation](#project-motivation)
3. [Data Analyst Perspective](#data-analyst-perspective)
4. [Data Analytics Workflow](#data-analytics-workflow)
5. [Key Features](#key-features)
6. [Visualizations & Screenshots](#visualizations--screenshots)
7. [Excel Export for Advanced Analytics](#excel-export-for-advanced-analytics)
8. [Tech Stack](#tech-stack)
9. [System Architecture & Data Flow](#system-architecture--data-flow)
10. [API Endpoints](#api-endpoints)
11. [Project Structure](#project-structure)
12. [Getting Started](#getting-started)
13. [Environment Variables](#environment-variables)
14. [Disclaimer](#disclaimer)
15. [Author](#author)

---

## Overview

**Vietnam Stock Data Analysis Terminal (VSDAT)** is a mini data analytics product designed to collect, process, calculate, and visualize historical time-series financial data from the Vietnamese stock market.

Users can search for valid stock symbols such as `VIC`, `FPT`, or `VNM`. The system then displays an interactive dashboard containing price information, price changes, technical indicators, and historical data visualizations.

In addition to the dashboard, VSDAT supports automated Excel report generation, allowing users to continue analyzing the data with Excel, Pivot Tables, Power BI, Tableau, or other BI tools.

---

## Project Motivation

Many stock market dashboards focus heavily on interface design or market summaries, but provide limited access to clean, structured data for further analysis.

**VSDAT** was built to combine:

- Stock data retrieval
- Data cleaning and transformation with Python
- Time-series analysis
- Technical indicator calculation
- Dashboard visualization
- Automated Excel reporting

This project demonstrates how a Data Analyst can build an end-to-end analytics workflow, from backend data processing to frontend visualization and report generation.

---

## Data Analyst Perspective

This project highlights practical skills required for a **Junior Data Analyst / Data Analyst Intern** role:

- **Data Integration:** Connect to external stock data sources through APIs or financial data libraries.
- **Data Cleaning:** Standardize datetime values, convert numeric fields, and prepare price and volume data.
- **Data Transformation:** Convert raw market data into analysis-ready datasets.
- **Time-Series Analysis:** Sort, structure, and analyze stock price movement over time.
- **Technical Indicator Calculation:** Calculate RSI and moving averages such as `MA20`, `MA50`, `MA100`, and `MA200` using `Pandas` and `NumPy`.
- **Dashboard Visualization:** Build interactive charts for price trends, volume, and market momentum.
- **Excel Report Automation:** Export structured Excel reports for additional analysis in Excel, Pivot Tables, or Power BI.

---

## Data Analytics Workflow

VSDAT follows a clear data processing pipeline:

```text
[Data Source: VCI API via vnstock]
│
▼
[Data Ingestion Layer]
Fetches historical OHLCV stock data
│
▼
[Data Cleaning Layer]
Parses dates, converts numeric values, and standardizes prices
│
▼
[Data Transformation Layer]
Calculates price changes, percentage changes, RSI, and moving averages
│
▼
[Data Presentation Layer]
Converts processed data into chart-ready JSON payloads
│
▼
[Dashboard Layer]
Displays KPI cards, price charts, volume charts, and RSI charts
│
▼
[Excel Reporting Layer]
Exports cleaned data into formatted Excel files
```

---

## Key Features

- **Stock Symbol Search:** Accepts user input, removes extra whitespace, and normalizes stock symbols to uppercase.
- **Latest Price Display:** Shows the latest available stock price from the processed data.
- **Price Change Calculation:** Displays price change and percentage change compared with the reference price.
- **RSI Indicator:** Calculates the 14-period RSI to help monitor momentum conditions.
- **Moving Averages:** Calculates `MA20`, `MA50`, `MA100`, and `MA200` for trend analysis.
- **Time-Series Visualization:** Displays closing prices, trading volume, and moving averages.
- **RSI Visualization:** Shows RSI movement over time with overbought and oversold reference zones.
- **Excel Export:** Exports historical stock data by selected date range into a formatted Excel workbook.
- **Dark-Themed Dashboard:** Provides a financial dashboard interface suitable for stock data visualization.
- **Online Deployment:** The application is deployed online and can be accessed directly through a browser.

---

## Visualizations & Screenshots

| 1. Main Query Interface | 2. Technical Analysis Dashboard |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/07defeb9-a194-4e39-8978-65ba8af11b10" width="100%" alt="VSDAT Home Interface" /> | <img src="https://github.com/user-attachments/assets/0b1b5455-425c-4893-b947-d54d2acbaa49" width="100%" alt="VSDAT Quantitative Analysis Dashboard" /> |
| **Title:** Stock Query & Excel Export Interface<br>**Data Analyst Context:** This screen represents the data input layer where users define the stock symbol and reporting date range. | **Title:** Technical Analysis Dashboard<br>**Data Analyst Context:** Displays key metrics, price movement, volume, RSI, and moving averages for decision-support analysis. |

| 3. RSI Indicator Chart | 4. Generated Excel Report |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/30219a3f-dc33-4bb2-bd7a-56bfcf78d824" width="100%" alt="VSDAT RSI Indicator Chart" /> | <img src="https://github.com/user-attachments/assets/a5f6e01f-8570-42f9-b69f-19b377dc01d8" width="100%" alt="VSDAT Generated Excel Sheet" /> |
| **Title:** RSI Momentum Visualization<br>**Data Analyst Context:** Shows RSI movement over time and helps identify overbought, oversold, or neutral market conditions. | **Title:** Automated Excel Analytical Report<br>**Data Analyst Context:** Provides clean OHLCV data, price changes, percentage changes, and volume for further analysis. |

---

## Excel Export for Advanced Analytics

One important feature of VSDAT is the automated Excel export pipeline. Instead of limiting users to the dashboard, VSDAT allows them to download structured data for further analysis.

The exported Excel file includes:

- Trading date
- Open price
- High price
- Low price
- Close price
- Price change
- Percentage change
- Trading volume

Benefits for Data Analysts:

- **Clean Data Output:** Data is processed and formatted before export.
- **Ready for Further Analysis:** Users can filter, sort, create Pivot Tables, or build charts in Excel.
- **BI Integration:** The exported file can be imported into Power BI, Tableau, or other analytics tools.
- **Report Automation:** Reduces manual work when collecting historical stock data.
- **Practical Portfolio Value:** Demonstrates an end-to-end workflow from data processing to report delivery.

---

## Tech Stack

### Backend - Analytical Engine

- **Language:** Python 3.10
- **Framework:** Flask
- **Data Processing:** Pandas, NumPy
- **Excel Export:** OpenPyXL
- **Stock Data Source:** vnstock / vnstock3
- **Deployment:** Render

### Frontend - Dashboard Interface

- **Framework:** React 18
- **Build Tool:** Vite
- **API Client:** Axios
- **Charts:** Recharts
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Deployment:** Render

---

## System Architecture & Data Flow

VSDAT is built using a decoupled client-server architecture:

1. The user enters a stock symbol on the React frontend.
2. The frontend sends an API request to the Flask backend.
3. The backend retrieves stock data through `vnstock / vnstock3`.
4. `Pandas` and `NumPy` process the data and calculate RSI, moving averages, and price changes.
5. The backend returns structured JSON data to the frontend.
6. Recharts visualizes price, volume, moving averages, and RSI.
7. When the user exports data, the backend generates an Excel file using `OpenPyXL`.

---

## API Endpoints

### 1. Retrieve Stock Analysis Data

- **Path:** `GET /stock/<symbol>`
- **Description:** Retrieves stock data, processes the time-series data, calculates indicators, and returns JSON data for the dashboard.
- **Response Status:** `200 OK` / `400 Bad Request` / `442 Unprocessable Content`

Example response:

```json
{
  "color": "green",
  "currentPrice": 227900.0,
  "ma20": 218040.0,
  "percentChange": 1.24,
  "priceChange": 2800.0,
  "referencePrice": 225100.0,
  "rsi": 70.51,
  "status": "up",
  "symbol": "VIC",
  "data": [
    {
      "time": "2026-02-25",
      "open": 159000.0,
      "high": 161000.0,
      "low": 157000.0,
      "close": 158000.0,
      "volume": 5289800.0,
      "MA20": 146490.0,
      "MA50": 138200.0,
      "MA100": 131130.0,
      "MA200": 93179.0,
      "RSI": 68.4
    }
  ]
}
```

### 2. Export Excel Report

- **Path:** `GET /export/<symbol>/<start_date>/<end_date>`
- **Response Type:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- **Description:** Dynamically generates an Excel workbook from historical stock data and returns it as a downloadable file.

Example:

```text
/export/VIC/2025-01-01/2025-12-31
```

---

## Project Structure

```bash
VSDAT-Terminal/
├── backend/
│   ├── app.py                 # Flask server, API routes, and analytical logic
│   ├── requirements.txt       # Python dependencies
│   └── runtime.txt            # Runtime version for deployment
└── frontend/
    ├── src/
    │   ├── App.jsx            # Dashboard UI and user interaction logic
    │   ├── index.css          # Tailwind CSS configuration
    │   └── main.jsx           # React application entry point
    ├── package.json           # Frontend dependencies
    ├── tailwind.config.js     # Tailwind CSS configuration
    └── vite.config.js         # Vite build configuration
```

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js v18 or higher
- Git

### 1. Run the Backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate
```

```bash
# macOS / Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
python app.py
```

The backend will run at:

```text
http://127.0.0.1:5000
```

### 2. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

---

## Environment Variables

### Backend

```env
PORT=5000
DEVELOPER_EMAIL=doananhtuan77qn@gmail.com
DEVELOPER_PHONE=0399848871
DEVELOPER_GITHUB=https://github.com/tuanda2309
DEVELOPER_WEB=https://vsdat-frontend.onrender.com
```

### Frontend

```env
VITE_API_URL=https://your-backend-url.onrender.com
```

For local development:

```env
VITE_API_URL=http://127.0.0.1:5000
```

---

## Disclaimer

**This project is built for educational purposes, Data Analytics practice, and personal portfolio presentation only.**

VSDAT is **not** an investment advisory tool. It does not provide buy/sell recommendations and does not replace professional financial analysis platforms.

All data and indicators are calculated automatically and should only be used for reference, learning, data processing practice, and dashboard visualization practice.

---

## Author

- **Full Name:** Doan Anh Tuan
- **Email:** [doananhtuan77qn@gmail.com](mailto:doananhtuan77qn@gmail.com)
- **GitHub:** [tuanda2309](https://github.com/tuanda2309)
- **Live Demo:** [VSDAT Terminal Live](https://vsdat-frontend.onrender.com)

---

# Tiếng Việt

## 📌 Mục lục

1. [Tổng quan](#tổng-quan)
2. [Lý do xây dựng dự án](#lý-do-xây-dựng-dự-án)
3. [Góc nhìn Data Analyst](#góc-nhìn-data-analyst)
4. [Quy trình phân tích dữ liệu](#quy-trình-phân-tích-dữ-liệu)
5. [Tính năng chính](#tính-năng-chính)
6. [Trực quan hóa & Ảnh minh họa](#trực-quan-hóa--ảnh-minh-họa)
7. [Xuất Excel cho phân tích nâng cao](#xuất-excel-cho-phân-tích-nâng-cao)
8. [Công nghệ sử dụng](#công-nghệ-sử-dụng)
9. [Kiến trúc hệ thống & Luồng dữ liệu](#kiến-trúc-hệ-thống--luồng-dữ-liệu)
10. [API Endpoints](#api-endpoints-1)
11. [Cấu trúc dự án](#cấu-trúc-dự-án)
12. [Cài đặt và chạy Local](#cài-đặt-và-chạy-local)
13. [Biến môi trường](#biến-môi-trường)
14. [Lưu ý / Disclaimer](#lưu-ý--disclaimer)
15. [Tác giả](#tác-giả)

---

## Tổng quan

**Vietnam Stock Data Analysis Terminal (VSDAT)** là một mini data analytics product được xây dựng để thu thập, xử lý, tính toán và trực quan hóa dữ liệu tài chính dạng chuỗi thời gian của thị trường chứng khoán Việt Nam.

Người dùng có thể nhập mã cổ phiếu hợp lệ như `VIC`, `FPT`, `VNM`. Sau đó, hệ thống sẽ hiển thị dashboard phân tích gồm giá hiện tại, mức thay đổi, phần trăm thay đổi, RSI và các đường trung bình động như `MA20`, `MA50`, `MA100`, `MA200`.

Ngoài dashboard trực quan, VSDAT còn hỗ trợ **xuất báo cáo Excel tự động**, giúp Data Analyst tiếp tục phân tích dữ liệu bằng Excel, Pivot Table, Power BI hoặc các công cụ BI khác.

---

## Lý do xây dựng dự án

Nhiều dashboard chứng khoán hiện nay tập trung nhiều vào giao diện hoặc thông tin thị trường, nhưng lại thiếu phần dữ liệu sạch để người phân tích có thể tiếp tục xử lý.

**VSDAT** được xây dựng nhằm kết hợp giữa:

- Truy xuất dữ liệu chứng khoán
- Xử lý và làm sạch dữ liệu bằng Python
- Phân tích dữ liệu chuỗi thời gian
- Tính toán chỉ báo kỹ thuật
- Trực quan hóa bằng dashboard
- Xuất dữ liệu sạch ra Excel phục vụ báo cáo và phân tích tiếp theo

Dự án này thể hiện cách một Data Analyst có thể xây dựng một quy trình phân tích dữ liệu hoàn chỉnh, từ backend xử lý dữ liệu đến frontend dashboard và báo cáo Excel.

---

## Góc nhìn Data Analyst

Dự án này tập trung thể hiện các kỹ năng thực tế cần có của một **Junior Data Analyst / Data Analyst Intern**:

- **Data Integration:** Kết nối và lấy dữ liệu từ nguồn bên ngoài thông qua API hoặc thư viện dữ liệu chứng khoán.
- **Data Cleaning:** Chuẩn hóa dữ liệu ngày tháng, ép kiểu dữ liệu số, xử lý dữ liệu giá và khối lượng.
- **Data Transformation:** Chuyển đổi dữ liệu thô thành dữ liệu có thể phân tích và trực quan hóa.
- **Time-Series Analysis:** Sắp xếp dữ liệu theo thời gian và phân tích biến động giá cổ phiếu.
- **Technical Indicator Calculation:** Tính toán các chỉ báo như RSI, `MA20`, `MA50`, `MA100`, `MA200` bằng `Pandas` và `NumPy`.
- **Dashboard Visualization:** Xây dựng dashboard trực quan để theo dõi xu hướng giá, khối lượng và động lượng thị trường.
- **Excel Report Automation:** Tự động xuất báo cáo Excel để hỗ trợ phân tích sâu hơn bằng Excel, Pivot Table hoặc Power BI.

---

## Quy trình phân tích dữ liệu

Hệ thống hoạt động theo một quy trình xử lý dữ liệu rõ ràng, phù hợp với workflow của Data Analyst:

```text
[Data Source: VCI API thông qua vnstock]
│
▼
[Data Ingestion Layer]
Thu thập dữ liệu OHLCV lịch sử
│
▼
[Data Cleaning Layer]
Parse dữ liệu ngày tháng, ép kiểu số và chuẩn hóa giá
│
▼
[Data Transformation Layer]
Tính toán biến động giá, phần trăm thay đổi, RSI và các đường MA
│
▼
[Data Presentation Layer]
Chuyển dữ liệu đã xử lý thành JSON sẵn sàng cho biểu đồ
│
▼
[Dashboard Layer]
Hiển thị KPI cards, biểu đồ giá, khối lượng và RSI
│
▼
[Excel Reporting Layer]
Xuất dữ liệu sạch thành file Excel để phân tích tiếp
```

---

## Tính năng chính

- **Tìm kiếm mã cổ phiếu:** Người dùng nhập mã như `VIC`, `FPT`, `VNM`, hệ thống tự động chuẩn hóa chữ hoa và loại bỏ khoảng trắng.
- **Hiển thị giá mới nhất:** Lấy giá hiện tại hoặc giá gần nhất có sẵn từ dữ liệu chứng khoán.
- **Tính biến động giá:** Hiển thị mức thay đổi giá và phần trăm thay đổi so với giá tham chiếu.
- **Chỉ báo RSI:** Tính RSI 14 phiên để quan sát trạng thái quá mua, quá bán hoặc trung tính.
- **Đường trung bình động:** Tính `MA20`, `MA50`, `MA100` và `MA200` để phân tích xu hướng giá.
- **Biểu đồ giá và khối lượng:** Trực quan hóa giá đóng cửa, khối lượng giao dịch và các đường MA.
- **Biểu đồ RSI:** Theo dõi động lượng thị trường theo thời gian.
- **Xuất Excel:** Xuất dữ liệu lịch sử theo khoảng ngày thành file Excel có định dạng sẵn.
- **Giao diện dashboard tối:** Thiết kế dark theme phù hợp với dữ liệu tài chính.
- **Deploy online:** Người dùng có thể truy cập trực tiếp bằng trình duyệt, không cần cài đặt local.

---

## Trực quan hóa & Ảnh minh họa

| 1. Giao diện truy vấn mã cổ phiếu | 2. Dashboard phân tích kỹ thuật |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/07defeb9-a194-4e39-8978-65ba8af11b10" width="100%" alt="VSDAT Home Interface" /> | <img src="https://github.com/user-attachments/assets/0b1b5455-425c-4893-b947-d54d2acbaa49" width="100%" alt="VSDAT Quantitative Analysis Dashboard" /> |
| **Tiêu đề:** Giao diện nhập mã cổ phiếu và xuất Excel<br>**Góc nhìn Data Analyst:** Đây là lớp nhập tham số dữ liệu, nơi người dùng xác định mã cổ phiếu cần phân tích và khoảng thời gian cần xuất báo cáo. | **Tiêu đề:** Dashboard phân tích kỹ thuật<br>**Góc nhìn Data Analyst:** Hiển thị các KPI quan trọng như giá hiện tại, mức thay đổi, RSI, MA20 và biểu đồ giá - khối lượng, giúp trình bày dữ liệu theo hướng hỗ trợ ra quyết định. |

| 3. Biểu đồ RSI | 4. Báo cáo Excel tự động |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/30219a3f-dc33-4bb2-bd7a-56bfcf78d824" width="100%" alt="VSDAT RSI Indicator Chart" /> | <img src="https://github.com/user-attachments/assets/a5f6e01f-8570-42f9-b69f-19b377dc01d8" width="100%" alt="VSDAT Generated Excel Sheet" /> |
| **Tiêu đề:** Trực quan hóa chỉ báo RSI<br>**Góc nhìn Data Analyst:** Biểu đồ tập trung vào biến động RSI theo thời gian, hỗ trợ quan sát động lượng thị trường và các vùng quá mua/quá bán. | **Tiêu đề:** Báo cáo Excel được tạo tự động<br>**Góc nhìn Data Analyst:** File Excel chứa dữ liệu OHLCV sạch, biến động giá, phần trăm thay đổi và khối lượng, phù hợp để tiếp tục lọc, pivot, báo cáo hoặc import vào Power BI. |

---

## Xuất Excel cho phân tích nâng cao

Một điểm quan trọng của VSDAT là chức năng **tự động xuất báo cáo Excel**. Thay vì chỉ xem dữ liệu trên dashboard, người dùng có thể tải dữ liệu về để tiếp tục phân tích theo workflow thực tế của Data Analyst.

File Excel xuất ra bao gồm:

- Ngày giao dịch
- Giá mở cửa
- Giá cao nhất
- Giá thấp nhất
- Giá đóng cửa
- Thay đổi giá
- Phần trăm thay đổi
- Khối lượng giao dịch

Lợi ích đối với Data Analyst:

- **Dữ liệu sạch:** Dữ liệu được xử lý và định dạng sẵn trước khi xuất.
- **Dễ phân tích tiếp:** Có thể dùng Excel để filter, sort, tạo Pivot Table hoặc chart.
- **Tích hợp BI:** Có thể import vào Power BI, Tableau hoặc các công cụ phân tích khác.
- **Tự động hóa báo cáo:** Giảm thao tác thủ công khi cần lấy dữ liệu lịch sử theo khoảng ngày.
- **Phù hợp báo cáo nhanh:** Hỗ trợ tạo dữ liệu đầu vào cho báo cáo phân tích cổ phiếu.

---

## Công nghệ sử dụng

### Backend - Analytical Engine

- **Ngôn ngữ:** Python 3.10
- **Framework:** Flask
- **Xử lý dữ liệu:** Pandas, NumPy
- **Xuất Excel:** OpenPyXL
- **Nguồn dữ liệu chứng khoán:** vnstock / vnstock3
- **Deploy:** Render

### Frontend - Dashboard Interface

- **Frontend Framework:** React 18
- **Build Tool:** Vite
- **Gọi API:** Axios
- **Biểu đồ:** Recharts
- **Giao diện:** Tailwind CSS
- **Icon:** Lucide React
- **Deploy:** Render

---

## Kiến trúc hệ thống & Luồng dữ liệu

VSDAT được xây dựng theo mô hình client-server tách biệt:

1. Người dùng nhập mã cổ phiếu trên frontend React.
2. Frontend gửi request đến backend Flask thông qua API.
3. Backend lấy dữ liệu chứng khoán bằng `vnstock / vnstock3`.
4. `Pandas` và `NumPy` xử lý dữ liệu, tính toán RSI, MA và các chỉ số biến động.
5. Backend trả JSON cho frontend để hiển thị dashboard.
6. Recharts trực quan hóa dữ liệu thành biểu đồ giá, khối lượng và RSI.
7. Khi người dùng xuất Excel, backend tạo file bằng `OpenPyXL` và trả về file `.xlsx`.

---

## API Endpoints

### 1. Lấy dữ liệu phân tích cổ phiếu

- **Path:** `GET /stock/<symbol>`
- **Mô tả:** Lấy dữ liệu cổ phiếu, xử lý chuỗi thời gian, tính toán chỉ báo và trả dữ liệu JSON cho dashboard.
- **Response Status:** `200 OK` / `400 Bad Request` / `442 Unprocessable Content`

Ví dụ JSON trả về:

```json
{
  "color": "green",
  "currentPrice": 227900.0,
  "ma20": 218040.0,
  "percentChange": 1.24,
  "priceChange": 2800.0,
  "referencePrice": 225100.0,
  "rsi": 70.51,
  "status": "up",
  "symbol": "VIC",
  "data": [
    {
      "time": "2026-02-25",
      "open": 159000.0,
      "high": 161000.0,
      "low": 157000.0,
      "close": 158000.0,
      "volume": 5289800.0,
      "MA20": 146490.0,
      "MA50": 138200.0,
      "MA100": 131130.0,
      "MA200": 93179.0,
      "RSI": 68.4
    }
  ]
}
```

### 2. Xuất báo cáo Excel

- **Path:** `GET /export/<symbol>/<start_date>/<end_date>`
- **Response Type:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- **Mô tả:** Tạo file Excel động từ dữ liệu lịch sử và trả về file để người dùng tải xuống.

Ví dụ:

```text
/export/VIC/2025-01-01/2025-12-31
```

---

## Cấu trúc dự án

```bash
VSDAT-Terminal/
├── backend/
│   ├── app.py                 # Flask server, API routes và logic phân tích dữ liệu
│   ├── requirements.txt       # Danh sách thư viện Python
│   └── runtime.txt            # Phiên bản runtime cho môi trường deploy
└── frontend/
    ├── src/
    │   ├── App.jsx            # Giao diện dashboard và logic tương tác người dùng
    │   ├── index.css          # Cấu hình Tailwind CSS
    │   └── main.jsx           # File khởi tạo React app
    ├── package.json           # Danh sách thư viện frontend
    ├── tailwind.config.js     # Cấu hình Tailwind
    └── vite.config.js         # Cấu hình Vite build
```

---

## Cài đặt và chạy Local

### Yêu cầu môi trường

- Python 3.9 trở lên
- Node.js v18 trở lên
- Git

### 1. Chạy Backend Flask

```bash
cd backend
python -m venv venv
```

Kích hoạt môi trường ảo:

```bash
# Windows
venv\Scripts\activate
```

```bash
# macOS / Linux
source venv/bin/activate
```

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

Chạy backend:

```bash
python app.py
```

Backend sẽ chạy tại:

```text
http://127.0.0.1:5000
```

### 2. Chạy Frontend React

```bash
cd frontend
npm install
npm run dev
```

Frontend sẽ chạy tại:

```text
http://localhost:5173
```

---

## Biến môi trường

### Backend

```env
PORT=5000
DEVELOPER_EMAIL=doananhtuan77qn@gmail.com
DEVELOPER_PHONE=0399848871
DEVELOPER_GITHUB=https://github.com/tuanda2309
DEVELOPER_WEB=https://vsdat-frontend.onrender.com
```

### Frontend

```env
VITE_API_URL=https://your-backend-url.onrender.com
```

Khi chạy local, có thể dùng:

```env
VITE_API_URL=http://127.0.0.1:5000
```

---

## Lưu ý / Disclaimer

**Dự án này chỉ được xây dựng cho mục đích học tập, luyện tập Data Analytics và trình bày portfolio cá nhân.**

VSDAT **không phải** là công cụ tư vấn đầu tư, không đưa ra khuyến nghị mua/bán cổ phiếu và không thay thế các nền tảng phân tích tài chính chuyên nghiệp.

Tất cả dữ liệu và chỉ báo được tính toán tự động nhằm phục vụ mục đích tham khảo, thực hành xử lý dữ liệu và trực quan hóa dashboard.

---

## Tác giả

- **Họ tên:** Doan Anh Tuan
- **Email:** [doananhtuan77qn@gmail.com](mailto:doananhtuan77qn@gmail.com)
- **GitHub:** [tuanda2309](https://github.com/tuanda2309)
- **Live Demo:** [VSDAT Terminal Live](https://vsdat-frontend.onrender.com)

---
