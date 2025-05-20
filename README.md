# Financial Data API

A Flask-based REST API that provides financial data and analytics using the Yahoo Finance API.

## Features

- Company information retrieval
- Real-time stock market data
- Historical market data with customizable date ranges
- Analytical insights with technical indicators

## API Endpoints

### 1. Company Information
```
GET /api/company_info/<symbol>
```
Retrieves detailed company information including full company name, business summary, industry, sector, and key officers.

### 2. Stock Market Data
```
GET /api/stock_data/<symbol>
```
Fetches real-time stock market data including current price, price change, percentage change, and other metrics.

### 3. Historical Market Data
```
POST /api/historical_data
```
Returns historical market data for a specified company symbol within a given date range.

**Request Body:**
```json
{
  "symbol": "AAPL",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "interval": "1d"
}
```

### 4. Analytical Insights
```
GET /api/analytics/<symbol>
```
Performs comprehensive analysis of the company based on historical data and delivers actionable insights.

## Installation

1. Clone this repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run the application:
```
python app.py
```

## Usage Examples

### Get Company Information
```
curl http://localhost:5000/api/company_info/AAPL
```

### Get Real-time Stock Data
```
curl http://localhost:5000/api/stock_data/MSFT
```

### Get Historical Data
```
curl -X POST http://localhost:5000/api/historical_data \
  -H "Content-Type: application/json" \
  -d '{"symbol":"GOOGL","start_date":"2023-01-01","end_date":"2023-12-31"}'
```

### Get Analytics
```
curl http://localhost:5000/api/analytics/AMZN
```

## Technologies Used

- Flask
- yfinance (Yahoo Finance API)
