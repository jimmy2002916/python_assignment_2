-- All data is stored in TEXT format to prevent information loss during systems data exchanges.
CREATE TABLE IF NOT EXISTS financial_data (
    symbol TEXT,
    date TEXT,
    open_price TEXT,
    close_price TEXT,
    volume TEXT,
    UNIQUE(symbol, date)
);
