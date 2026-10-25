import requests
import streamlit as st

class IDXScraper:
    """Scraper untuk mengambil SEMUA data saham dari IDX"""
    
    def get_all_stocks(self):
        """Ambil semua daftar saham dari repositori GitHub (Sangat Cepat & Stabil)"""
        try:
            # URL ini berisi daftar 900+ saham BEI dalam format JSON
            url = "https://raw.githubusercontent.com/wildangunawan/Daftar-Saham-IDX/main/data/daftar_saham.json"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stocks = {}
                
                # Format JSON-nya biasanya berupa list of dict: [{"kode": "AALI", "nama": "Astra Agro Lestari"}, ...]
                if isinstance(data, list):
                    for item in data:
                        # Sesuaikan dengan key yang ada di JSON
                        code = item.get('kode') or item.get('code')
                        name = item.get('nama') or item.get('name') or "Unknown"
                        
                        if code:
                            stocks[f"{code.strip().upper()}.JK"] = name.strip()
                            
                # Jika berhasil dapat lebih dari 100 saham, kembalikan
                if len(stocks) > 100:
                    return stocks
        except Exception as e:
            print(f"Gagal mengambil data dari GitHub: {e}")
        
        # Jika internet mati total atau GitHub down, pakai daftar cadangan
        return self.get_static_stocks()
    
    def get_static_stocks(self):
        """Daftar cadangan (Fallback) jika GitHub benar-benar down"""
        return {
            'BBCA.JK': 'Bank Central Asia', 'BBRI.JK': 'Bank Rakyat Indonesia', 
            'BMRI.JK': 'Bank Mandiri', 'BBNI.JK': 'Bank Negara Indonesia',
            'TLKM.JK': 'Telkom Indonesia', 'ASII.JK': 'Astra International',
            'ADRO.JK': 'Adaro Energy', 'UNVR.JK': 'Unilever Indonesia',
            'ICBP.JK': 'Indofood CBP', 'INDF.JK': 'Indofood Sukses',
            'ANTM.JK': 'Aneka Tambang', 'GOTO.JK': 'GoTo Gojek Tokopedia'
        }
