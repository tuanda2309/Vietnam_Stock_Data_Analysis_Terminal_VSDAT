# Vietnam Stock Data Analysis Terminal (VSDAT)

[English](#english) | [Tiếng Việt](#tiếng-việt)

---

# English

## Vietnam Stock Data Analysis Terminal (VSDAT) 🚀
**A Data Analytics Portfolio Project for Time-Series Analysis & Financial Indicator Automation**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind--CSS-3.4+-06B6D4?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com/)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)](#)

## 🌐 Live Demo
Experience the analytical terminal live here: **[VSDAT Live Web App](https://vsdat-frontend.onrender.com)**

---

## 📌 Table of Contents
1. [Overview](#overview)
2. [Why this Project was Built](#why-this-project-was-built)
3. [Data Analyst Perspective](#data-analyst-perspective)
4. [Data Analytics Workflow (Data Pipeline)](#data-analytics-workflow-data-pipeline)
5. [Key Features](#key-features)
6. [Visualizations & Screenshots](#visualizations--screenshots)
7. [Excel Export for Advanced Analytics](#excel-export-for-advanced-analytics)
8. [Tech Stack](#tech-stack)
9. [System Architecture & Data Flows](#system-architecture--data-flows)
10. [API Endpoints](#api-endpoints)
11. [Project Structure](#project-structure)
12. [Getting Started Local Deployment](#getting-started-local-deployment)
13. [Environment Variables](#environment-variables)
14. [Disclaimer](#disclaimer)
15. [Author](#author)

---

## 🏥 Overview
**Vietnam Stock Data Analysis Terminal (VSDAT)** is a dedicated mini data analytics product developed to ingest, transform, calculate, and visualize historical time-series financial data from the Vietnamese stock market. Users can query any valid stock ticker (e.g., `VIC`, `FPT`, `VNM`), rendering an interactive decision-support dashboard loaded with calculated technical indicators. Additionally, the platform provides automated analytical Excel report generation for subsequent ad-hoc auditing and business intelligence integrations.

---

## 🎯 Why this Project was Built
Traditional stock market dashboards are often overcrowded, marketing-driven, or completely abstracted away from raw data access. **VSDAT** was built to bridge the gap between financial visualization and practical data science engineering. It serves as a live presentation of an analytical asset, proving how an engineering-focused Data Analyst handles real-world streaming variations, unrefined third-party data data types, and delivers scalable, business-ready programmatic artifacts.

---

## 👨‍💻 Data Analyst Perspective
This project explicitly highlights the following technical and analytical competencies required of a **Junior/Intermediate Data Analyst**:
* **Data Integration Architecture:** Handling external streaming connections cleanly via Python endpoints, converting numeric raw string representations to precise financial values.
* **Time-Series Engineering:** Implementing algorithmic operations over indexed date series (e.g., sorting Chronologically, structural imputation using moving averages).
* **Mathematical Metric Derivation:** Translating financial formula equations directly into vector-optimized Python code using `Pandas` and `NumPy` without relying on black-box charting platforms.
* **Downstream Workflow Support:** Implementing parameterized Excel automated pipelines to enable user-driven reporting, filtering, and cross-application BI imports (Power BI / Advanced Excel).

---

## ⚙️ Data Analytics Workflow (Data Pipeline)
The system executes a rigid, linear processing model to guarantee reliable numerical rendering:


```

[Data Source: VCI API via vnstock]
│
▼
[Data Ingestion Layer]  ──► Fetches 2-year raw OHLCV historical time-series
│
▼
[Data Cleaning Layer]  ──► Handles Datetime parsing, forces explicit float types,
multiplies relative raw values into absolute VND currency
│
▼
[Data Transformation Layer] ──► Fills tracking gaps, calculates price variances,
computes rolling technical boundaries (MA, RSI, Bollinger)
│
▼
[Data Presentation Layer] ──► Converts structural frames into chart-ready JSON Payloads
│
▼
[User Interface Dashboard] ──► Interactive line charts, momentum area monitors, KPI metric blocks

```

---

## 🚀 Key Features
* **Symbol Search Parsing:** Sanitizes input strings, handles whitespace stripping, and normalizes tickers to standard uppercase formats.
* **Real-time Price Sync Processing:** Intraday validation layers query instant ticks, evaluating current performance against previous closing margins safely.
* **Advanced Mathematical Metrics:** Implements programmatic rolling vector calculation for `MA20`, `MA50`, `MA100`, `MA200`, and `RSI (14-period)`.
* **Dynamic Time-Series Visualization:** Responsive dark-themed charts plotting closing values, moving boundary lines, and transparent relative trade volume bars.
* **Interactive Momentum Monitor:** Isolated RSI charting area mapping oversold (`<=30`), neutral, and overbought (`>=70`) zones dynamically.
* **Excel Report Automation:** Directly compiles structured operational sheets using low-overhead XML generators (`openpyxl`), complete with standard auditing formatting rules.

---

## 🖼️ Visualizations & Screenshots

| 1. Main Landing Query Interface | 2. Time-Series Analysis Dashboard |
| :---: | :---: |
| <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/07defeb9-a194-4e39-8978-65ba8af11b10" />
" width="100%" alt="VSDAT Home Interface"/> | <img src="assets/screenshots/dashboard.png" width="100%" alt="VSDAT Quantitative Analysis Dashboard"/> |
| **Title:** Stock Query & Excel Export Interface<br>*Data Analyst Context:* This screen represents the data extraction and reporting specification layer. Users define parameters for time-series parsing and reporting boundaries. | **Title:** Technical Analysis Dashboard<br>*Data Analyst Context:* Demonstrates analytical UI design, operational KPI metrics cards, and multi-axis time-series visualization for operational decision-making. |
| **3. Relative Strength Indicator Chart** | **4. Generated Programmatic Excel Report** |
| <img src="assets/screenshots/rsi-chart.png" width="100%" alt="VSDAT RSI Indicator Chart"/> | <img src="assets/screenshots/excel-export.png" width="100%" alt="VSDAT Generated Excel Sheet"/> |
| **Title:** RSI Momentum Visualization<br>*Data Analyst Context:* Focused visual representation of momentum derivation over a moving 14-day chronological window, illustrating index tracking and boundary constraints. | **Title:** Automated Excel Analytical Report<br>*Data Analyst Context:* Displays the structured outputs generated by the Python backend. Emphasizes clean structured layouts optimized for Pivot tables or Power BI modeling. |

---

## 📊 Excel Export for Advanced Analytics
A critical feature of VSDAT is its automated reporting pipeline. Instead of forcing data professionals to stay within an interactive dashboard, VSDAT enables them to extract the raw metrics for custom workflows:

* **Clean Data Integrity:** Outputs structured tabular logs containing matching Date, Open, High, Low, Close, Delta Change, Percentage Deviation, and Volumetric tallies.
* **Ad-Hoc Ready Design:** Cells are explicitly typed numerically with thousands formatting separators (`#,##0.00` and `#,##0`), removing text parsing obstacles during spreadsheet model building.
* **BI Integration:** Clean structured columns make the output file fully compatible for direct data source injection into Microsoft Power BI, Tableau, or Excel Pivot Table architectures.
* **Automated Audit Footprints:** Embedded metadata binds contact pathways directly to trace validation lineage seamlessly.

---

## 🛠 Tech Stack
### Backend Analytical Engine
* **Core Language:** Python 3.10
* **Framework:** Flask (Lightweight REST API Routing Engine)
* **Data Manipulation & Processing:** Pandas, NumPy
* **Report Compiling Engine:** OpenPyXL (Low-level analytical XML generator)
* **Market Financial Broker Connection:** vnstock / vnstock3 (External quote historical pipeline wrapper)

### Frontend Interactive Layer
* **Core Runtime Architecture:** React 18 / Vite (Modern decoupled client engine)
* **Network Query Client:** Axios
* **Vector Data Charting Canvas:** Recharts (High-performance analytical drawing nodes)
* **Styling & UI Components:** Tailwind CSS, Lucide React (Responsive dashboard styling)

---

## 🌐 System Architecture & Data Flows
The platform operates as a modern decoupled client-server instance:

1. **Client Action:** Frontend posts queries to the Backend hosted gateway.
2. **Analysis Cycle:** Backend verifies the parameter, computes moving vectors, slices data windows down to the past 120 operational candles, and formats raw strings into floats.
3. **Visualization Compilation:** Returns a single high-efficiency object array to populate Recharts components instantly.
4. **Export Cycle:** On export execution, the backend creates an isolated multi-pass binary stream, draws structural boundaries, applies mathematical formats, and forces header configuration bindings to prevent cross-origin tracking dropouts (`Access-Control-Expose-Headers`).

---

## 🔌 API Endpoints

### 1. Retrieve Historical Diagnostics
* **Path:** `GET /stock/<symbol>`
* **Response Status:** `200 OK` / `400 Bad Request` / `442 Unprocessable Content`
* **JSON Payload Format Example:**
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

### 2. Stream Processed Automated Excel Workbook

* **Path:** `GET /export/<symbol>/<start_date>/<end_date>`
* **Response Type:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
* **Functionality:** Compiles data dynamically inside server memory buffers and pushes download attachments to clients immediately.

---

## 📂 Project Structure

```bash
VSDAT-Terminal/
├── backend/
│   ├── app.py                 # Main Flask server entry point, routes, and analytical computations
│   ├── requirements.txt       # Python operational environment dependencies
│   └── runtime.txt            # Explicit server version mapping for production engines
└── frontend/
    ├── src/
    │   ├── App.jsx            # Analytical dashboard rendering layout and user state logic
    │   ├── index.css          # Tailwind CSS layer definitions
    │   └── main.jsx           # Application initialization mount node
    ├── package.json           # Frontend dependency manifest
    ├── tailwind.config.js     # Responsive design grid overrides
    └── vite.config.js         # Production bundle asset compiler options

```

---

## 🚀 Getting Started Local Deployment

### Prerequisite Environment Assets

* Python 3.9 or higher installed
* Node.js v18 or higher installed

### 1. Localizing the Analytical Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows deployment use: venv\Scripts\activate
pip install -r requirements.txt
python app.py

```

The analytical service will spin up natively on `http://127.0.0.1:5000`.

### 2. Mounting the Graphical Interface Client

```bash
cd frontend
npm install
npm run dev

```

Open your standard testing browser instance at `http://localhost:5173`.

---

## 🔒 Environment Variables

Configure runtime configurations via systemic environment parameters:

### Backend Layer (`.env` configuration)

* `PORT`: Service routing gate mapping (Defaults to `5000`).
* `DEVELOPER_EMAIL`: Automation trace identifier link.

### Frontend Layer (`.env.local` configuration)

* `VITE_API_URL`: Root path destination redirect parameter directing requests to the analytical service (e.g., `https://your-api.render.com`).

---

## ⚠️ Disclaimer

**This project is exclusively developed for educational, technical demonstration, and data analytics portfolio practice purposes only.** It does not present investment advice, does not output financial buy/sell recommendations, and does not replace professional broker tools. All calculations are executed algorithmically without contextual market analysis warranties.

---

## 👤 Author

* **Full Name:** Doan Anh Tuan
* **Email Contact:** doananhtuan77qn@gmail.com
* **GitHub Repository Portfolio:** [tuanda2309](https://github.com/tuanda2309)
* **Live Operational Terminal Link:** [VSDAT Terminal Live](https://vsdat-frontend.onrender.com)

---

---

# Tiếng Việt

## Vietnam Stock Data Analysis Terminal (VSDAT) 🚀

**Dự Án Portfolio Phân Tích Dữ Liệu Phân Tích Chuỗi Thời Gian & Tự Động Hóa Chỉ Báo Tài Chính**

---

## 🌐 Bản Demo Trực Tuyến

Trải nghiệm trực tiếp hệ thống phân tích tại đây: **[VSDAT Live Web App](https://vsdat-frontend.onrender.com)**

---

## 📌 Mục Lục

1. [Tổng Quan Dự Án](https://www.google.com/search?q=%23t%E1%BB%95ng-quan-d%E1%BB%B1-%C3%A1n)
2. [Lý Do Xây Dựng Dự Án](https://www.google.com/search?q=%23l%C3%BD-do-x%C3%A2y-d%E1%BB%B1ng-d%E1%BB%B1-%C3%A1n)
3. [Góc Nhìn Data Analyst](https://www.google.com/search?q=%23g%C3%B3c-nh%C3%ACn-data-analyst)
4. [Quy Trình Xử Lý & Phân Tích Dữ Liệu (Data Pipeline)](https://www.google.com/search?q=%23quy-tr%C3%ACnh-x%E1%BB%AD-l%C3%BD--ph%C3%A2n-t%C3%ADch-d%E1%BB%AF-li%E1%BB%87u-data-pipeline)
5. [Các Tính Năng Nổi Bật](https://www.google.com/search?q=%23c%C3%A1c-t%C3%ADnh-n%C4%83ng-n%E1%BB%95i-b%E1%BA%ADt)
6. [Trực Quan Hóa & Ảnh Chụp Màn Hình](https://www.google.com/search?q=%23tr%E1%BB%B1c-quan-h%C3%B3a--%E1%BA%A3nh-ch%E1%BB%A5p-m%C3%A0n-h%C3%ACnh)
7. [Chức Năng Xuất Excel Dành Cho Phân Tích Nâng Cao](https://www.google.com/search?q=%23ch%E1%BB%A9c-n%C4%83ng-xu%E1%BA%A5t-excel-d%C3%A0nh-cho-ph%C3%A2n-t%C3%ADch-n%C3%A2ng-cao)
8. [Công Nghệ Sử Dụng (Tech Stack)](https://www.google.com/search?q=%23c%C3%B4ng-ngh%E1%BB%87-s%E1%BB%AD-d%E1%BB%A5ng-tech-stack)
9. [Kiến Trúc Hệ Thống & Luồng Dữ Liệu](https://www.google.com/search?q=%23ki%E1%BA%BFn-tr%C3%BAc-h%E1%BB%87-th%E1%BB%91ng--lu%E1%BB%93ng-d%E1%BB%AF-li%E1%BB%87u)
10. [Các API Cốt Lõi](https://www.google.com/search?q=%23c%C3%A1c-api-c%E1%BB%91t-l%C3%B5i)
11. [Cấu Trúc Thư Mục Dự Án](https://www.google.com/search?q=%23c%E1%BA%A5u-tr%C3%BAc-th%C6%B0-m%E1%BB%A5c-d%E1%BB%B1-%C3%A1n)
12. [Hướng Dẫn Cài Đặt Chạy Local](https://www.google.com/search?q=%23h%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-c%C3%A0i-%C4%91%E1%BA%B7t-ch%E1%BA%A1y-local)
13. [Biến Môi Trường](https://www.google.com/search?q=%23bi%E1%BA%BFn-m%C3%B4i-tr%C6%B0%E1%BB%9Dng)
14. [Tuyên Bố Miễn Trách](https://www.google.com/search?q=%23tuy%C3%AAn-b%E1%BB%91-mi%E1%BB%85n-tr%C3%A1ch)
15. [Thông Tin Tác Giả](https://www.google.com/search?q=%23th%C3%B4ng-tin-t%C3%A1c-gi%E1%BA%A3)

---

## 🏥 Tổng Quan Dự Án

**Vietnam Stock Data Analysis Terminal (VSDAT)** là một sản phẩm phân tích dữ liệu thu nhỏ (mini data analytics product) được thiết kế để thu thập, làm sạch, biến đổi và trực quan hóa dữ liệu chuỗi thời gian lịch sử của thị trường chứng khoán Việt Nam. Khi người dùng truy vấn một mã cổ phiếu (ví dụ: `VIC`, `FPT`, `VNM`), hệ thống sẽ tính toán các chỉ báo định lượng và hiển thị một dashboard hỗ trợ quyết định một cách trực quan. Hệ thống cũng cung cấp chức năng tự động hóa báo cáo Excel để phục vụ các quy trình phân tích ad-hoc sâu hơn hoặc tích hợp vào các công cụ Business Intelligence (BI).

---

## 🎯 Lý Do Xây Dựng Dự Án

Các bảng điều khiển chứng khoán thông thường trên thị trường thường bị quá tải thông tin, mang nặng tính quảng cáo, hoặc ẩn đi quy trình xử lý dữ liệu thô. **VSDAT** được xây dựng nhằm mục đích thu hẹp khoảng cách giữa việc trực quan hóa tài chính đơn thuần và kỹ thuật phân tích dữ liệu thực tế. Dự án là một minh chứng cụ thể cho hồ sơ năng lực (Portfolio) của một Data Analyst trong việc xử lý dữ liệu từ bên thứ ba, tối ưu hóa thuật toán chuỗi thời gian và đóng gói thành một sản phẩm công nghệ có khả năng triển khai thực tế.

---

## 👤 Góc Nhìn Data Analyst

Dự án này làm nổi bật các kỹ năng chuyên môn cốt lõi của một **Data Analyst**:

* **Xây Dựng Pipeline Dữ Liệu:** Kết nối và trích xuất dữ liệu từ API bên thứ ba, xử lý chuẩn hóa các kiểu dữ liệu số từ các chuỗi định dạng thô.
* **Xử Lý Chuỗi Thời Gian (Time-Series):** Sắp xếp dòng thời gian theo thứ tự biên niên (Chronological sorting), thiết lập chỉ mục đồng nhất và cấu hình các khoảng trích xuất dữ liệu một cách khoa học.
* **Tính Toán Chỉ Báo Định Lượng:** Chuyển đổi các công thức toán học tài chính phức tạp thành mã lập trình tối ưu hóa vector thông qua `Pandas` và `NumPy` thay vì phụ thuộc vào các thư viện đồ thị đóng gói sẵn.
* **Tự Động Hóa Workflow Doanh Nghiệp:** Thiết lập quy trình tự động biên soạn báo cáo Excel có định dạng chuẩn, giúp người dùng cuối dễ dàng tiếp tục thực hiện kiểm toán dữ liệu hoặc dựng mô hình BI.

---

## ⚙️ Quy Trình Xử Lý & Phân Tích Dữ Liệu (Data Pipeline)

Hệ thống vận hành theo một đường ống dữ liệu tuần tự khép kín để đảm bảo tính toàn vẹn của các con số:

```
[Nguồn Dữ Liệu: VCI API qua vnstock]
                │
                ▼
   [Tầng Thu Thập Dữ Liệu] ──► Tải về chuỗi dữ liệu lịch sử OHLCV thời gian 2 năm
                │
                ▼
    [Tầng Làm Sạch Dữ Liệu] ──► Định dạng Datetime, ép kiểu số float,
                                quy chuẩn giá trị thô về đơn vị VNĐ tuyệt đối
                │
                ▼
   [Tầng Biến Đổi Dữ Liệu]  ──► Xử lý khoảng trống dữ liệu, tính toán độ lệch giá,
                                tính các đường biên rolling (MA, RSI, Bollinger)
                │
                ▼
   [Tầng Trực Quan Hóa]    ──► Chuyển đổi DataFrame sang cấu trúc JSON sẵn sàng cho đồ thị
                │
                ▼
   [Giao Diện Dashboard]   ──► Hiển thị biểu đồ xu hướng, khối lượng và động lượng RSI

```

---

## 🚀 Các Tính Năng Nổi Bật

* **Xử Lý Chuỗi Ký Tự Mã Cổ Phiếu:** Tự động làm sạch khoảng trắng, chuẩn hóa ký tự thành chữ in hoa để tránh lỗi truy vấn hệ thống.
* **Đồng Bộ Giá Thời Gian Thực:** Lớp kiểm định dữ liệu trong ngày (intraday validation) đối chiếu mức giá khớp lệnh gần nhất với giá đóng cửa phiên trước đó một cách chính xác.
* **Hệ Thống Chỉ Báo Định Lượng:** Sử dụng tính toán vector hóa rolling để xác định nhanh các đường trung bình động động `MA20`, `MA50`, `MA100`, `MA200` và chỉ số sức mạnh tương đối `RSI (14 phiên)`.
* **Biểu Đồ Xu Hướng Đa Trục:** Đồ thị giao diện tối hiển thị đồng thời đường giá đóng cửa, 4 đường trung bình động xu hướng và các cột khối lượng giao dịch dạng mờ (alpha blending).
* **Đồ Thị Động Lượng Độc Lập:** Phân vùng biểu đồ RSI rõ ràng giúp nhận diện nhanh các trạng thái Quá mua (`>=70`), Trung tính và Quá bán (`<=30`).
* **Xuất Báo Cáo Excel Tự Động:** Sử dụng bộ thư viện cấu trúc thấp (`openpyxl`) để tạo tệp bảng tính có định dạng phân rã số liệu chuyên nghiệp.

---

## 🖼️ Trực Quan Hóa & Ảnh Chụp Màn Hình

| 1. Giao Diện Tra Cứu & Thiết Lập Tham Số | 2. Dashboard Phân Tích Chuỗi Thời Gian |
| --- | --- |
|  |  |
| **Tiêu đề:** Giao Diện Truy Vấn Mã & Xuất Excel<br>

<br>*Dưới góc nhìn Data Analyst:* Màn hình này đại diện cho lớp trích xuất dữ liệu. Người dùng cấu hình tham số đầu vào và xác định phạm vi thời gian của báo cáo cần truy xuất. | **Tiêu đề:** Bảng Điều Khiển Phân Tích Kỹ Thuật<br>

<br>*Dưới góc nhìn Data Analyst:* Thể hiện khả năng thiết kế giao diện phân tích, bố cục thẻ chỉ số KPI doanh nghiệp và trực quan hóa chuỗi thời gian đa trục hỗ trợ ra quyết định. |
| **3. Biểu Đồ Chỉ Số Sức Mạnh Tương Đối (RSI)** | **4. Tệp Báo Cáo Excel Được Hệ Thống Tự Động Biên Soạn** |
|  |  |
| **Tiêu đề:** Trực Quan Hóa Động Lượng RSI<br>

<br>*Dưới góc nhìn Data Analyst:* Biểu thị trực quan sự biến thiên của động lượng trong khung cửa sổ 14 ngày lịch sử, tuân thủ các ràng buộc biên độ của chỉ số kỹ thuật. | **Tiêu đề:** Báo Cáo Dữ Liệu Excel Tự Động<br>

<br>*Dưới góc nhìn Data Analyst:* Minh chứng cho kết quả đầu ra của pipeline backend Python. Bảng dữ liệu sạch được tối ưu hóa cho cấu trúc Pivot Table hoặc mô hình dữ liệu Power BI. |

---

## 📊 Chức Năng Xuất Excel Dành Cho Phân Tích Nâng Cao

Một tính năng cực kỳ quan trọng chứng minh tư duy thiết kế hệ thống dữ liệu của VSDAT là khả năng tự động hóa báo cáo. Thay vì giữ chân nhà phân tích trong một giao diện cố định, VSDAT mở rộng quy trình làm việc (workflow) sang các công cụ chuyên dụng khác:

* **Tính Toàn Vẹn Của Dữ Liệu Sạch:** Tệp xuất ra chứa cấu trúc bảng chuẩn bao gồm các cột: Ngày, Giá Mở Cửa, Giá Cao Nhất, Giá Thấp Nhất, Giá Đóng Cửa, Thay Đổi Giá, % Thay Đổi và Khối Lượng.
* **Định Dạng Chuẩn Định Lượng:** Toàn bộ các ô dữ liệu số được ép kiểu dữ liệu số (numeric type) kết hợp mã định dạng hiển thị phân tách hàng nghìn (`#,##0.00` và `#,##0`), loại bỏ hoàn toàn tình trạng lỗi định dạng chữ (text format) khi viết hàm.
* **Sẵn Sàng Cho Công Cụ BI:** Cấu trúc cột đồng nhất giúp tệp Excel trở thành nguồn dữ liệu đầu vào (data source) sạch, kết nối trực tiếp vào Microsoft Power BI, Tableau hoặc dựng các bảng Pivot Table nâng cao.
* **Tích Hợp Dấu Vết Kiểm Toán:** Các dòng thông tin liên hệ được nhúng trực tiếp bằng rich-text định dạng link giúp dễ dàng truy vết nguồn gốc phát triển của báo cáo.

---

## 🛠 Công Nghệ Sử Dụng (Tech Stack)

### Backend (Động Cơ Phân Tích Định Lượng)

* **Ngôn ngữ cốt lõi:** Python 3.10
* **Framework:** Flask (Điều phối REST API cấu trúc tinh gọn)
* **Xử lý & Biến đổi dữ liệu:** Pandas, NumPy
* **Công cụ biên soạn báo cáo:** OpenPyXL (Trình biên dịch XML bảng tính hiệu năng cao)
* **Kết nối cổng dữ liệu thị trường:** vnstock / vnstock3 (Thư viện đóng gói pipeline lịch sử chứng khoán)

### Frontend (Giao Diện Trực Quan Tương Tác)

* **Kiến trúc vận hành:** React 18 / Vite (Trình đóng gói và thực thi giao diện hiện đại)
* **Client kết nối mạng:** Axios
* **Thư viện vẽ đồ thị vector:** Recharts (Vẽ đồ thị dựa trên các node thành phần hiệu năng cao)
* **Thiết kế giao diện:** Tailwind CSS, Lucide React (Thư viện tối ưu hóa hiển thị dashboard đáp ứng)

---

## 🌐 Kiến Trúc Hệ Thống & Luồng Dữ Liệu

Hệ thống vận hành theo mô hình máy chủ - máy trạm độc lập (decoupled client-server architecture):

1. **Yêu cầu từ Client:** Frontend gửi tham số mã chứng khoán qua giao thức HTTP đến cổng API Backend.
2. **Quy trình xử lý tại Server:** Backend tiếp nhận mã, tính toán các mảng dịch chuyển toán học, cắt lát chuỗi thời gian lấy 120 phiên gần nhất, chuyển đổi cấu trúc DataFrame thành mảng đối tượng dạng JSON.
3. **Kết xuất trực quan:** Client nhận JSON, nạp trực tiếp vào các nút đồ thị Recharts giúp hiển thị giao diện mượt mà.
4. **Quy trình xuất file:** Khi có lệnh xuất file, backend tạo luồng nhị phân trực tiếp trên bộ nhớ đệm (memory buffer), dựng khung bảng tính Excel, cấu hình format ô và kích hoạt tiêu đề phơi bày `Access-Control-Expose-Headers` để tránh tình trạng trình duyệt chặn tải file do lỗi CORS.

---

## 🔌 Các API Cốt Lõi

### 1. Lấy Dữ Liệu Phân Tích Chỉ Báo Kỹ Thuật

* **Đường dẫn:** `GET /stock/<symbol>`
* **Mã trạng thái phản hồi:** `200 OK` / `400 Bad Request` / `442 Unprocessable Content`
* **Ví dụ cấu trúc dữ liệu JSON trả về:**

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

### 2. Trích Xuất File Báo Cáo Bảng Tính Excel

* **Đường dẫn:** `GET /export/<symbol>/<start_date>/<end_date>`
* **Kiểu dữ liệu phản hồi:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
* **Mô tả vận hành:** Tổng hợp bảng dữ liệu lịch sử theo khoảng ngày chỉ định, ghi trực tiếp vào bộ nhớ máy chủ và trả về luồng tải tệp (download attachment) ngay lập tức cho client.

---

## 📂 Cấu Trúc Thư Mục Dự Án

```bash
VSDAT-Terminal/
├── backend/
│   ├── app.py                 # Tệp chạy chính Flask, điều hướng API và tính toán định lượng
│   ├── requirements.txt       # Danh sách các thư viện Python môi trường bắt buộc
│   └── runtime.txt            # Định nghĩa phiên bản Python chạy trên môi trường production
└── frontend/
    ├── src/
    │   ├── App.jsx            # Cấu trúc giao diện dashboard, gọi API và quản lý state ứng dụng
    │   ├── index.css          # Tích hợp các layer cấu hình Tailwind CSS
    │   └── main.jsx           # Điểm khởi tạo gắn node mount của ứng dụng React
    ├── package.json           # Danh sách thư viện và script vận hành Frontend
    ├── tailwind.config.js     # Cấu hình mở rộng grid và theme giao diện responsive
    └── vite.config.js         # Các tùy chọn cấu hình trình biên dịch Vite

```

---

## 🚀 Hướng Dẫn Cài Đặt Chạy Local

### Yêu Cầu Môi Trường Máy Máy Máy

* Máy tính đã cài đặt sẵn Python 3.9 hoặc cao hơn.
* Máy tính đã cài đặt sẵn Node.js v18 hoặc cao hơn.

### 1. Khởi Chạy Máy Chủ API Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Trên Windows sử dụng lệnh: venv\Scripts\activate
pip install -r requirements.txt
python app.py

```

Máy chủ phân tích dữ liệu sẽ khởi chạy trực tiếp tại địa chỉ: `http://127.0.0.1:5000`.

### 2. Khởi Chạy Giao Diện Máy Trạm Frontend

```bash
cd frontend
npm install
npm run dev

```

Mở trình duyệt web của bạn và truy cập địa chỉ kiểm thử: `http://localhost:5173`.

---

## 🔒 Biến Môi Trường

Cấu hình các tham số vận hành hệ thống thông qua các biến môi trường:

### Cấu hình Backend (Tệp `.env`)

* `PORT`: Cổng định tuyến dịch vụ (Mặc định nếu không thiết lập là `5000`).
* `DEVELOPER_EMAIL`: Địa chỉ email nhúng vào chữ ký kiểm toán báo cáo tự động.

### Cấu hình Frontend (Tệp `.env.local`)

* `VITE_API_URL`: Địa chỉ URL gốc của máy chủ backend (Ví dụ khi triển khai thực tế: `https://your-api.render.com`).

---

## ⚠️ Tuyên Bố Miễn Trách

**Dự án này được xây dựng hoàn toàn cho mục đích học tập, thử nghiệm công nghệ và thực hành portfolio phân tích dữ liệu.** Ứng dụng này không phải là một công cụ tư vấn tài chính, không đưa ra bất kỳ khuyến nghị mua/bán cổ phiếu nào và không thay thế cho các nền tảng giao dịch chuyên nghiệp. Mọi con số tính toán dựa trên thuật toán thuần túy và không có cam kết bảo đảm tính chính xác ngữ cảnh thị trường thực tế.

---

## 👤 Thông Tin Tác Giả

* **Họ và tên:** Doan Anh Tuan
* **Email liên hệ:** doananhtuan77qn@gmail.com
* **Hồ sơ GitHub Portfolio:** [tuanda2309](https://github.com/tuanda2309)
* **Đường dẫn Demo ứng dụng trực tuyến:** [VSDAT Terminal Live](https://vsdat-frontend.onrender.com)

```

```
