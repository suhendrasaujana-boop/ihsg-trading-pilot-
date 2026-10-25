import requests
import pandas as pd
import streamlit as st
from io import StringIO

class IDXScraper:
    """Scraper untuk mengambil SEMUA data saham dari file CSV publik (GitHub)"""
    
    def get_all_stocks(self):
        # URL CSV yang valid dan berisi ratusan saham
        url = "https://raw.githubusercontent.com/ronnyfahrudin/Scraping_data/master/stocks_list.csv"
        
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                # Baca CSV dari response
                df = pd.read_csv(StringIO(response.text))
                
                stocks = {}
                # Loop melalui DataFrame
                for index, row in df.iterrows():
                    code = str(row['Code']).strip().upper()
                    name = str(row['CompanyName']).strip()
                    
                    # Kode saham IDX selalu 4 huruf
                    if len(code) == 4:
                        stocks[f"{code}.JK"] = name
                
                # Jika berhasil dapat lebih dari 100 saham, langsung kembalikan
                if len(stocks) > 100:
                    return stocks
        except Exception as e:
            st.error(f"Gagal mengambil data dari CSV: {e}")
        
        # Fallback jika internet mati total (daftar kecil darurat)
        return self.get_expanded_fallback_stocks()
    
    def get_expanded_fallback_stocks(self):
        """Daftar cadangan (Fallback) jika file CSV gagal diunduh"""
        return {
            'BBCA.JK': 'Bank Central Asia', 'BBRI.JK': 'Bank Rakyat Indonesia', 
            'BMRI.JK': 'Bank Mandiri', 'BBNI.JK': 'Bank Negara Indonesia',
            'TLKM.JK': 'Telkom Indonesia', 'ASII.JK': 'Astra International',
            'ADRO.JK': 'Adaro Energy', 'UNVR.JK': 'Unilever Indonesia',
            'ICBP.JK': 'Indofood CBP', 'INDF.JK': 'Indofood Sukses',
            'ANTM.JK': 'Aneka Tambang', 'GOTO.JK': 'GoTo Gojek Tokopedia'
        }
