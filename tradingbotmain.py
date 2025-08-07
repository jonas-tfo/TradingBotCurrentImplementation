from multiprocessing import util
from tradingfunctions import * 
import datetime
import time
import math
from ib_insync import IB, Stock, MarketOrder, StopOrder
import traceback
import asyncio


US_EXCHANGES = ['NYQ', 'NMS', 'ASE', 'AMEX', 'OTC', 'TSX', 'NASDAQ', 'NYSE', "SMART"]
EUROPEAN_EXCHANGES = ['IBIS', 'DTB', 'FRA', 'LSE', "GER", "XETRA", "TLX"]

sp500_tickers = [
    'MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ATVI', 'ADM', 'ADBE', 'ADP', 'AAP', 'AES', 'AFL',
    'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG',
    'MO', 'AMZN', 'AMCR', 'AMD', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP',
    'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ANET',
    'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'AZO', 'AVB', 'AVY', 'AXON', 'BKR', 'BALL', 'BAC',
    'BBWI', 'BAX', 'BDX', 'WRB', 'BRK.B', 'BBY', 'BIO', 'TECH', 'BIIB', 'BLK', 'BK', 'BA',
    'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF.B', 'BG', 'CHRW', 'CDNS',
    'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT', 'CBOE', 'CBRE',
    'CDW', 'CE', 'CNC', 'CNP', 'CDAY', 'CF', 'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB',
    'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CLX', 'CME', 'CMS', 'KO', 'CTSH',
    'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CTVA',
    'CSGP', 'COST', 'CTRA', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE',
    'DAL', 'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DIS', 'DG', 'DLTR', 'D', 'DPZ',
    'DOV', 'DOW', 'DTE', 'DUK', 'DD', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA',
    'ELV', 'LLY', 'EMR', 'ENPH', 'ETR', 'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS',
    'EL', 'ETSY', 'RE', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS',
    'FICO', 'FAST', 'FRT', 'FDX', 'FITB', 'FRC', 'FE', 'FIS', 'FISV', 'FLT', 'FMC', 'F',
    'FTNT', 'FTV', 'FOXA', 'FOX', 'BEN', 'FCX', 'GRMN', 'IT', 'GEHC', 'GEN', 'GNRC', 'GD',
    'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GL', 'GPN', 'GS', 'HAL', 'HBI', 'HAS', 'HCA', 'PEAK',
    'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ',
    'HUM', 'HBAN', 'HII', 'IBM', 'IEX', 'IDXX', 'ITW', 'ILMN', 'INCY', 'IR', 'PODD', 'INTC',
    'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'INVH', 'IQV', 'IRM', 'JBHT', 'JKHY',
    'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KDP', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC',
    'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN', 'LNC', 'LIN', 'LYV', 'LKQ',
    'LMT', 'L', 'LOW', 'LUMN', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS',
    'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM', 'MCHP', 'MU',
    'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS',
    'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NKE', 'NI',
    'NDSN', 'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY',
    'ODFL', 'OMC', 'ON', 'OKE', 'ORCL', 'OGN', 'OTIS', 'PCAR', 'PKG', 'PARA', 'PH', 'PAYX',
    'PAYC', 'PYPL', 'PNR', 'PEP', 'PKI', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PNC',
    'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM',
    'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG',
    'RMD', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX',
    'SEE', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SJM', 'SNA', 'SEDG', 'SO', 'LUV', 'SWK',
    'SBUX', 'STT', 'STE', 'SYK', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR',
    'TRGP', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO',
    'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TYL', 'TSN', 'USB', 'UDR', 'ULTA', 'UNP', 'UAL',
    'UPS', 'URI', 'UNH', 'UHS', 'VLO', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VFC', 'VTRS',
    'VICI', 'V', 'VMC', 'WAB', 'WBA', 'WMT', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', 'WELL',
    'WST', 'WDC', 'WRK', 'WY', 'WHR', 'WMB', 'WTW', 'GWW', 'WYNN', 'XEL', 'XYL', 'YUM',
    'ZBRA', 'ZBH', 'ZION', 'ZTS', "MBLY", "DELL"
]

# Expanded lists of German stocks from various indices

dax40_tickers = [
    "ADS", "AIR", "ALV", "BAS", "BAYN", "BEI", "BMW", "BNR", "CON", "DHER",
    "DTG", "DTE", "EOAN", "FME", "FRE", "HEN3", "HEI", "HFG", "IFX", "LEG",
    "LIN", "MRK", "MTX", "MUV2", "PAH3", "PBB", "PUM", "QIA", "RHM", "RWE",
    "SAP", "SART", "SIE", "SY1", "TKA", "VNA", "VOW3", "VOW", "ZAL", "TUI1",
    "P911"
]

sdax_tickers = [
    "AIXA", "ASIZ", "BNHL", "CELA", "COS", "DELG", "DIC", "ESEG", "FREN", "GESA",
    "HNR", "IGL", "KRON", "LEIW", "MANU", "NEUB", "ODXA", "PRIA", "QANT", "RABA", "AFX"
]

mdax_tickers = [
    "ALDI", "BAIN", "CUNA", "DIFO", "ELOX", "FIRE", "GOMA", "HUMA", "IVIA", "JUMO",
    "KUKA", "LUBA", "MIRA", "NEUM", "OPTB", "PUMA", "QUEN", "ROTI", "SONN", "TROX"
]

tecdax_tickers = [
    "ANDI", "BRAU", "CONX", "DANU", "EPEX", "FONI", "GRAV", "HOF", "INTU", "JAZZ",
    "KIWI", "LEON", "MANTA", "NEXO", "ORIX", "PEGA", "QUAD", "RADI", "SIMO", "TECH"
]

german_tickers = dax40_tickers + sdax_tickers + mdax_tickers + tecdax_tickers

class MinimalTradingApp:

    def __init__(self):

        # Initialize IB connection
        try:
            self.ib = IB()
            self.ib.connect('127.0.0.1', 7497, clientId=1)

            if not self.ib or not self.ib.isConnected():
                print("Failed to connect to IB")
                self.ib = None
        except Exception as e:
            print(f"Failed to initialize IB connection: {e}")
            self.ib = None


    """
    Stock related functions
    """
        
        
    def us_market_is_open(self):
        try:
            from zoneinfo import ZoneInfo
            now = datetime.datetime.now(ZoneInfo("America/New_York"))
            is_weekday = now.weekday() < 5
            is_trading_hours = datetime.time(9, 20) <= now.time() <= datetime.time(16, 0)
            return is_weekday and is_trading_hours
        except ImportError:
            import pytz
            EST = pytz.timezone("America/New_York")
            now = datetime.datetime.now(EST)
            is_weekday = now.weekday() < 5
            is_trading_hours = datetime.time(9, 20) <= now.time() <= datetime.time(16, 0)
            return is_weekday and is_trading_hours


    def european_market_is_open(self):
        try:
            from zoneinfo import ZoneInfo
            now = datetime.datetime.now(ZoneInfo("Europe/Berlin"))
            is_weekday = now.weekday() < 5
            is_trading_hours = datetime.time(8, 0) <= now.time() <= datetime.time(17, 30)
            return is_weekday and is_trading_hours
        except ImportError:
            import pytz
            CET = pytz.timezone("Europe/Berlin")
            now = datetime.datetime.now(CET)
            is_weekday = now.weekday() < 5
            is_trading_hours = datetime.time(8, 0) <= now.time() <= datetime.time(17, 30)
            return is_weekday and is_trading_hours


    def get_correct_stock_symbol(self, stock):
        """Determine the correct stock symbol format based on the exchange."""
        # Try to get price with original symbol
        price = get_stock_closing_price(stock) # type: ignore
        if price and price > 0:
            return stock
        
        # Try with .DE extension
        german_symbol = f"{stock}.DE"
        price = get_stock_closing_price(german_symbol) # type: ignore 
        if price and price > 0:
            return german_symbol
            
        # If still no valid price, return original symbol
        return stock


    # gets the current unrealzed profit loss of a stock
    def get_unrealized_pl(self, stock):
        positions = self.ib.positions()
        stock_position = next((pos for pos in positions if pos.contract.symbol == stock), None)
        if stock_position is None:
            print(f"No position found for {stock}")
            return 0
        else:
            contract = stock_position.contract
            market_data = self.ib.reqMktData(contract, '', False, False)
            self.ib.sleep(1)
            current_price = market_data.last if market_data.last else market_data.close
            if current_price is None or current_price <= 0:
                current_price = get_stock_closing_price(stock) # type: ignore
            avg_cost = stock_position.avgCost
            position_size = stock_position.position
            unrealized_pnl = (current_price - avg_cost) * position_size
            return unrealized_pnl

  
    # Retrieve the stock exchange for a given stock symbol
    def get_stock_exchange(self, stock_symbol):
        """Get the correct exchange for a stock symbol."""
        # First check if it's a German stock by symbol or .DE extension
        base_symbol = stock_symbol.split('.')[0]
        if base_symbol in german_tickers or stock_symbol.endswith('.DE'):
            print(f"Identified {stock_symbol} as German stock")
            return 'IBIS'
            
        # Then check if it's a US stock
        if base_symbol in sp500_tickers:
            print(f"Identified {stock_symbol} as US stock")
            return 'SMART'
            
        # Default case with logging
        try:
            ticker = yf.Ticker(stock_symbol) # type: ignore
            info = ticker.info
            if 'exchange' in info:
                exchange_code = info['exchange']
                exchange_map = {
                    'NMS': 'NASDAQ',
                    'NYQ': 'NYSE'
                }
                result = exchange_map.get(exchange_code, exchange_code)
                print(f"Found exchange {result} for {stock_symbol}")
                return result
        except Exception as e:
            print(f"Error getting exchange for {stock_symbol}: {e}")
        return 'Unknown'


    def get_exchange_rate_euro_to_dollar(self, pair="EURUSD=X"):
        try:
            ticker = yf.Ticker(pair) # type: ignore
            data = ticker.history(period="1d")
            if not data.empty:
                return data["Close"].iloc[-1]
            return 1.0  # Default if fetch fails
        except Exception as e:
            print(f"Error getting exchange rate for {pair}: {e}")
            return 1.0
        




    """
        IB FUNCTIONS 
    """

    def get_available_position_with_symbol(self, symbol):
        """Retrieve available position for a given stock symbol."""
        for pos in self.ib.positions():
            if pos.contract.symbol == symbol:
                return pos
        return None


    def _execute_stop_loss_sell_order(self, symbol, contract):
        # Retrieve account info and position details
        account_info = self.get_ib_account_info()
        pos_info = account_info["positions"].get(symbol)
        if pos_info is None:
            # Try base symbol if suffixed symbol not found (e.g., "AAPL" from "AAPL.NASDAQ")
            base_symbol = symbol.split('.')[0]
            pos_info = account_info["positions"].get(base_symbol)
        if pos_info is None:
            print(f"No position found for symbol {symbol} in stop loss order")
            return
        
        # Get shares owned and market value
        shares_owned = pos_info["shares"]
        if shares_owned <= 0:
            print(f"No shares owned for {symbol}")
            return

        market_value = pos_info["market_value"]

        # Calculate current price per share
        if market_value > 0 and shares_owned > 0:
            current_price = market_value / shares_owned
        else:
            current_price = get_stock_closing_price(symbol)
            if current_price <= 0:
                print(f"Cannot determine current price for {symbol}")
                return

        # Set stop price at 85% of current price (per share)
        stop_price = current_price * 0.85
        # Quantity is the number of shares owned (whole shares)
        quantity = int(shares_owned)  # Use int() to ensure whole shares

        # Create and place the stop-loss order
        order = StopOrder('SELL', quantity, stopPrice=stop_price)
        order.transmit = True  # Explicitly ensure transmission (default is True)

        trade = self.ib.placeOrder(contract, order)
        print(f"Attempted to place stop order for {symbol}: {order}")

        # Verify transmission by checking order status
        self.ib.sleep(1)  # Wait briefly for status update
        order_status = trade.orderStatus.status
        print(f"Order status: {order_status}")
        if order_status == "Submitted" or order_status == "Filled":
            print(f"Stop order transmitted for {quantity} shares at stop price {stop_price} for stock {symbol}")
        else:
            print(f"Stop order not transmitted for {symbol}, status: {order_status}")

        

    def _execute_buy_order(self, symbol, buy_value_eur, exchange):

        if exchange in EUROPEAN_EXCHANGES and not self.european_market_is_open():
            print("EU market not open")
            return

        if exchange in US_EXCHANGES and not self.us_market_is_open():
            print("US market not open")
            return
        

        if not self.ib.isConnected():
            self.ib.connect('127.0.0.1', 7497, clientId=1)
            print("Reconnected to Interactive Brokers")

        try:
            print(f"Starting buy order for {symbol} with {buy_value_eur} EUR")
            
            # Verify symbol is in allowed lists
            if symbol.split(".")[0] not in sp500_tickers and symbol.split(".")[0] not in german_tickers:
                print(f"Symbol {symbol} not in allowed stock lists")
                return False

            # Create contract with proper exchange
            if any(symbol.endswith(ext) for ext in ['.DE', '.DU']):
                base_symbol = symbol.split('.')[0]
                contract = Stock(base_symbol, 'IBIS', 'EUR')
                needs_conversion = False
            
            else:
                if exchange in US_EXCHANGES:
                    contract = Stock(symbol, 'SMART', 'USD')
                    needs_conversion = True
                elif exchange in EUROPEAN_EXCHANGES:
                    contract = Stock(symbol, 'IBIS', 'EUR')
                    needs_conversion = False

            print(f"Created contract: {contract}")

            # add a stop loss order to the contract for 85 percent of the current value
            #self._execute_stop_loss_sell_order(symbol, contract)
            #print("Executed stop loss sell order")

            # Convert buy value if needed
            if needs_conversion:
                eur_usd_rate = self.get_exchange_rate_euro_to_dollar()
                buy_value = buy_value_eur * eur_usd_rate
                print(f"Converting {buy_value_eur} EUR to {buy_value} USD (rate: {eur_usd_rate})")
            else:
                buy_value = buy_value_eur
            
            # Qualify the contract
            qualified = self.ib.qualifyContracts(contract)
            if not qualified:
                raise ValueError(f"Failed to qualify contract for {symbol}")
            
            # Get current market price with better validation
            ticker = self.ib.reqMktData(contract, '', False, False)
            timeout = 10
            start_time = time.time()
            price = None
            
            while time.time() - start_time < timeout:
                self.ib.sleep(1)
                if ticker.last and not math.isnan(ticker.last):
                    price = ticker.last
                    break
                elif ticker.close and not math.isnan(ticker.close):
                    price = ticker.close
                    break
                    
            # If no valid price from market data, try closing price
            if price is None or price <= 0 or math.isnan(price):
                fallback_price = get_stock_closing_price(symbol) # type: ignore
                if fallback_price and fallback_price > 0 and not math.isnan(fallback_price):
                    price = fallback_price
                    print(f"Using fallback price: {price}")
                else:
                    raise ValueError(f"Could not get valid price for {symbol}")
                    
            print(f"Current price for {symbol}: {price}")
            
            # Calculate quantity with validation
            if price <= 0:
                raise ValueError(f"Invalid price {price} for {symbol}")
                
            quantity = math.floor(buy_value / price)
            if quantity <= 0:
                raise ValueError(f"Buy value {buy_value} too small for current price {price}")
            
            print(f"Attempting to buy {quantity} shares at approximately {price}")
            
            # Place and monitor order
            order = MarketOrder('BUY', quantity)
            order.transmit = True
            trade = self.ib.placeOrder(contract, order)
            print(f"Order placed: {order}")
            
            # Monitor order status
            timeout = 10
            start_time = time.time()
            while not trade.isDone() and time.time() - start_time < timeout:
                self.ib.sleep(1)
                status = trade.orderStatus.status
                filled = trade.orderStatus.filled
                print(f"Order status: {status}, filled: {filled}")
                if status in ['Filled', 'Cancelled']:
                    break
                    
            if trade.orderStatus.status == 'Filled':
                print(f"Order filled: {trade.orderStatus.filled} shares at {trade.orderStatus.avgFillPrice}")
                return True
            else:
                print(f"Order failed: {trade.orderStatus.status}")
                if trade.orderStatus.whyHeld:
                    print(f"Why held: {trade.orderStatus.whyHeld}")
                return False
                
        except Exception as e:
            print(f"Error executing trade: {e}")
            import traceback
            traceback.print_exc()
            return False


    # maybe chnage back to next
    def _execute_sell_order(self, symbol, sell_value_eur, exchange):

        if exchange in EUROPEAN_EXCHANGES and not self.european_market_is_open():
            print("EU market not open")
            return

        if exchange in US_EXCHANGES and not self.us_market_is_open():
            print("US market not open")
            return
    
        if not self.ib.isConnected():
            self.ib.connect('127.0.0.1', 7497, clientId=1)
            print("Reconnected to Interactive Brokers")

        try:
            # Create contract with proper exchange handling
            if symbol.endswith('.DE'):
                contract = Stock(symbol.replace('.DE', ''), 'IBIS', 'EUR')
                sell_value = sell_value_eur
            else:
                currency = 'USD' if exchange in US_EXCHANGES else 'EUR'
                contract = Stock(symbol, exchange, currency)
                eur_usd_rate = self.get_exchange_rate_euro_to_dollar()
                sell_value = sell_value_eur * eur_usd_rate
                

                
            print(f"Created contract: {contract}")
            
            # Qualify the contract
            qualified = self.ib.qualifyContracts(contract)
            if not qualified:
                raise ValueError(f"Failed to qualify contract for {symbol}")
            
            # Get current market price with better validation
            ticker = self.ib.reqMktData(contract, '', False, False)
            timeout = 10
            start_time = time.time()
            price = None
            
            while time.time() - start_time < timeout:
                self.ib.sleep(1)
                if ticker.last and not math.isnan(ticker.last):
                    price = ticker.last
                    break
                elif ticker.close and not math.isnan(ticker.close):
                    price = ticker.close
                    break
                    
            # If no valid price from market data, try closing price
            if price is None or price <= 0 or math.isnan(price):
                fallback_price = get_stock_closing_price(symbol) # type: ignore
                if fallback_price and fallback_price > 0 and not math.isnan(fallback_price):
                    price = fallback_price
                    print(f"Using fallback price: {price}")
                else:
                    raise ValueError(f"Could not get valid price for {symbol}")
                    
            print(f"Current price for {symbol}: {price}")
            
            # Calculate quantity with validation
            if price <= 0:
                raise ValueError(f"Invalid price {price} for {symbol}")
                
            quantity = math.floor(sell_value / price)
            if quantity <= 0:
                raise ValueError(f"Sell value {sell_value} too small for current price {price}")

            # Check available shares
            positions = self.ib.positions()
            position = self.get_available_position_with_symbol(symbol.split(".")[0])

            if not position or position.position < quantity:
                if position:
                    quantity = math.floor(position.position)  # Sell all available shares
                else:
                    raise ValueError(f"No shares of {symbol} to sell")
            
            print(f"Attempting to sell {quantity} shares at approximately {price}")
            
            # Place and monitor order
            order = MarketOrder('SELL', quantity)
            order.transmit = True
            trade = self.ib.placeOrder(contract, order)
            print(f"Order placed: {order}")
            
            # Monitor order status
            timeout = 10
            start_time = time.time()
            while not trade.isDone() and time.time() - start_time < timeout:
                self.ib.sleep(1)
                status = trade.orderStatus.status
                filled = trade.orderStatus.filled
                print(f"Order status: {status}, filled: {filled}")
                if status in ['Filled', 'Cancelled']:
                    break
                    
            if trade.orderStatus.status == 'Filled':
                print(f"Order filled: {trade.orderStatus.filled} shares at {trade.orderStatus.avgFillPrice}")
                return True
            else:
                print(f"Order failed: {trade.orderStatus.status}")
                if trade.orderStatus.whyHeld:
                    print(f"Why held: {trade.orderStatus.whyHeld}")
                return False
                
        except Exception as e:
            print(f"Error executing trade: {e}")
            traceback.print_exc()
            return False
        


    def get_ib_total_networth(self) -> dict:
        try:
            account_info = self.get_ib_account_info()
            cash_eur = float(account_info['summary']['NetLiquidation']['value'])
            positions = account_info.get('positions', {})
            total_stock_value_eur = 0.0
            eur_usd_rate = self.get_exchange_rate_euro_to_dollar()

            for symbol, info in positions.items():

                current_price = get_stock_closing_price(symbol) # type: ignore
                shares = float(info['shares'])
                
                # Convert USD values to EUR if needed
                if info.get('exchange') in US_EXCHANGES:
                    current_price_eur = current_price / eur_usd_rate
                else:
                    current_price_eur = current_price
                    
                total_stock_value_eur += shares * current_price_eur

            return float(cash_eur + total_stock_value_eur)
            
        except Exception as e:
            print(f"Error retrieving total networth: {e}")
            return 0.0



    def get_ib_cash_balance(self) -> float:
        try:
            if not self.ib.isConnected():
                self.ib.connect('127.0.0.1', 7497, clientId=1)
                
            # Get account summary
            account_values = self.ib.accountSummary()
            

            for value in account_values:
                if value.tag == 'TotalCashValue':
                    available_funds = float(value.value)
                    break
            
            print(f"Available cash balance: {available_funds} EUR")
            return float(available_funds)
            
        except Exception as e:
            print(f"Error getting cash balance: {e}")
            return 0.0
        


    def get_ib_account_info(self) -> dict:
        if self.ib is None:
            raise ValueError("IB connection is not established. Please check your connection.")
        
        # Get account summary
        account_summary = self.ib.accountSummary()
        summary_dict = {item.tag: {'value': item.value, 'currency': item.currency} 
                    for item in account_summary}
        
        # Get positions with correct attribute names
        positions = self.ib.positions()
        positions_dict = {
            pos.contract.symbol: {
                'shares': pos.position,
                'avg_cost': pos.avgCost,
                'market_price': pos.contract.lastTradingDate if hasattr(pos.contract, 'lastTradingDate') else 0.0,
                'exchange': pos.contract.exchange  # Add exchange information
            } 
            for pos in positions
        }
        
        # Calculate market value for each position using current price
        for symbol, info in positions_dict.items():
            try:
                lookup_symbol = symbol
                if info['exchange'] == 'IBIS' and not symbol.endswith('.DE'):
                    lookup_symbol = f"{symbol}.DE"
                    print(f"Using {lookup_symbol} for IBIS stock price lookup")
                
                current_price = get_stock_closing_price(lookup_symbol) # type: ignore

                positions_dict[symbol]['market_value'] = (
                    positions_dict[symbol]['shares'] * current_price
                )
            except Exception as e:
                print(f"Error calculating market value for {symbol}: {e}")
                positions_dict[symbol]['market_value'] = (
                    positions_dict[symbol]['shares'] * positions_dict[symbol]['avg_cost']
                )

        return {'summary': summary_dict, 'positions': positions_dict}



    """
    Main worker functions to handle score generation, buying and selling 
    """

    # main function that handles the score generation and the orders according to the scores
    async def main_retrieve_scores_buy_sell_worker(self):
        
        while True:
            try:
                # Fetch account info once at the start
                account_info = self.get_ib_account_info()
                available_funds = self.get_ib_cash_balance()
                total_networth = self.get_ib_total_networth()
                positions = account_info['positions']

                # Early exit if no funds and no positions
                if available_funds <= 0 and not positions:
                    print("No funds or positions available.")
                    return

                # Get stock scores 
                stock_scores = {}
                if self.us_market_is_open() or True:
                    print("Calling get_final_scores_alpha()...")
                    stock_scores_alpha = get_final_scores_alpha()  # type: ignore
                    print(f"Stock scores from alpha: {stock_scores_alpha}")
                    if stock_scores_alpha:
                        for stock, score in stock_scores_alpha.items():
                            if stock in stock_scores:
                                stock_scores[stock] = (stock_scores[stock] + score) / 2
                            else:
                                stock_scores[stock] = score

                    print("Calling get_final_scores_cnbc()...") 
                    stock_scores_cnbc = get_final_scores_web_english()  # type: ignore
                    print(f"Stock scores from cnbc: {stock_scores_cnbc}")
                    if stock_scores_cnbc:
                        for stock, score in stock_scores_cnbc.items():
                            if stock in stock_scores:
                                stock_scores[stock] = (stock_scores[stock] + score) / 2
                            else:
                                stock_scores[stock] = score

                if self.european_market_is_open() or True:
                    print("Calling get_final_scores_web_german()...")
                    stock_scores_web = get_final_scores_web_german()  # type: ignore
                    print(f"Stock scores from web: {stock_scores_web}")
                    if stock_scores_web:
                        for stock, score in stock_scores_web.items():
                            if stock in stock_scores:
                                stock_scores[stock] = (stock_scores[stock] + score) / 2
                            else:
                                stock_scores[stock] = score




                # Assign neutral scores if no scores but positions exist
                if not stock_scores and positions:
                    for stock in positions.keys():
                        stock_scores[stock] = 50
                    print("No scores returned; assigned default neutral scores of 50.")

                # generates trade term scores for all of the stocks in all of the articles
                final_trade_term_scores = get_all_trade_term_scores() # type: ignore

                # average the scores with previous scores if they exist
                if stock_scores:
                    prev_scores = load_scores_from_json("saved_scores.json")
                    if prev_scores:
                        averaged_scores = {}
                        for stock, current_score in stock_scores.items():
                            if stock in prev_scores:
                                averaged_scores[stock] = (current_score + prev_scores[stock]) / 2
                            else:
                                averaged_scores[stock] = current_score
                        stock_scores = averaged_scores
                    # Save the averaged (or original) scores back to the JSON file
                    save_scores_to_json(stock_scores, "saved_scores.json")



                #---------------------------------------------------------------------------------------
                # Process SELL orders
        
                sell_amounts = get_amount_to_sell(positions, stock_scores, final_trade_term_scores) # type: ignore

                for stock, amount in sell_amounts.items():
                    if amount > 0:
                        exchange = self.get_stock_exchange(stock)
                        self._execute_sell_order(stock, amount, exchange)

                #---------------------------------------------------------------------------------------
                # Process BUY orders - and sell stock to compensate if cash is not available for stock purchase
                buy_amounts = get_amount_to_buy(total_networth, stock_scores) # type: ignore
                total_buy_amount = sum(buy_amounts.values())

                print(f"The buy amounts are: {buy_amounts}")

                
                for stock, amount_to_buy in buy_amounts.items():

                    if stock_scores[stock] is not None:
                        if stock_scores[stock] > 50:
                            continue


                    # First ensure proper German stock formatting
                    if stock.split('.')[0] in german_tickers and not stock.endswith('.DE'):
                        stock = f"{stock}.DE"
                        print(f"Corrected German stock symbol to: {stock}")
                    
                    available_funds = self.get_ib_cash_balance()

                    # this might not be needed
                    if self.get_stock_exchange(stock) in US_EXCHANGES:
                        # Convert to EUR if needed
                        eur_usd_rate = self.get_exchange_rate_euro_to_dollar()
                        amount_to_buy = amount_to_buy / eur_usd_rate
                        print(f"Converted buy amount to EUR: {amount_to_buy}")

                    if available_funds < amount_to_buy and positions:

                        print("Trying to sell stocks to make funds available for buying.............")
                        # Calculate total needed funds
                        total_buy_amount = sum(buy_amounts.values())
                        
                        # Calculate total positions value and P/L for each position
                        positions_pl = {}
                        total_positions_value = 0
                        for stock, info in positions.items():
                            shares = info['shares']
                            avg_cost = info['avg_cost']
                            current_price = get_stock_closing_price(stock) # type: ignore
                            if current_price <= 0:
                                continue
                            position_value = shares * current_price
                            total_positions_value += position_value
                            pl_percent = (current_price - avg_cost) / avg_cost
                            positions_pl[stock] = {
                                'pl_percent': pl_percent,
                                'value': position_value,
                                'shares': shares,
                                'price': current_price
                            }

                        print("Calculated positions PL...................")



                        
                        # If we have enough value in positions plus balance to cover buys
                        if total_networth >= total_buy_amount:

                            print("Sorting positions...........")
                            # Sort positions by P/L percentage descending
                            sorted_positions = sorted(
                                positions_pl.items(),
                                key=lambda x: x[1]['pl_percent'],
                                reverse=True
                            )
                            
                            funds_needed = total_buy_amount

                            scores_from_file = load_scores_from_json("saved_scores.json")
                            if scores_from_file.get(stock, 50) > 65:
                                print(f"Stock {stock} has a score > 65, not selling to free up funds.")
                                continue

                            term_scores_from_file = load_scores_from_json("saved_trade_term_scores.json")
                            if term_scores_from_file.get(stock, 50) > 75:
                                print(f"Stock {stock} has a term score > 75, not selling to free up funds.")
                                continue

                            # Sell positions starting with highest P/L until and loops until we have enough funds through selling
                            for stock, info in sorted_positions:
                                if funds_needed <= 0:
                                    break


                                # dont sell stock just to buy it back again
                                if stock in buy_amounts.keys():
                                    buy_amounts[stock] = buy_amounts[stock] - positions_pl[stock]["value"] # buy the difference between owned and buy amount
                                    if buy_amounts[stock] <= 0:
                                        buy_amounts[stock] = 0
                                    continue

                                print("Selling positions starting at most valuable.............")
                                # Calculate how much of this position to sell
                                sell_value = min(info['value'], funds_needed)
                                exchange = self.get_stock_exchange(stock)

                                if (exchange in US_EXCHANGES and self.us_market_is_open()) or (exchange in EUROPEAN_EXCHANGES and self.european_market_is_open()):
                                
                                    # Execute sell order
                                    self._execute_sell_order(stock, sell_value, exchange)

                                    time.sleep(3)
                                    
                                    funds_needed -= sell_value

                print("--------------------------------------------------")
                print(f"The stock scores are: {stock_scores}")
                print(f"The buy amounts are: {buy_amounts}")
                print("--------------------------------------------------")

                # TODO -- maybe add safeguard here if cash balance goes below 0
                for stock, buy_value in buy_amounts.items():

                    cash_balance = self.get_ib_cash_balance()

                    if cash_balance <= 0:
                        print("No cash balance available for buying stocks.")
                        break

                    if buy_value > 0 and cash_balance >= buy_value:
                        print(f"Funds are sufficient to buy {buy_value} of {stock}")
                        # First ensure proper German stock formatting
                        if stock.split('.')[0] in german_tickers and not stock.endswith('.DE'):
                            stock = f"{stock}.DE"
                            print(f"Corrected German stock symbol to: {stock}")
                            
                        # Then get exchange after symbol correction
                        exchange = self.get_stock_exchange(stock)
                        print(f"Got exchange {exchange} for stock {stock}")
                        
                        if exchange in EUROPEAN_EXCHANGES and self.european_market_is_open():
                            self._execute_buy_order(stock, buy_value, "IBIS")
                        elif exchange in US_EXCHANGES and self.us_market_is_open():
                            self._execute_buy_order(stock, buy_value, exchange)
                        else:
                            print(f"Market not open for {stock} on exchange {exchange}")

            except Exception as e:
                print(f"Error in retrieve_scores_buy_sell_worker: {e}")
                traceback.print_exc()
            finally:
                print(f"main_retrieve_scores_buy_sell_worker done, running again in 60 minutes from {datetime.datetime.now()}...")
                await asyncio.sleep(60 * 60)  # Sleep for 60 minutes


    # sub function that makes tweaks to the current holdings based on the most recent information 
    async def sub_retrieve_scores_buy_sell_worker(self):
            
        while True:
            try:
                # Fetch account info once at the start
                account_info = self.get_ib_account_info()
                available_cash = self.get_ib_cash_balance()
                total_networth = self.get_ib_total_networth()
                positions = account_info['positions']

                # Early exit if no funds and no positions
                if available_cash <= 0 and not positions:
                    print("No funds or positions available.")
                    return

                # Get stock scores based on current news for stocks in portfolip
                stock_scores = get_final_scores_for_portfolio_stocks(positions)

                # only acknowledge the very high or low scores for tweaks
                for stock, score in stock_scores.items():
                    if 15 < score < 85:
                        score = 50

                # generates trade term scores for all of the stocks in all of the articles (averaged with saved scores)
                final_trade_term_scores = get_all_trade_term_scores() # type: ignore

                #---------------------------------------------------------------------------------------
                # Process tweaks to amount of stocks owned based off of very recent scores

                # process sell orders    
                sell_amounts = get_amount_to_sell(positions, stock_scores, final_trade_term_scores)


                # process sell orders                
                for stock, amount in sell_amounts.items():
                    if amount > 0:
                        exchange = self.get_stock_exchange(stock)
                        self._execute_sell_order(stock, amount, exchange)


                # process buy orders ---- TODO changed this to cash balance, dont want freeing up funds to take place here to prevent overselling, maybe alter
                buy_amounts = get_amount_to_buy(available_cash, stock_scores)
                total_buy_amount = sum(buy_amounts.values())


                print("--------------------------------------------------")
                print(f"The stock scores are: {stock_scores}")
                print(f"The buy amounts are: {buy_amounts}")
                print("--------------------------------------------------")

                for stock, buy_value in buy_amounts.items():

                    
                    if total_buy_amount - buy_value <= 0:
                        break

                    cash_balance = self.get_ib_cash_balance()

                    if buy_value > 0 and cash_balance >= buy_value:
                        # First ensure proper German stock formatting
                        if stock.split('.')[0] in german_tickers and not stock.endswith('.DE'):
                            stock = f"{stock}.DE"
                            print(f"Corrected German stock symbol to: {stock}")
                            
                        # Then get exchange after symbol correction
                        exchange = self.get_stock_exchange(stock)
                        print(f"Got exchange {exchange} for stock {stock}")
                        
                        if exchange in EUROPEAN_EXCHANGES and self.european_market_is_open():
                            self._execute_buy_order(stock, buy_value, "IBIS")
                        elif exchange in US_EXCHANGES and self.us_market_is_open():
                            self._execute_buy_order(stock, buy_value, exchange)
                        else:
                            print(f"Market not open for {stock} on exchange {exchange}")
                        
                        # Adjust the total buy amount
                        total_buy_amount -= buy_value
                  



            except Exception as e:
                print(f"Error in retrieve_scores_buy_sell_worker: {e}")
                traceback.print_exc()
            finally:
                print(f"sub_retrieve_scores_buy_sell_worker done, running again in 25 minutes from {datetime.datetime.now()}...") 
                await asyncio.sleep(25 * 60)  # Sleep for 25 minutes



    """Schedules both functions to run concurrently, main every hour, sub every 20min"""
    async def main(self):
        task1 = asyncio.create_task(self.sub_retrieve_scores_buy_sell_worker())  # Runs every 20 min
        task2 = asyncio.create_task(self.main_retrieve_scores_buy_sell_worker()) # Runs every 60 min
        await asyncio.gather(task1, task2)


if __name__ == "__main__":

    util.startLoop()   
    app = MinimalTradingApp()
 
    asyncio.run(app.main())
    