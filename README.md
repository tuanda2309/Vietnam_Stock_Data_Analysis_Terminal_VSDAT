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
| <img src="https://github.com/user-attachments/assets/07defeb9-a194-4e39-8978-65ba8af11b10" width="100%" alt="VSDAT Home Interface" /> | <img src="https://github.com/user-attachments/assets/0b1b5455-425c-4893-b947-d54d2acbaa49" width="100%" alt="VSDAT Quantitative Analysis Dashboard" /> |
| **Title:** Stock Query & Excel Export Interface<br>*Data Analyst Context:* This screen represents the data extraction and reporting specification layer. Users define parameters for time-series parsing and reporting boundaries. | **Title:** Technical Analysis Dashboard<br>*Data Analyst Context:* Demonstrates analytical UI design, operational KPI metrics cards, and multi-axis time-series visualization for operational decision-making. |
| **3. Relative Strength Indicator Chart** | **4. Generated Programmatic Excel Report** |
| <img src="https://github.com/user-attachments/assets/30219a3f-dc33-4bb2-bd7a-56bfcf78d824" width="100%" alt="VSDAT RSI Indicator Chart" /> | <img src="https://github.com/user-attachments/assets/a5f6e01f-8570-42f9-b69f-19b377dc01d8" width="100%" alt="VSDAT Generated Excel Sheet" /> |
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
**Dự án Portfolio Data Analytics về Phân tích Chuỗi Thời gian & Tự động hóa Chỉ báo Tài chính**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind--CSS-3.4+-06B6D4?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com/)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)](#)

## 🌐 Demo Trực tuyến
Trải nghiệm ứng dụng tại đây: **[VSDAT Live Web App](https://vsdat-frontend.onrender.com)**

---

## 📌 Mục lục
1. [Tổng quan](#-tổng-quan)
2. [Lý do xây dựng dự án](#-lý-do-xây-dựng-dự-án)
3. [Góc nhìn Data Analyst](#-góc-nhìn-data-analyst)
4. [Quy trình phân tích dữ liệu](#️-quy-trình-phân-tích-dữ-liệu-data-pipeline)
5. [Tính năng chính](#-tính-năng-chính)
6. [Trực quan hóa & Ảnh minh họa](#️-trực-quan-hóa--ảnh-minh-họa)
7. [Xuất Excel cho phân tích nâng cao](#-xuất-excel-cho-phân-tích-nâng-cao)
8. [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
9. [Kiến trúc hệ thống & Luồng dữ liệu](#-kiến-trúc-hệ-thống--luồng-dữ-liệu)
10. [API Endpoints](#-api-endpoints)
11. [Cấu trúc dự án](#-cấu-trúc-dự-án)
12. [Cài đặt và chạy Local](#-cài-đặt-và-chạy-local)
13. [Biến môi trường](#-biến-môi-trường)
14. [Lưu ý / Disclaimer](#️-lưu-ý--disclaimer)
15. [Tác giả](#-tác-giả)

---

## 📊 Tổng quan
**Vietnam Stock Data Analysis Terminal (VSDAT)** là một mini data analytics product được xây dựng để thu thập, xử lý, tính toán và trực quan hóa dữ liệu tài chính dạng chuỗi thời gian của thị trường chứng khoán Việt Nam.

Người dùng có thể nhập mã cổ phiếu hợp lệ như `VIC`, `FPT`, `VNM`, sau đó hệ thống sẽ hiển thị một dashboard phân tích gồm giá hiện tại, mức thay đổi, phần trăm thay đổi, RSI và các đường trung bình động như MA20, MA50, MA100, MA200.

Ngoài dashboard trực quan, VSDAT còn hỗ trợ **xuất báo cáo Excel tự động**, giúp Data Analyst tiếp tục phân tích dữ liệu bằng Excel, Pivot Table, Power BI hoặc các công cụ BI khác.

---

## 🎯 Lý do xây dựng dự án
Nhiều dashboard chứng khoán hiện nay tập trung nhiều vào giao diện hoặc thông tin thị trường, nhưng lại thiếu phần truy xuất dữ liệu sạch để người phân tích có thể tiếp tục xử lý.

**VSDAT** được xây dựng nhằm kết hợp giữa:
- Truy xuất dữ liệu chứng khoán.
- Xử lý và làm sạch dữ liệu bằng Python.
- Phân tích chuỗi thời gian.
- Tính toán chỉ báo kỹ thuật.
- Trực quan hóa bằng dashboard.
- Xuất dữ liệu sạch ra Excel phục vụ báo cáo và phân tích tiếp theo.

Dự án này thể hiện cách một Data Analyst có thể xây dựng một quy trình phân tích dữ liệu hoàn chỉnh từ backend xử lý dữ liệu đến frontend dashboard và báo cáo Excel.

---

## 👨‍💻 Góc nhìn Data Analyst
Dự án này tập trung thể hiện các kỹ năng thực tế cần có của một **Junior Data Analyst / Data Analyst Intern**:

* **Data Integration:** Kết nối và lấy dữ liệu từ nguồn bên ngoài thông qua API/thư viện dữ liệu chứng khoán.
* **Data Cleaning:** Chuẩn hóa dữ liệu ngày tháng, ép kiểu dữ liệu số, xử lý dữ liệu giá và khối lượng.
* **Data Transformation:** Chuyển đổi dữ liệu thô thành dữ liệu có thể phân tích và trực quan hóa.
* **Time-Series Analysis:** Sắp xếp dữ liệu theo thời gian và phân tích biến động giá cổ phiếu.
* **Technical Indicator Calculation:** Tính toán các chỉ báo như RSI, MA20, MA50, MA100, MA200 bằng `Pandas` và `NumPy`.
* **Dashboard Visualization:** Xây dựng dashboard trực quan để theo dõi xu hướng giá, khối lượng và động lượng thị trường.
* **Excel Report Automation:** Tự động xuất báo cáo Excel để hỗ trợ phân tích sâu hơn bằng Excel, Pivot Table hoặc Power BI.

---

## ⚙️ Quy trình phân tích dữ liệu Data Pipeline

Hệ thống hoạt động theo một quy trình xử lý dữ liệu tuyến tính, rõ ràng và phù hợp với workflow của Data Analyst:

```text
[Data Source: VCI API thông qua vnstock]
│
▼
[Data Ingestion Layer]
Thu thập dữ liệu OHLCV lịch sử trong khoảng 2 năm
│
▼
[Data Cleaning Layer]
Parse dữ liệu ngày tháng, ép kiểu số, chuẩn hóa giá về đơn vị VNĐ
│
▼
[Data Transformation Layer]
Tính toán biến động giá, phần trăm thay đổi, RSI và các đường MA
│
▼
[Data Presentation Layer]
Chuyển DataFrame thành JSON sẵn sàng cho biểu đồ
│
▼
[Dashboard Layer]
Hiển thị KPI cards, biểu đồ giá, khối lượng và RSI
│
▼
[Excel Reporting Layer]
Xuất dữ liệu sạch thành file Excel để phân tích tiếp
````

---

## 🚀 Tính năng chính

* **Tìm kiếm mã cổ phiếu:** Người dùng nhập mã như `VIC`, `FPT`, `VNM`, hệ thống tự động chuẩn hóa chữ hoa và loại bỏ khoảng trắng.
* **Hiển thị giá mới nhất:** Lấy giá hiện tại hoặc giá gần nhất có sẵn từ dữ liệu chứng khoán.
* **Tính biến động giá:** Hiển thị mức thay đổi giá và phần trăm thay đổi so với giá tham chiếu.
* **Chỉ báo RSI:** Tính RSI 14 phiên để quan sát trạng thái quá mua, quá bán hoặc trung tính.
* **Đường trung bình động:** Tính MA20, MA50, MA100 và MA200 để phân tích xu hướng giá.
* **Biểu đồ giá và khối lượng:** Trực quan hóa giá đóng cửa, khối lượng giao dịch và các đường MA.
* **Biểu đồ RSI:** Theo dõi động lượng thị trường theo thời gian.
* **Xuất Excel:** Xuất dữ liệu lịch sử theo khoảng ngày thành file Excel có định dạng sẵn.
* **Giao diện Dashboard tối:** Thiết kế dashboard dark theme phù hợp với dữ liệu tài chính.
* **Deploy online:** Người dùng có thể truy cập trực tiếp bằng trình duyệt, không cần cài đặt local.

---

## 🖼️ Trực quan hóa & Ảnh minh họa

|                                                                                       1. Giao diện truy vấn mã cổ phiếu                                                                                      |                                                                                                   2. Dashboard phân tích kỹ thuật                                                                                                  |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                                     <img src="https://github.com/user-attachments/assets/07defeb9-a194-4e39-8978-65ba8af11b10" width="100%" alt="VSDAT Home Interface" />                                    |                                       <img src="https://github.com/user-attachments/assets/0b1b5455-425c-4893-b947-d54d2acbaa49" width="100%" alt="VSDAT Quantitative Analysis Dashboard" />                                       |
| **Tiêu đề:** Giao diện nhập mã cổ phiếu và xuất Excel<br>**Góc nhìn Data Analyst:** Đây là lớp nhập tham số dữ liệu, nơi người dùng xác định mã cổ phiếu cần phân tích và khoảng thời gian cần xuất báo cáo. | **Tiêu đề:** Dashboard phân tích kỹ thuật<br>**Góc nhìn Data Analyst:** Hiển thị các KPI quan trọng như giá hiện tại, mức thay đổi, RSI, MA20 và biểu đồ giá - khối lượng, giúp trình bày dữ liệu theo hướng hỗ trợ ra quyết định. |
|                                                                                              **3. Biểu đồ RSI**                                                                                              |                                                                                                    **4. Báo cáo Excel tự động**                                                                                                    |
|                                  <img src="https://github.com/user-attachments/assets/30219a3f-dc33-4bb2-bd7a-56bfcf78d824" width="100%" alt="VSDAT RSI Indicator Chart" />                                  |                                            <img src="https://github.com/user-attachments/assets/a5f6e01f-8570-42f9-b69f-19b377dc01d8" width="100%" alt="VSDAT Generated Excel Sheet" />                                            |
|          **Tiêu đề:** Trực quan hóa chỉ báo RSI<br>**Góc nhìn Data Analyst:** Biểu đồ tập trung vào biến động RSI theo thời gian, hỗ trợ quan sát động lượng thị trường và các vùng quá mua/quá bán.         |  **Tiêu đề:** Báo cáo Excel được tạo tự động<br>**Góc nhìn Data Analyst:** File Excel chứa dữ liệu OHLCV sạch, biến động giá, phần trăm thay đổi và khối lượng, phù hợp để tiếp tục lọc, pivot, báo cáo hoặc import vào Power BI.  |

---

## 📊 Xuất Excel cho phân tích nâng cao

Một điểm quan trọng của VSDAT là chức năng **tự động xuất báo cáo Excel**. Thay vì chỉ xem dữ liệu trên dashboard, người dùng có thể tải dữ liệu về để tiếp tục phân tích theo workflow thực tế của Data Analyst.

File Excel xuất ra bao gồm:

* **Ngày giao dịch**
* **Giá mở cửa**
* **Giá cao nhất**
* **Giá thấp nhất**
* **Giá đóng cửa**
* **Thay đổi giá**
* **Phần trăm thay đổi**
* **Khối lượng giao dịch**

Lợi ích đối với Data Analyst:

* **Dữ liệu sạch:** Dữ liệu được xử lý và định dạng sẵn trước khi xuất.
* **Dễ phân tích tiếp:** Có thể dùng Excel để filter, sort, tạo Pivot Table hoặc chart.
* **Tích hợp BI:** Có thể import vào Power BI, Tableau hoặc các công cụ phân tích khác.
* **Tự động hóa báo cáo:** Giảm thao tác thủ công khi cần lấy dữ liệu lịch sử theo khoảng ngày.
* **Phù hợp báo cáo nhanh:** Hỗ trợ tạo dữ liệu đầu vào cho báo cáo phân tích cổ phiếu.

---

## 🛠 Công nghệ sử dụng

### Backend - Analytical Engine

* **Ngôn ngữ:** Python 3.10
* **Framework:** Flask
* **Xử lý dữ liệu:** Pandas, NumPy
* **Xuất Excel:** OpenPyXL
* **Nguồn dữ liệu chứng khoán:** vnstock / vnstock3
* **Deploy:** Render

### Frontend - Dashboard Interface

* **Frontend Framework:** React 18
* **Build Tool:** Vite
* **Gọi API:** Axios
* **Biểu đồ:** Recharts
* **Giao diện:** Tailwind CSS
* **Icon:** Lucide React
* **Deploy:** Render

---

## 🌐 Kiến trúc hệ thống & Luồng dữ liệu

VSDAT được xây dựng theo mô hình client-server tách biệt:

1. **Người dùng nhập mã cổ phiếu** trên frontend React.
2. **Frontend gửi request** đến backend Flask thông qua API.
3. **Backend lấy dữ liệu chứng khoán** bằng `vnstock / vnstock3`.
4. **Pandas và NumPy xử lý dữ liệu**, tính toán RSI, MA và các chỉ số biến động.
5. **Backend trả JSON** cho frontend để hiển thị dashboard.
6. **Recharts trực quan hóa dữ liệu** thành biểu đồ giá, khối lượng và RSI.
7. Khi người dùng xuất Excel, backend tạo file bằng `OpenPyXL` và trả về file `.xlsx`.

---

## 🔌 API Endpoints

### 1. Lấy dữ liệu phân tích cổ phiếu

* **Path:** `GET /stock/<symbol>`
* **Mô tả:** Lấy dữ liệu cổ phiếu, xử lý chuỗi thời gian, tính toán chỉ báo và trả dữ liệu JSON cho dashboard.
* **Response Status:** `200 OK` / `400 Bad Request` / `442 Unprocessable Content`

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

* **Path:** `GET /export/<symbol>/<start_date>/<end_date>`
* **Response Type:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
* **Mô tả:** Tạo file Excel động từ dữ liệu lịch sử và trả về file để người dùng tải xuống.

Ví dụ:

```text
/export/VIC/2025-01-01/2025-12-31
```

---

## 📂 Cấu trúc dự án

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

## 🚀 Cài đặt và chạy Local

### Yêu cầu môi trường

* Python 3.9 trở lên
* Node.js v18 trở lên
* Git

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

## 🔒 Biến môi trường

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

## ⚠️ Lưu ý / Disclaimer

**Dự án này chỉ được xây dựng cho mục đích học tập, luyện tập Data Analytics và trình bày portfolio cá nhân.**

VSDAT **không phải** là công cụ tư vấn đầu tư, không đưa ra khuyến nghị mua/bán cổ phiếu và không thay thế các nền tảng phân tích tài chính chuyên nghiệp.

Tất cả dữ liệu và chỉ báo được tính toán tự động nhằm phục vụ mục đích tham khảo, thực hành xử lý dữ liệu và trực quan hóa dashboard.

---

## 👤 Tác giả

* **Họ tên:** Doan Anh Tuan
* **Email:** [doananhtuan77qn@gmail.com](mailto:doananhtuan77qn@gmail.com)
* **GitHub:** [tuanda2309](https://github.com/tuanda2309)
* **Live Demo:** [VSDAT Terminal Live](https://vsdat-frontend.onrender.com)

---
