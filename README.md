# Vietnam Stock Data Analysis Terminal (VSDAT)

<p align="center">
  <strong>A full-stack web application for Vietnamese stock data analysis, technical indicators, chart visualization, and Excel export.</strong>
</p>

<p align="center">
  <a href="https://vsdat-frontend.onrender.com"><strong>🚀 Live Demo</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Frontend-React%20%2F%20Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React Vite" />
  <img src="https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Python-3.10.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10.12" />
  <img src="https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black" alt="Render" />
</p>

<p align="center">
  🌐 Language: <a href="#english">English</a> | <a href="#tiếng-việt">Tiếng Việt</a>
</p>

---

## English

### Project Title

**Vietnam Stock Data Analysis Terminal (VSDAT)**

### Live Demo

[🚀 Live Demo](https://vsdat-frontend.onrender.com)

Frontend URL:

```text
https://vsdat-frontend.onrender.com
```

Backend URL:

```text
https://vsdat-backend-1.onrender.com
```

---

### Language Selection

🌐 Language: [English](#english) | [Tiếng Việt](#tiếng-việt)

---

### Project Overview

**Vietnam Stock Data Analysis Terminal (VSDAT)** is a full-stack web application for analyzing Vietnamese stock market data. It allows users to search a Vietnamese stock symbol, retrieve price data, view price movement, inspect technical indicators, display analysis dashboards, and export historical OHLCV data to Excel for further data analysis.

The project is designed as a portfolio project that demonstrates:

- Full-stack web development with React/Vite and Flask
- REST API design
- Data processing with Pandas and NumPy
- Technical indicator calculation
- Financial data visualization
- Excel report generation
- Basic production deployment on Render

> VSDAT is not an investment advisory tool. All charts, indicators, signals, and exported data are intended for educational and data analysis purposes only.

---

### Key Features

- Search Vietnamese stock symbols
- Display current price information
- Show price change and percentage change
- Identify stock movement status: up, down, or unchanged
- Technical analysis dashboard
- Price and volume chart
- RSI chart
- MACD chart
- Moving averages: MA20, MA50, MA100, MA200
- RSI indicator
- MACD indicator and signal line
- Bollinger Bands calculation in backend
- Support and resistance reference levels
- VNINDEX market context if data is available
- Reference-only signal scoring and warning messages
- Reference-only risk management card
- Excel export for historical OHLCV data
- Loading and error states
- Frontend symbol/date validation
- Backend input validation
- Backend rate limiting
- Backend response caching
- Production deployment configuration with Render

---

### Screenshots

| Main Query Interface | Technical Analysis Dashboard |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/07defeb9-a194-4e39-8978-65ba8af11b10" width="100%" alt="VSDAT Home Interface" /> | <img src="https://github.com/user-attachments/assets/0b1b5455-425c-4893-b947-d54d2acbaa49" width="100%" alt="VSDAT Technical Analysis Dashboard" /> |
| Stock symbol input and Excel export controls | Main dashboard with technical analysis cards and charts |

| RSI Indicator Chart | Generated Excel Report |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/30219a3f-dc33-4bb2-bd7a-56bfcf78d824" width="100%" alt="VSDAT RSI Indicator Chart" /> | <img src="https://github.com/user-attachments/assets/a5f6e01f-8570-42f9-b69f-19b377dc01d8" width="100%" alt="VSDAT Generated Excel Sheet" /> |
| RSI visualization for momentum analysis | Exported OHLCV Excel file for further analysis |

---

### Tech Stack

#### Frontend

- React
- Vite
- Tailwind CSS
- Axios
- Recharts
- Lucide React
- JavaScript

#### Backend

- Python 3.10.12
- Flask
- Flask-CORS
- Flask-Limiter
- Gunicorn

#### Data Processing

- Pandas
- NumPy
- vnstock / vnstock3 Vietnamese stock data source

#### Excel Export

- openpyxl
- BytesIO for in-memory Excel file generation

#### Deployment

- Render

---

### Project Structure

The following structure is based on the uploaded project ZIP.

```text
VSDAT/
├── backend/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── export_routes.py
│   │   └── stock_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── analysis_service.py
│   │   ├── export_service.py
│   │   ├── market_service.py
│   │   └── stock_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── dataframe_utils.py
│   │   ├── helpers.py
│   │   ├── indicators.py
│   │   ├── json_utils.py
│   │   ├── risk.py
│   │   ├── simple_cache.py
│   │   ├── support_resistance.py
│   │   └── validators.py
│   ├── .env.example
│   ├── app.py
│   ├── config.py
│   ├── constants.py
│   ├── extensions.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │   ├── cat-logo.png
│   │   ├── favicon.svg
│   │   └── icons.svg
│   ├── src/
│   │   ├── assets/
│   │   │   ├── hero.png
│   │   │   ├── react.svg
│   │   │   └── vite.svg
│   │   ├── components/
│   │   │   ├── cards/
│   │   │   │   ├── ChecklistCard.jsx
│   │   │   │   ├── InfoRow.jsx
│   │   │   │   ├── LevelsCard.jsx
│   │   │   │   ├── Ma20Card.jsx
│   │   │   │   ├── MarketCard.jsx
│   │   │   │   ├── MiniMetric.jsx
│   │   │   │   ├── PriceCard.jsx
│   │   │   │   ├── RiskManagementCard.jsx
│   │   │   │   ├── RsiCard.jsx
│   │   │   │   ├── SectionCard.jsx
│   │   │   │   ├── SignalCard.jsx
│   │   │   │   ├── SuggestedOrderCard.jsx
│   │   │   │   └── TechnicalMetricsCard.jsx
│   │   │   ├── charts/
│   │   │   │   ├── MacdChart.jsx
│   │   │   │   ├── PriceVolumeChart.jsx
│   │   │   │   └── RsiChart.jsx
│   │   │   ├── controls/
│   │   │   │   ├── ExportPanel.jsx
│   │   │   │   └── SearchPanel.jsx
│   │   │   └── layout/
│   │   │       ├── ErrorAlert.jsx
│   │   │       ├── ErrorBoundary.jsx
│   │   │       ├── Header.jsx
│   │   │       ├── LanguageSwitcher.jsx
│   │   │       ├── LoadingState.jsx
│   │   │       └── RiskWarning.jsx
│   │   ├── config/
│   │   │   └── api.js
│   │   ├── constants/
│   │   │   └── actionStyles.js
│   │   ├── hooks/
│   │   │   └── useStockAnalysis.js
│   │   ├── i18n/
│   │   │   ├── backendTextTranslations.js
│   │   │   ├── LanguageContext.jsx
│   │   │   └── translations.js
│   │   ├── services/
│   │   │   └── stockApi.js
│   │   ├── utils/
│   │   │   └── formatters.js
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .env.example
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── README.md
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── .gitignore
├── README.md
└── render.yaml
```

The uploaded ZIP also contains local/generated folders such as `.git/`, `frontend/node_modules/`, and `backend/__pycache__/`. These should not be committed to a clean public GitHub repository.

---

### Backend Overview

The backend is a Flask API located in the `backend/` folder.

Important backend files:

| File | Purpose |
|---|---|
| `backend/app.py` | Flask app factory, CORS setup, health check, error handlers, security headers |
| `backend/extensions.py` | Shared Flask extensions such as rate limiter |
| `backend/constants.py` | Common constants such as data source and risk warning |
| `backend/config.py` | Developer/config values loaded from environment variables |
| `backend/routes/stock_routes.py` | Stock analysis API route |
| `backend/routes/export_routes.py` | Excel export API route |
| `backend/services/stock_service.py` | Main stock data fetching and analysis service |
| `backend/services/export_service.py` | Excel report generation service |
| `backend/services/analysis_service.py` | Reference-only signal scoring and suggested order logic |
| `backend/services/market_service.py` | VNINDEX market context analysis |
| `backend/utils/indicators.py` | RSI, MACD, Bollinger Bands, moving averages |
| `backend/utils/dataframe_utils.py` | OHLCV DataFrame cleaning and normalization |
| `backend/utils/validators.py` | Symbol and date validation |
| `backend/utils/simple_cache.py` | Simple in-memory response cache |
| `backend/utils/json_utils.py` | JSON-safe conversion for NumPy/Pandas values |
| `backend/requirements.txt` | Python dependencies |

Backend production-related features:

- CORS restricted by environment variables
- `debug=False` when running directly
- Gunicorn start command in `render.yaml`
- Rate limiting for API endpoints
- Health check endpoint
- Safe error handling without exposing raw stack traces to users

---

### Frontend Overview

The frontend is a React/Vite application located in the `frontend/` folder.

Important frontend files:

| File | Purpose |
|---|---|
| `frontend/src/App.jsx` | Main application layout and dashboard composition |
| `frontend/src/main.jsx` | React entry point |
| `frontend/src/config/api.js` | API base URL configuration using `VITE_API_URL` |
| `frontend/src/services/stockApi.js` | Axios API functions |
| `frontend/src/hooks/useStockAnalysis.js` | Main state management hook for search, export, loading, and errors |
| `frontend/src/components/controls/SearchPanel.jsx` | Stock symbol search form |
| `frontend/src/components/controls/ExportPanel.jsx` | Excel export controls |
| `frontend/src/components/cards/PriceCard.jsx` | Current price and price change display |
| `frontend/src/components/cards/TechnicalMetricsCard.jsx` | Technical indicator summary |
| `frontend/src/components/charts/PriceVolumeChart.jsx` | Price and volume chart |
| `frontend/src/components/charts/RsiChart.jsx` | RSI chart |
| `frontend/src/components/charts/MacdChart.jsx` | MACD chart |
| `frontend/src/components/layout/RiskWarning.jsx` | Disclaimer/risk warning UI |
| `frontend/src/i18n/LanguageContext.jsx` | Language state provider |
| `frontend/src/i18n/translations.js` | Frontend UI translations |
| `frontend/package.json` | Frontend dependencies and scripts |
| `frontend/vite.config.js` | Vite configuration |
| `frontend/tailwind.config.js` | Tailwind CSS configuration |

Frontend features include:

- Vietnamese/English language support
- Loading and error UI states
- Symbol validation
- Date validation for Excel export
- Responsive dashboard layout
- Chart rendering with Recharts

---

### API Endpoints

#### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "VSDAT backend"
}
```

#### Get Stock Analysis

```http
GET /stock/<symbol>
```

Example:

```http
GET /stock/VIC
```

Example response shape:

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
  "technical": {
    "rsi14": 45.2,
    "ma20": 220000,
    "ma50": 218500,
    "ma100": 215000,
    "ma200": 210000,
    "macd": 120.5,
    "macdSignal": 95.3,
    "macdHistogram": 25.2
  },
  "data": []
}
```

Price status logic:

```text
priceChange > 0  -> status = "up", color = "green"
priceChange < 0  -> status = "down", color = "red"
priceChange == 0 -> status = "unchanged", color = "yellow"
```

#### Export Historical Data to Excel

```http
GET /export/<symbol>/<start_date>/<end_date>
```

Example:

```http
GET /export/VIC/2024-01-01/2024-12-31
```

Date format:

```text
YYYY-MM-DD
```

The endpoint returns an Excel file containing historical OHLCV data.

---

### Excel Export

The Excel export feature generates an `.xlsx` file in memory using `BytesIO`.

The exported file may include:

- Stock symbol
- Date
- Open price
- High price
- Low price
- Close price
- Volume
- Price change
- Percentage change
- Basic formatting
- Educational/data analysis disclaimer

Export validation includes:

- Valid stock symbol format
- Valid date format
- `start_date <= end_date`
- No future end date
- Maximum export range and row limit

---

### Installation

#### Prerequisites

Install the following tools first:

- Python 3.10.12
- Node.js and npm
- Git

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

---

### Environment Variables

#### Frontend

Create `frontend/.env`:

```env
VITE_API_URL=https://vsdat-backend-1.onrender.com
```

For local development:

```env
VITE_API_URL=http://127.0.0.1:5000
```

#### Backend

Create `backend/.env` if you run the backend locally with environment loading, or configure these variables directly on Render:

```env
FRONTEND_URL=https://vsdat-frontend.onrender.com
FLASK_ENV=production
PYTHON_VERSION=3.10.12
```

Optional backend variables:

```env
CORS_EXTRA_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
STOCK_CACHE_TTL_SECONDS=60
RATELIMIT_DEFAULT=120 per minute
RATELIMIT_DAILY=1000 per day
LOG_LEVEL=INFO
DEVELOPER_EMAIL=
DEVELOPER_GITHUB=https://github.com/tuanda2309
DEVELOPER_WEB=https://vsdat-frontend.onrender.com
```

Do not commit real `.env` files to GitHub.

---

### Running Locally

#### Backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Activate the virtual environment on macOS/Linux:

```bash
source venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
python app.py
```

Backend local URL:

```text
http://127.0.0.1:5000
```

Test the health endpoint:

```bash
curl http://127.0.0.1:5000/health
```

#### Frontend

```bash
cd frontend
npm install
```

Create `.env` from the example file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
copy .env.example .env
```

Run the development server:

```bash
npm run dev
```

Build the production frontend:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

---

### Deployment on Render

This project includes `render.yaml` for Render deployment.

#### Backend on Render

Recommended settings:

```text
Service Type: Web Service
Runtime: Python
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: gunicorn --workers 2 --threads 4 --timeout 60 app:app
Health Check Path: /health
Python Version: 3.10.12
```

Backend environment variables:

```env
PYTHON_VERSION=3.10.12
FLASK_ENV=production
FRONTEND_URL=https://vsdat-frontend.onrender.com
CORS_EXTRA_ORIGINS=
STOCK_CACHE_TTL_SECONDS=60
RATELIMIT_DEFAULT=120 per minute
RATELIMIT_DAILY=1000 per day
LOG_LEVEL=INFO
```

Backend production URL:

```text
https://vsdat-backend-1.onrender.com
```

#### Frontend on Render

Recommended settings:

```text
Service Type: Static Site
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

Frontend environment variable:

```env
VITE_API_URL=https://vsdat-backend-1.onrender.com
```

Frontend production URL:

```text
https://vsdat-frontend.onrender.com
```

---

### Limitations

- Stock data depends on an external Vietnamese stock data provider.
- Data may be delayed, incomplete, or temporarily unavailable.
- Render free tier may sleep after inactivity.
- In-memory cache is simple and resets when the backend restarts.
- The project does not guarantee real-time accuracy.
- Technical indicators are reference-only.
- Signal, risk, and suggested order cards are for learning/data analysis practice only.
- This project does not provide financial advice or investment recommendations.

---

### Disclaimer

This project is for educational and data analysis purposes only. It is not financial advice. Stock market data may be delayed, incomplete, or inaccurate. Users should not make investment decisions based only on this application.

---

### Future Improvements

- Add automated tests for backend APIs
- Add frontend component tests
- Add CI/CD workflow
- Add Redis cache for better production scalability
- Add more market overview features
- Add watchlist functionality
- Add comparison between multiple stock symbols
- Add more technical indicators
- Add PDF export
- Add user authentication
- Add better monitoring and error tracking
- Improve accessibility and mobile experience
- Add official GitHub Pages or documentation site

---

### Author

**Đoàn Anh Tuấn**

- Email: doananhtuan77qn@gmail.com
- GitHub: [Your GitHub Profile](https://github.com/YOUR_USERNAME)

---

<br />

## Tiếng Việt

### Tên dự án

**Vietnam Stock Data Analysis Terminal (VSDAT)**

### Link Demo

[🚀 Live Demo](https://vsdat-frontend.onrender.com)

Frontend URL:

```text
https://vsdat-frontend.onrender.com
```

Backend URL:

```text
https://vsdat-backend-1.onrender.com
```

---

### Chọn ngôn ngữ

🌐 Ngôn ngữ: [English](#english) | [Tiếng Việt](#tiếng-việt)

---

### Tổng quan dự án

**Vietnam Stock Data Analysis Terminal (VSDAT)** là ứng dụng web full-stack dùng để phân tích dữ liệu chứng khoán Việt Nam. Ứng dụng cho phép người dùng nhập mã cổ phiếu, lấy dữ liệu giá, xem giá hiện tại, trạng thái tăng/giảm, biểu đồ giá, chỉ báo kỹ thuật, dashboard phân tích và xuất dữ liệu lịch sử OHLCV ra file Excel.

Dự án được xây dựng nhằm thể hiện các kỹ năng:

- Xây dựng ứng dụng full-stack với React/Vite và Flask
- Thiết kế REST API
- Xử lý dữ liệu bằng Pandas và NumPy
- Tính toán chỉ báo kỹ thuật
- Trực quan hóa dữ liệu tài chính
- Tạo báo cáo Excel
- Deploy ứng dụng ở mức production basic trên Render

> VSDAT không phải là công cụ khuyến nghị đầu tư. Tất cả biểu đồ, chỉ báo, tín hiệu và dữ liệu xuất ra chỉ phục vụ mục đích học tập và phân tích dữ liệu.

---

### Tính năng chính

- Tra cứu mã cổ phiếu Việt Nam
- Hiển thị thông tin giá hiện tại
- Hiển thị mức tăng/giảm và phần trăm thay đổi
- Xác định trạng thái cổ phiếu: tăng, giảm hoặc không đổi
- Dashboard phân tích kỹ thuật
- Biểu đồ giá và khối lượng
- Biểu đồ RSI
- Biểu đồ MACD
- Đường trung bình MA20, MA50, MA100, MA200
- Chỉ báo RSI
- Chỉ báo MACD và đường signal
- Tính toán Bollinger Bands ở backend
- Mức hỗ trợ và kháng cự tham khảo
- Bối cảnh thị trường VNINDEX nếu có dữ liệu
- Chấm điểm tín hiệu và cảnh báo chỉ mang tính tham khảo
- Thẻ quản trị rủi ro chỉ phục vụ học tập/phân tích
- Xuất dữ liệu lịch sử OHLCV ra Excel
- Trạng thái loading và error rõ ràng
- Validate mã cổ phiếu và ngày xuất dữ liệu ở frontend
- Validate input ở backend
- Rate limit cơ bản ở backend
- Cache response đơn giản
- Cấu hình deploy production trên Render

---

### Hình ảnh giao diện

| Giao diện tra cứu chính | Dashboard phân tích kỹ thuật |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/07defeb9-a194-4e39-8978-65ba8af11b10" width="100%" alt="VSDAT Home Interface" /> | <img src="https://github.com/user-attachments/assets/0b1b5455-425c-4893-b947-d54d2acbaa49" width="100%" alt="VSDAT Technical Analysis Dashboard" /> |
| Nhập mã cổ phiếu và điều khiển xuất Excel | Dashboard chính với thẻ phân tích kỹ thuật và biểu đồ |

| Biểu đồ chỉ báo RSI | File Excel được tạo |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/30219a3f-dc33-4bb2-bd7a-56bfcf78d824" width="100%" alt="VSDAT RSI Indicator Chart" /> | <img src="https://github.com/user-attachments/assets/a5f6e01f-8570-42f9-b69f-19b377dc01d8" width="100%" alt="VSDAT Generated Excel Sheet" /> |
| Trực quan hóa RSI để phân tích động lượng | File Excel OHLCV được xuất để tiếp tục phân tích |

---

### Công nghệ sử dụng

#### Frontend

- React
- Vite
- Tailwind CSS
- Axios
- Recharts
- Lucide React
- JavaScript

#### Backend

- Python 3.10.12
- Flask
- Flask-CORS
- Flask-Limiter
- Gunicorn

#### Xử lý dữ liệu

- Pandas
- NumPy
- vnstock / vnstock3 làm nguồn dữ liệu chứng khoán Việt Nam

#### Xuất Excel

- openpyxl
- BytesIO để tạo file Excel trong bộ nhớ

#### Deploy

- Render

---

### Cấu trúc dự án

Cấu trúc dưới đây dựa trên file ZIP project đã gửi.

```text
VSDAT/
├── backend/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── export_routes.py
│   │   └── stock_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── analysis_service.py
│   │   ├── export_service.py
│   │   ├── market_service.py
│   │   └── stock_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── dataframe_utils.py
│   │   ├── helpers.py
│   │   ├── indicators.py
│   │   ├── json_utils.py
│   │   ├── risk.py
│   │   ├── simple_cache.py
│   │   ├── support_resistance.py
│   │   └── validators.py
│   ├── .env.example
│   ├── app.py
│   ├── config.py
│   ├── constants.py
│   ├── extensions.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │   ├── cat-logo.png
│   │   ├── favicon.svg
│   │   └── icons.svg
│   ├── src/
│   │   ├── assets/
│   │   │   ├── hero.png
│   │   │   ├── react.svg
│   │   │   └── vite.svg
│   │   ├── components/
│   │   │   ├── cards/
│   │   │   │   ├── ChecklistCard.jsx
│   │   │   │   ├── InfoRow.jsx
│   │   │   │   ├── LevelsCard.jsx
│   │   │   │   ├── Ma20Card.jsx
│   │   │   │   ├── MarketCard.jsx
│   │   │   │   ├── MiniMetric.jsx
│   │   │   │   ├── PriceCard.jsx
│   │   │   │   ├── RiskManagementCard.jsx
│   │   │   │   ├── RsiCard.jsx
│   │   │   │   ├── SectionCard.jsx
│   │   │   │   ├── SignalCard.jsx
│   │   │   │   ├── SuggestedOrderCard.jsx
│   │   │   │   └── TechnicalMetricsCard.jsx
│   │   │   ├── charts/
│   │   │   │   ├── MacdChart.jsx
│   │   │   │   ├── PriceVolumeChart.jsx
│   │   │   │   └── RsiChart.jsx
│   │   │   ├── controls/
│   │   │   │   ├── ExportPanel.jsx
│   │   │   │   └── SearchPanel.jsx
│   │   │   └── layout/
│   │   │       ├── ErrorAlert.jsx
│   │   │       ├── ErrorBoundary.jsx
│   │   │       ├── Header.jsx
│   │   │       ├── LanguageSwitcher.jsx
│   │   │       ├── LoadingState.jsx
│   │   │       └── RiskWarning.jsx
│   │   ├── config/
│   │   │   └── api.js
│   │   ├── constants/
│   │   │   └── actionStyles.js
│   │   ├── hooks/
│   │   │   └── useStockAnalysis.js
│   │   ├── i18n/
│   │   │   ├── backendTextTranslations.js
│   │   │   ├── LanguageContext.jsx
│   │   │   └── translations.js
│   │   ├── services/
│   │   │   └── stockApi.js
│   │   ├── utils/
│   │   │   └── formatters.js
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .env.example
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── README.md
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── .gitignore
├── README.md
└── render.yaml
```

File ZIP hiện tại cũng có các thư mục local/generated như `.git/`, `frontend/node_modules/`, và `backend/__pycache__/`. Các thư mục này không nên commit lên GitHub public.

---

### Tổng quan Backend

Backend là Flask API nằm trong thư mục `backend/`.

Các file backend quan trọng:

| File | Vai trò |
|---|---|
| `backend/app.py` | Khởi tạo Flask app, cấu hình CORS, health check, xử lý lỗi, security headers |
| `backend/extensions.py` | Chứa extension dùng chung như rate limiter |
| `backend/constants.py` | Chứa hằng số dùng chung như nguồn dữ liệu và cảnh báo rủi ro |
| `backend/config.py` | Cấu hình/developer values lấy từ biến môi trường |
| `backend/routes/stock_routes.py` | Route API phân tích cổ phiếu |
| `backend/routes/export_routes.py` | Route API xuất file Excel |
| `backend/services/stock_service.py` | Service chính để lấy và phân tích dữ liệu cổ phiếu |
| `backend/services/export_service.py` | Service tạo báo cáo Excel |
| `backend/services/analysis_service.py` | Logic chấm điểm tín hiệu tham khảo |
| `backend/services/market_service.py` | Phân tích bối cảnh thị trường VNINDEX |
| `backend/utils/indicators.py` | Tính RSI, MACD, Bollinger Bands, MA |
| `backend/utils/dataframe_utils.py` | Làm sạch và chuẩn hóa DataFrame OHLCV |
| `backend/utils/validators.py` | Validate mã cổ phiếu và ngày |
| `backend/utils/simple_cache.py` | Cache response đơn giản trong bộ nhớ |
| `backend/utils/json_utils.py` | Chuyển đổi NumPy/Pandas values về JSON-safe |
| `backend/requirements.txt` | Danh sách thư viện Python |

Backend có các phần phục vụ production basic:

- CORS cấu hình qua biến môi trường
- Không bật debug trong production
- Start command bằng Gunicorn trong `render.yaml`
- Rate limit cho API endpoints
- Endpoint kiểm tra trạng thái `/health`
- Xử lý lỗi an toàn, không trả stack trace thô cho người dùng

---

### Tổng quan Frontend

Frontend là ứng dụng React/Vite nằm trong thư mục `frontend/`.

Các file frontend quan trọng:

| File | Vai trò |
|---|---|
| `frontend/src/App.jsx` | Layout chính và ghép các phần dashboard |
| `frontend/src/main.jsx` | Entry point của React |
| `frontend/src/config/api.js` | Cấu hình API base URL bằng `VITE_API_URL` |
| `frontend/src/services/stockApi.js` | Các hàm gọi API bằng Axios |
| `frontend/src/hooks/useStockAnalysis.js` | Hook quản lý state tìm kiếm, xuất Excel, loading và lỗi |
| `frontend/src/components/controls/SearchPanel.jsx` | Form nhập mã cổ phiếu |
| `frontend/src/components/controls/ExportPanel.jsx` | Form xuất Excel |
| `frontend/src/components/cards/PriceCard.jsx` | Hiển thị giá hiện tại và tăng/giảm |
| `frontend/src/components/cards/TechnicalMetricsCard.jsx` | Hiển thị chỉ báo kỹ thuật |
| `frontend/src/components/charts/PriceVolumeChart.jsx` | Biểu đồ giá và khối lượng |
| `frontend/src/components/charts/RsiChart.jsx` | Biểu đồ RSI |
| `frontend/src/components/charts/MacdChart.jsx` | Biểu đồ MACD |
| `frontend/src/components/layout/RiskWarning.jsx` | Cảnh báo rủi ro trên giao diện |
| `frontend/src/i18n/LanguageContext.jsx` | Provider quản lý ngôn ngữ |
| `frontend/src/i18n/translations.js` | Nội dung dịch giao diện |
| `frontend/package.json` | Dependencies và scripts frontend |
| `frontend/vite.config.js` | Cấu hình Vite |
| `frontend/tailwind.config.js` | Cấu hình Tailwind CSS |

Frontend có các tính năng:

- Hỗ trợ giao diện tiếng Anh/tiếng Việt
- Loading state và error state
- Validate mã cổ phiếu
- Validate ngày khi xuất Excel
- Dashboard responsive
- Hiển thị biểu đồ bằng Recharts

---

### API endpoints

#### Kiểm tra backend

```http
GET /health
```

Ví dụ response:

```json
{
  "status": "ok",
  "service": "VSDAT backend"
}
```

#### Lấy dữ liệu phân tích cổ phiếu

```http
GET /stock/<symbol>
```

Ví dụ:

```http
GET /stock/VIC
```

Ví dụ dạng response:

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
  "technical": {
    "rsi14": 45.2,
    "ma20": 220000,
    "ma50": 218500,
    "ma100": 215000,
    "ma200": 210000,
    "macd": 120.5,
    "macdSignal": 95.3,
    "macdHistogram": 25.2
  },
  "data": []
}
```

Logic trạng thái giá:

```text
priceChange > 0  -> status = "up", color = "green"
priceChange < 0  -> status = "down", color = "red"
priceChange == 0 -> status = "unchanged", color = "yellow"
```

#### Xuất dữ liệu lịch sử ra Excel

```http
GET /export/<symbol>/<start_date>/<end_date>
```

Ví dụ:

```http
GET /export/VIC/2024-01-01/2024-12-31
```

Định dạng ngày:

```text
YYYY-MM-DD
```

API sẽ trả về file Excel chứa dữ liệu OHLCV lịch sử.

---

### Chức năng xuất Excel

Chức năng xuất Excel tạo file `.xlsx` trong bộ nhớ bằng `BytesIO`.

File Excel có thể bao gồm:

- Mã cổ phiếu
- Ngày giao dịch
- Giá mở cửa
- Giá cao nhất
- Giá thấp nhất
- Giá đóng cửa
- Khối lượng giao dịch
- Mức thay đổi giá
- Phần trăm thay đổi
- Định dạng bảng cơ bản
- Disclaimer phục vụ học tập và phân tích dữ liệu

Validate export bao gồm:

- Mã cổ phiếu hợp lệ
- Định dạng ngày hợp lệ
- `start_date <= end_date`
- Không cho ngày tương lai
- Giới hạn khoảng ngày và số dòng export

---

### Cài đặt

#### Yêu cầu

Cài đặt trước:

- Python 3.10.12
- Node.js và npm
- Git

Clone repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

---

### Biến môi trường

#### Frontend

Tạo file `frontend/.env`:

```env
VITE_API_URL=https://vsdat-backend-1.onrender.com
```

Khi chạy local:

```env
VITE_API_URL=http://127.0.0.1:5000
```

#### Backend

Tạo `backend/.env` nếu bạn chạy local với cơ chế load biến môi trường, hoặc cấu hình trực tiếp trên Render:

```env
FRONTEND_URL=https://vsdat-frontend.onrender.com
FLASK_ENV=production
PYTHON_VERSION=3.10.12
```

Biến môi trường tùy chọn:

```env
CORS_EXTRA_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
STOCK_CACHE_TTL_SECONDS=60
RATELIMIT_DEFAULT=120 per minute
RATELIMIT_DAILY=1000 per day
LOG_LEVEL=INFO
DEVELOPER_EMAIL=
DEVELOPER_GITHUB=https://github.com/tuanda2309
DEVELOPER_WEB=https://vsdat-frontend.onrender.com
```

Không commit file `.env` thật lên GitHub.

---

### Chạy local

#### Backend

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

Cài đặt thư viện backend:

```bash
pip install -r requirements.txt
```

Chạy backend:

```bash
python app.py
```

Backend local URL:

```text
http://127.0.0.1:5000
```

Test endpoint health:

```bash
curl http://127.0.0.1:5000/health
```

#### Frontend

```bash
cd frontend
npm install
```

Tạo file `.env` từ file mẫu:

```bash
cp .env.example .env
```

Trên Windows PowerShell:

```powershell
copy .env.example .env
```

Chạy development server:

```bash
npm run dev
```

Build frontend production:

```bash
npm run build
```

Preview bản build:

```bash
npm run preview
```

---

### Deploy trên Render

Project có sẵn file `render.yaml` để deploy trên Render.

#### Backend trên Render

Cấu hình đề xuất:

```text
Service Type: Web Service
Runtime: Python
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: gunicorn --workers 2 --threads 4 --timeout 60 app:app
Health Check Path: /health
Python Version: 3.10.12
```

Biến môi trường backend:

```env
PYTHON_VERSION=3.10.12
FLASK_ENV=production
FRONTEND_URL=https://vsdat-frontend.onrender.com
CORS_EXTRA_ORIGINS=
STOCK_CACHE_TTL_SECONDS=60
RATELIMIT_DEFAULT=120 per minute
RATELIMIT_DAILY=1000 per day
LOG_LEVEL=INFO
```

Backend production URL:

```text
https://vsdat-backend-1.onrender.com
```

#### Frontend trên Render

Cấu hình đề xuất:

```text
Service Type: Static Site
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

Biến môi trường frontend:

```env
VITE_API_URL=https://vsdat-backend-1.onrender.com
```

Frontend production URL:

```text
https://vsdat-frontend.onrender.com
```

---

### Hạn chế

- Dữ liệu chứng khoán phụ thuộc vào nguồn dữ liệu bên ngoài.
- Dữ liệu có thể bị trễ, thiếu hoặc tạm thời không khả dụng.
- Render free tier có thể sleep sau một thời gian không hoạt động.
- Cache hiện tại là cache đơn giản trong bộ nhớ và sẽ reset khi backend restart.
- Project không đảm bảo độ chính xác realtime tuyệt đối.
- Chỉ báo kỹ thuật chỉ mang tính tham khảo.
- Các thẻ tín hiệu, quản trị rủi ro và gợi ý lệnh chỉ phục vụ học tập/phân tích dữ liệu.
- Dự án không đưa ra lời khuyên tài chính hoặc khuyến nghị đầu tư.

---

### Lưu ý rủi ro

Dự án chỉ phục vụ mục đích học tập và phân tích dữ liệu, không phải khuyến nghị đầu tư. Dữ liệu chứng khoán có thể bị trễ, thiếu hoặc sai lệch. Người dùng không nên đưa ra quyết định đầu tư chỉ dựa trên ứng dụng này.

---

### Hướng phát triển

- Thêm automated tests cho backend API
- Thêm frontend component tests
- Thêm CI/CD workflow
- Thêm Redis cache để tăng khả năng scale production
- Thêm tính năng tổng quan thị trường
- Thêm watchlist cổ phiếu
- Thêm chức năng so sánh nhiều mã cổ phiếu
- Thêm nhiều chỉ báo kỹ thuật hơn
- Thêm xuất báo cáo PDF
- Thêm đăng nhập người dùng
- Thêm monitoring và error tracking
- Cải thiện accessibility và trải nghiệm mobile
- Thêm trang tài liệu hoặc GitHub Pages chính thức

---

### Tác giả

**Đoàn Anh Tuấn**

- Email: doananhtuan77qn@gmail.com
- GitHub: [Tuanda2309](https://github.com/tuanda2309)
