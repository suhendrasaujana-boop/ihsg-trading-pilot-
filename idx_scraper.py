import requests
import json
import pandas as pd
from datetime import datetime
import streamlit as st

class IDXScraper:
    """Scraper untuk mengambil data saham dari IDX"""
    
    def __init__(self):
        self.base_url = "https://www.idx.co.id"
        self.idx_api = "https://api.idx.co.id"
        
    def get_all_stocks(self):
        """Ambil semua daftar saham dari IDX"""
        
        # Method 1: Using IDX Public API
        try:
            url = "https://www.idx.co.id/primary/ListedCompany/GetStockData"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Referer': 'https://www.idx.co.id/'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = {}
                
                for item in data['data']:
                    code = item['KodeEmiten']
                    name = item['NamaEmiten']
                    stocks[f"{code}.JK"] = name
                
                return stocks
        except Exception as e:
            print(f"IDX API error: {e}")
        
        # Method 2: Backup - Static list dari database lokal
        return self.get_backup_stocks()
    
    def get_backup_stocks(self):
        """Backup data saham jika IDX API bermasalah"""
        
        # Data dari IDX (update manual via GitHub atau cache)
        # Bisa di-cache ke file JSON
        
        try:
            # Coba load dari cache
            with open('stock_cache.json', 'r') as f:
                return json.load(f)
        except:
            return self.get_static_stocks()
    
    def get_static_stocks(self):
        """Static list untuk fallback"""
        return {
            # Banking
            'BBCA.JK': 'Bank Central Asia',
            'BBRI.JK': 'Bank Rakyat Indonesia', 
            'BMRI.JK': 'Bank Mandiri',
            'BBNI.JK': 'Bank Negara Indonesia',
            'BRIS.JK': 'Bank Syariah Indonesia',
            'BNGA.JK': 'Bank CIMB Niaga',
            'ARTO.JK': 'Bank Jago',
            
            # Telco
            'TLKM.JK': 'Telkom Indonesia',
            'ISAT.JK': 'Indosat Ooredoo',
            'EXCL.JK': 'XL Axiata',
            'GOTO.JK': 'GoTo Gojek Tokopedia',
            
            # Energy
            'ADRO.JK': 'Adaro Energy',
            'BUMI.JK': 'Bumi Resources',
            'ITMG.JK': 'Indo Tambangraya',
            'PTBA.JK': 'Bukit Asam',
            'BYAN.JK': 'Bayan Resources',
            'MDKA.JK': 'Merdeka Copper Gold',
            'ANTM.JK': 'Aneka Tambang',
            'INCO.JK': 'Vale Indonesia',
            'TINS.JK': 'Timah',
            
            # Consumer
            'UNVR.JK': 'Unilever Indonesia',
            'ICBP.JK': 'Indofood CBP',
            'INDF.JK': 'Indofood Sukses',
            'MYOR.JK': 'Mayora Indah',
            'KLBF.JK': 'Kalbe Farma',
            'HMSP.JK': 'H.M. Sampoerna',
            'GGRM.JK': 'Gudang Garam',
            'CPIN.JK': 'Charoen Pokphand',
            'JPFA.JK': 'Japfa Comfeed',
            
            # Industrial
            'ASII.JK': 'Astra International',
            'AUTO.JK': 'Astra Otoparts',
            'GDYR.JK': 'Goodyear Indonesia',
            
            # Property
            'BSDE.JK': 'Bumi Serpong Damai',
            'CTRA.JK': 'Ciputra Development',
            'PWON.JK': 'Pakuwon Jati',
            'SMRA.JK': 'Summarecon Agung',
            
            # Infrastructure
            'ADHI.JK': 'Adhi Karya',
            'PTPP.JK': 'Pembangunan Perumahan',
            'WSKT.JK': 'Waskita Karya',
            'JSMR.JK': 'Jasa Marga',
            'PGAS.JK': 'Perusahaan Gas Negara',
            
            # Retail
            'ACES.JK': 'Ace Hardware',
            'ERAA.JK': 'Erajaya Swasembada',
            'AMRT.JK': 'Sumber Alfaria Trijaya',
            'LPPF.JK': 'Matahari Department Store',
            
            # Cement
            'INTP.JK': 'Indocement Tunggal',
            'SMCB.JK': 'Semen Indonesia',
        }
    
    def search_stock(self, query, stocks):
        """Search saham berdasarkan kode atau nama"""
        query_lower = query.lower()
        results = {}
        
        for code, name in stocks.items():
            if query_lower in code.lower() or query_lower in name.lower():
                results[code] = name
                
        return results
    
    def get_sector_groups(self, stocks):
        """Group saham berdasarkan sektor"""
        sectors = {
            'Perbankan': ['BBCA', 'BBRI', 'BMRI', 'BBNI', 'BRIS', 'BNGA', 'ARTO'],
            'Energi & Tambang': ['ADRO', 'BUMI', 'ITMG', 'PTBA', 'BYAN', 'MDKA', 'ANTM', 'INCO', 'TINS', 'MEDC'],
            'Konsumen': ['UNVR', 'ICBP', 'INDF', 'MYOR', 'KLBF', 'HMSP', 'GGRM', 'CPIN', 'JPFA'],
            'Telekomunikasi': ['TLKM', 'ISAT', 'EXCL', 'GOTO', 'FREN'],
            'Infrastruktur': ['ADHI', 'PTPP', 'WSKT', 'JSMR', 'PGAS', 'TOWR', 'TBIG'],
            'Properti': ['BSDE', 'CTRA', 'PWON', 'SMRA', 'LPKR', 'DILD'],
            'Ritel & Perdagangan': ['ACES', 'ERAA', 'AMRT', 'LPPF', 'MAPI'],
            'Otomotif': ['ASII', 'AUTO', 'GDYR'],
            'Semen': ['INTP', 'SMCB', 'SMBR'],
        }
        
        grouped = {}
        for sector, codes in sectors.items():
            grouped[sector] = {}
            for code in codes:
                key = f"{code}.JK"
                if key in stocks:
                    grouped[sector][key] = stocks[key]
                    
        return grouped
