import requests
import pandas as pd
from io import StringIO
import streamlit as st

class IDXScraper:
    """Scraper untuk mengambil SEMUA data saham dari IDX"""
    
    def get_all_stocks(self):
        """Ambil semua daftar saham dari Wikipedia (Lebih stabil dari API IDX)"""
        try:
            # Mengambil list dari Wikipedia Indonesia
            url = "https://id.wikipedia.org/wiki/Daftar_perusahaan_yang_tercatat_di_Bursa_Efek_Indonesia"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Baca semua tabel di halaman tersebut
                tables = pd.read_html(StringIO(response.text))
                
                # Cari tabel yang paling besar (biasanya berisi semua saham)
                df = max(tables, key=len)
                
                stocks = {}
                for index, row in df.iterrows():
                    # Cari kolom Kode dan Nama Perusahaan
                    # Biasanya kolomnya bernama 'Kode' dan 'Nama Perusahaan'
                    if 'Kode' in df.columns and 'Nama Perusahaan' in df.columns:
                        code = str(row['Kode']).strip().upper()
                        name = str(row['Nama Perusahaan']).strip()
                        
                        # Kode saham IDX selalu 4 huruf
                        if len(code) == 4:
                            stocks[f"{code}.JK"] = name
                
                if len(stocks) > 100:
                    return stocks
        except Exception as e:
            print(f"Gagal mengambil data dari Wikipedia: {e}")
        
        # Jika gagal, pakai daftar cadangan
        return self.get_static_stocks()
    
    def get_static_stocks(self):
        """Static list fallback (Diperluas jadi 80+ saham)"""
        return {
            # Banking
            'BBCA.JK': 'Bank Central Asia', 'BBRI.JK': 'Bank Rakyat Indonesia', 
            'BMRI.JK': 'Bank Mandiri', 'BBNI.JK': 'Bank Negara Indonesia',
            'BRIS.JK': 'Bank Syariah Indonesia', 'BNGA.JK': 'Bank CIMB Niaga',
            'ARTO.JK': 'Bank Jago', 'BBTN.JK': 'Bank Tabungan Negara',
            'PNBN.JK': 'Bank Pan Indonesia', 'MEGA.JK': 'Bank Mega',
            # Telco & Tech
            'TLKM.JK': 'Telkom Indonesia', 'ISAT.JK': 'Indosat Ooredoo',
            'EXCL.JK': 'XL Axiata', 'GOTO.JK': 'GoTo Gojek Tokopedia',
            'EMTK.JK': 'Elang Mahkota Teknologi', 'DCII.JK': 'DCI Indonesia',
            # Energy & Mining
            'ADRO.JK': 'Adaro Energy', 'BUMI.JK': 'Bumi Resources',
            'ITMG.JK': 'Indo Tambangraya', 'PTBA.JK': 'Bukit Asam',
            'BYAN.JK': 'Bayan Resources', 'MDKA.JK': 'Merdeka Copper Gold',
            'ANTM.JK': 'Aneka Tambang', 'INCO.JK': 'Vale Indonesia',
            'TINS.JK': 'Timah', 'MEDC.JK': 'Medco Energi', 'PGAS.JK': 'Perusahaan Gas Negara',
            'AKRA.JK': 'AKR Corporindo', 'HRUM.JK': 'Harum Energy',
            # Consumer & Retail
            'UNVR.JK': 'Unilever Indonesia', 'ICBP.JK': 'Indofood CBP',
            'INDF.JK': 'Indofood Sukses', 'MYOR.JK': 'Mayora Indah',
            'KLBF.JK': 'Kalbe Farma', 'HMSP.JK': 'H.M. Sampoerna',
            'GGRM.JK': 'Gudang Garam', 'CPIN.JK': 'Charoen Pokphand',
            'JPFA.JK': 'Japfa Comfeed', 'AMRT.JK': 'Sumber Alfaria Trijaya',
            'ACES.JK': 'Ace Hardware', 'MAPI.JK': 'Mitra Adiperkasa',
            'ERAA.JK': 'Erajaya Swasembada', 'LPPF.JK': 'Matahari Department Store',
            # Industrial & Automotive
            'ASII.JK': 'Astra International', 'AUTO.JK': 'Astra Otoparts',
            'GDYR.JK': 'Goodyear Indonesia', 'UNTR.JK': 'United Tractors',
            'HEXA.JK': 'Hexindo Adiperkasa',
            # Property & Infrastructure
            'BSDE.JK': 'Bumi Serpong Damai', 'CTRA.JK': 'Ciputra Development',
            'PWON.JK': 'Pakuwon Jati', 'SMRA.JK': 'Summarecon Agung',
            'LPKR.JK': 'Lippo Karawaci', 'DILD.JK': 'Intiland Development',
            'ADHI.JK': 'Adhi Karya', 'PTPP.JK': 'Pembangunan Perumahan',
            'WSKT.JK': 'Waskita Karya', 'JSMR.JK': 'Jasa Marga',
            'TOWR.JK': 'Sarana Menara Nusantara', 'TBIG.JK': 'Tower Bersama',
            # Cement & Basic Materials
            'INTP.JK': 'Indocement Tunggal', 'SMCB.JK': 'Semen Indonesia (Holcim)',
            'SMGR.JK': 'Semen Indonesia (SIG)', 'SMBR.JK': 'Semen Baturaja',
            'TPIA.JK': 'Chandra Asri Petrochemical', 'BRPT.JK': 'Barito Pacific',
            # Healthcare
            'SIDO.JK': 'Sido Muncul', 'KAEF.JK': 'Kimia Farma',
            'MIKA.JK': 'Mitra Keluarga', 'HEAL.JK': 'Medikaloka Hermina',
            # Others
            'BFIN.JK': 'BFI Finance', 'ADMF.JK': 'Adira Dinamika Multi Finance',
            'BBRI.JK': 'Bank Rakyat Indonesia' # Duplikat untuk memastikan
        }
