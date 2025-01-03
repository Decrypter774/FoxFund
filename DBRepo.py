import psycopg2
from typing import List, Dict, Any, Optional

class StockDatabase:
    """
    A class to manage stock data in a PostgreSQL database.
    """

    def __init__(self, db_config: Dict[str, Any]):
        """
        Initializes the database connection using provided configuration.

        Args:
            db_config (Dict[str, Any]): Database connection parameters
        """
        self.db_config = db_config

    def _get_connection(self):
         """
        Establishes and returns a database connection using provided configuration.

        Returns:
           psycopg2.connection : Database connection object.
        """
         return psycopg2.connect(**self.db_config)

    def create_stock(self, stock_data: Dict[str, Any]) -> None:
        """
        Insert a new stock into the stocks table.

        Args:
            stock_data (Dict[str, Any]): A dictionary containing stock details.
        """
        query = '''
            INSERT INTO public.stocks (
                symbol, company_name, market_cap, sector, industry, beta, price,
                last_annual_dividend, volume, exchange, exchange_short_name, country,
                is_etf, is_fund, is_actively_trading, pe_ratio, industry_pe_ratio
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    stock_data['symbol'], stock_data['company_name'], stock_data['market_cap'],
                    stock_data['sector'], stock_data['industry'], stock_data['beta'],
                    stock_data['price'], stock_data['last_annual_dividend'], stock_data['volume'],
                    stock_data['exchange'], stock_data['exchange_short_name'], stock_data['country'],
                    stock_data['is_etf'], stock_data['is_fund'], stock_data['is_actively_trading'],
                    stock_data['pe_ratio'], stock_data['industry_pe_ratio']
                ))
            conn.commit()

    def get_stock_by_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a stock by its symbol.

        Args:
            symbol (str): The stock symbol.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the stock details or None if not found.
        """
        query = 'SELECT * FROM stocks WHERE symbol = %s'
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (symbol,))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            return None

    def update_stock(self, symbol: str, updates: Dict[str, Any]) -> None:
        """
        Update stock details by its symbol.

        Args:
            symbol (str): The stock symbol to update.
            updates (Dict[str, Any]): A dictionary containing the fields to update and their new values.
        """
        set_clause = ', '.join([f'{key} = %s' for key in updates.keys()])
        query = f'UPDATE stocks SET {set_clause} WHERE symbol = %s'
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (*updates.values(), symbol))
            conn.commit()

    def delete_stock(self, symbol: str) -> None:
        """
        Delete a stock from the table by its symbol.

        Args:
            symbol (str): The stock symbol to delete.
        """
        query = 'DELETE FROM stocks WHERE symbol = %s'
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (symbol,))
            conn.commit()

    def list_all_stocks(self) -> List[Dict[str, Any]]:
        """
        Retrieve all stocks from the table.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a stock.
        """
        query = 'SELECT * FROM public.stocks'
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]


# Database configuration (modify this for your specific DB setup)
DATABASE = {
    'dbname':'postgres',
    'user':'postgres',
    'password':'postgres',
    'host':'localhost',
    'port':5432
}

# Example usage
if __name__ == '__main__':
    stock_db = StockDatabase(DATABASE)

    # Delete a stock
    stock_db.delete_stock('AAPL')
    print(stock_db.list_all_stocks())
    # Create a stock entry
    stock_db.create_stock({
        'symbol': 'AAPL',
        'company_name': 'Apple Inc.',
        'market_cap': 2500000000000,
        'sector': 'Technology',
        'industry': 'Consumer Electronics',
        'beta': 1.2,
        'price': 150.5,
        'last_annual_dividend': 0.82,
        'volume': 100000,
        'exchange': 'NASDAQ',
        'exchange_short_name': 'NSDQ',
        'country': 'US',
        'is_etf': False,
        'is_fund': False,
        'is_actively_trading': True,
        'pe_ratio': 25.5,
        'industry_pe_ratio': 20.0
    })

    # Retrieve a stock
    print(stock_db.get_stock_by_symbol('AAPL'))

    # Update a stock
    stock_db.update_stock('AAPL', {'price': 155.0, 'volume': 120000})

    # List all stocks
    print(stock_db.list_all_stocks())

    # Delete a stock
    stock_db.delete_stock('AAPL')