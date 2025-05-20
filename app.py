from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import functools

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to the Financial Data API',
        'endpoints': {
            '/api/company_info/<symbol>': 'Get detailed company information',
            '/api/realstock/<symbol>': 'Get real-time stock market data',
            '/api/historical_data': 'Get historical market data (POST request with date range)'        }
    })

@app.route('/api/company_info/<symbol>', methods=['GET'])
def get_company_info(symbol):
    """
    Retrieve detailed company information by symbol
    """
    try:
        # Get company information from Yahoo Finance
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Extract relevant information
        company_info = {
            'symbol': symbol,
            'name': info.get('longName', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'business_summary': info.get('longBusinessSummary', 'N/A'),
            'website': info.get('website', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'employees': info.get('fullTimeEmployees', 'N/A'),
            'country': info.get('country', 'N/A'),
            'city': info.get('city', 'N/A')
        }
        
        # Get company officers if available
        if 'companyOfficers' in info and info['companyOfficers']:
            officers = []
            for officer in info['companyOfficers']:
                officers.append({
                    'name': officer.get('name', 'N/A'),
                    'title': officer.get('title', 'N/A'),
                    'year_born': officer.get('yearBorn', 'N/A')
                })
            company_info['officers'] = officers
        
        return jsonify({
            'status': 'success',
            'data': company_info
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/realstock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """
    Retrieve real-time stock market data by symbol
    """
    try:
        # Get stock data from Yahoo Finance
        ticker = yf.Ticker(symbol)
        
        # Get the latest market data
        data = ticker.history(period='1d')
        
        if data.empty:
            return jsonify({
                'status': 'error',
                'message': f'No data found for symbol: {symbol}'
            }), 404
        
        # Get the latest quote
        latest = data.iloc[-1]
        
        # Get additional info
        info = ticker.info
        
        stock_data = {
            'symbol': symbol,
            'company_name': info.get('longName', 'N/A'),
            'current_price': latest['Close'],
            'open': latest['Open'],
            'high': latest['High'],
            'low': latest['Low'],
            'volume': latest['Volume'],
            'previous_close': info.get('previousClose', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
            'market_state': info.get('marketState', 'N/A'),
            'exchange': info.get('exchange', 'N/A'),
            'currency': info.get('currency', 'N/A'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Calculate price change and percentage
        if 'previousClose' in info and info['previousClose']:
            prev_close = info['previousClose']
            price_change = latest['Close'] - prev_close
            percent_change = (price_change / prev_close) * 100
            
            stock_data['price_change'] = round(price_change, 2)
            stock_data['percent_change'] = round(percent_change, 2)
        
        return jsonify({
            'status': 'success',
            'data': stock_data
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/historical_data', methods=['POST'])
def get_historical_data():
    """
    Retrieve historical market data for a symbol within a date range
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400
        
        # Extract parameters
        symbol = data.get('symbol')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        interval = data.get('interval', '1d')  # Default to daily
        
        if not symbol:
            return jsonify({
                'status': 'error',
                'message': 'Symbol is required'
            }), 400
        
        if not start_date:
            # Default to 1 year ago if not provided
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        if not end_date:
            # Default to today if not provided
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Valid intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        # m- minutes, mo-month interval
        valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
        if interval not in valid_intervals:
            interval = '1d'  # Default to daily if invalid
        
        # Get historical data
        ticker = yf.Ticker(symbol)
        hist_data = ticker.history(start=start_date, end=end_date, interval=interval)
        
        if hist_data.empty:
            return jsonify({
                'status': 'error',
                'message': f'No historical data found for symbol: {symbol} in the specified date range'
            }), 404
        
        # Convert to dictionary format
        hist_data_dict = []
        for date, row in hist_data.iterrows():
            hist_data_dict.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume']
            })
        
        return jsonify({
            'status': 'success',
            'data': {
                'symbol': symbol,
                'start_date': start_date,
                'end_date': end_date,
                'interval': interval,
                'history': hist_data_dict
            }
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
