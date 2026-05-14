# Konfigurasi Saham IHSG (Liquid Stocks)
IHSG_STOCKS = {
    'BBCA.JK': 'Bank Central Asia',
    'BBRI.JK': 'Bank Rakyat Indonesia', 
    'BMRI.JK': 'Bank Mandiri',
    'TLKM.JK': 'Telkom Indonesia',
    'ASII.JK': 'Astra International',
    'UNVR.JK': 'Unilever Indonesia',
    'ADRO.JK': 'Adaro Energy',
    'ICBP.JK': 'Indofood CBP'
}

# Timeframes untuk multi-timeframe analysis
TIMEFRAMES = {
    '1h': '60m',
    '4h': '4h', 
    '1d': '1d'
}

# Scoring weights
SCORING_WEIGHTS = {
    'trend': 0.35,
    'momentum': 0.30,
    'volume': 0.20,
    'volatility': 0.15
}
