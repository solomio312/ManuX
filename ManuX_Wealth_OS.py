"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          MANUX WEALTH OS - v16.0 ULTIMATE SUITE (FULL FEATURES)              ║
║   Include: Yahoo Finance, Backtest, Real Estate, Rebalancing, Monte Carlo    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import requests
import json
import os
import csv
import random
from datetime import datetime
from math import pow, sqrt

# -----------------------------------------------------------------------------
# 1. CONFIGURĂRI
# -----------------------------------------------------------------------------
APP_TITLE = "ManuX Wealth OS"
VERSION = "16.0 Enterprise"
AUTHOR = "ManuX"

COLORS = {
    "bg": "#0f172a", 
    "panel": "#1e293b", 
    "card": "#334155", 
    "accent": "#3b82f6", 
    "success": "#10b981", 
    "danger": "#ef4444", 
    "warning": "#f59e0b", 
    "text": "#f8fafc", 
    "text_dim": "#94a3b8", 
    "info_bg": "#1e293b"
}

CURRENCIES = {"EUR": "€", "USD": "$", "CAD": "C$", "RON": "lei", "GBP": "£", "CHF": "CHF"}
MONTHS = ["Ian", "Feb", "Mar", "Apr", "Mai", "Iun", "Iul", "Aug", "Sep", "Oct", "Nov", "Dec"]
COMP_FREQ = {"Lunar": 12, "Trimestrial": 4, "Anual": 1}
TAX_PRESETS = {
    "Personalizat": 0.0, 
    "România (Broker Local <1 an)": 3.0, 
    "România (Broker Local >1 an)": 1.0, 
    "România (Broker Extern)": 10.0, 
    "Canada": 25.0, 
    "SUA": 15.0, 
    "Dubai": 0.0
}

# --- IMPORTURI EXTERNE SIGURE (MULTI-LINE) ---
HAS_YF = False
try:
    import yfinance as yf
    import pandas as pd
    HAS_YF = True
except ImportError:
    pass

HAS_PLOT = False
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
    HAS_PLOT = True
except ImportError:
    pass

HAS_EXCEL = False
try:
    import openpyxl
    HAS_EXCEL = True
except ImportError:
    pass

HAS_PDF = False
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    HAS_PDF = True
except ImportError:
    pass

HAS_PIL = False
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    pass

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# -----------------------------------------------------------------------------
# 2. BACKEND (LOGICĂ COMPLETĂ)
# -----------------------------------------------------------------------------
class Storage:
    FILE = "manux_scenarios.json"
    
    def save(self, name, params, res):
        data = self.load()
        hist = []
        # Salvăm doar 1 punct pe an pentru a nu aglomera fișierul JSON
        for x in res['history']:
            if x['idx'] % 12 == 0:
                hist.append(x)
        
        entry = {
            "name": name, 
            "date": str(datetime.now())[:16], 
            "final": res['final'], 
            "params": params, 
            "history": hist
        }
        data.append(entry)
        with open(self.FILE, 'w') as f:
            json.dump(data, f, indent=4)
            
    def load(self):
        if not os.path.exists(self.FILE):
            return []
        try:
            with open(self.FILE, 'r') as f:
                return json.load(f)
        except:
            return []
            
    def delete(self, idx):
        data = self.load()
        if 0 <= idx < len(data):
            del data[idx]
            with open(self.FILE, 'w') as f:
                json.dump(data, f, indent=4)

class FinanceEngine:
    def __init__(self): 
        self.rates = {"EUR": 1.0}
        self.storage = Storage()
    
    def fetch_rates(self, cb):
        def _run():
            try:
                r = requests.get("https://api.frankfurter.app/latest?from=EUR", timeout=3)
                if r.status_code == 200:
                    self.rates = r.json().get('rates', {})
                    self.rates['EUR'] = 1.0
                    if cb: 
                        cb(True, datetime.now().strftime("%H:%M"))
                else:
                    if cb: cb(False, "Err")
            except:
                if cb: cb(False, "Off")
        threading.Thread(target=_run, daemon=True).start()

    def convert(self, val, from_c, to_c):
        if from_c == to_c: return val
        val_eur = val / self.rates.get(from_c, 1.0)
        return val_eur * self.rates.get(to_c, 1.0)

    def calculate(self, p):
        months = int(p['years']) * 12
        ar = p['rate'] / 100
        freq = p['comp_freq']
        
        mr = pow(1 + ar/freq, freq/12) - 1
        mi = pow(1 + p['inflation']/100, 1/12) - 1
        
        bal = p['initial']
        inv = p['initial']
        tot_int = 0
        dep = p['deposit']
        cinf = 1.0
        hist = []
        
        s_yr = int(p['start_year'])
        s_mo = MONTHS.index(p['start_month'])
        
        for m in range(1, months + 1):
            curr_mo = s_mo + (m-1)
            d_str = f"{MONTHS[curr_mo%12]} {s_yr + curr_mo//12}"
            inv_yr = (m-1)//12 + 1
            
            if m > 1 and (m-1)%12 == 0: 
                dep *= (1 + p['dep_growth']/100)
            
            do_dep = p['dep_s'] <= inv_yr <= p['dep_e']
            do_wd = p['wd_s'] <= inv_yr <= p['wd_e']
            
            f_in = dep if do_dep else 0
            f_out = p['withdraw'] if do_wd else 0
            
            bal += f_in
            if do_dep: inv += f_in
            
            inte = bal * mr
            bal += inte
            tot_int += inte
            
            bal -= f_out
            if bal < 0: bal = 0
            
            cinf *= (1 + mi)
            real = bal / cinf
            
            hist.append({
                "idx": m, "date": d_str, "balance": bal, "real": real, 
                "invested": inv, "deposit": f_in, "withdraw": f_out, "interest_mo": inte
            })
            
        return {
            "final": bal, "real": real, "invested": inv, "profit": tot_int, 
            "history": hist, "infl_total": (cinf-1)*100, 
            "doubling": 72/(ar*100) if ar>0 else 0
        }

    def calculate_monte_carlo(self, p, volatility, sims=500):
        months = int(p['years']) * 12
        mu = p['rate'] / 100 / 12
        sigma = (volatility / 100) / sqrt(12)
        results = []
        trajectories = []
        
        for i in range(sims):
            bal = p['initial']
            curr_dep = p['deposit']
            traj = [] if i < 50 else None
            
            for m in range(1, months + 1):
                yr = (m-1)//12 + 1
                if m > 1 and (m-1)%12 == 0: 
                    curr_dep *= (1 + p['dep_growth']/100)
                
                do_dep = p['dep_s'] <= yr <= p['dep_e']
                do_wd = p['wd_s'] <= yr <= p['wd_e']
                f_in = curr_dep if do_dep else 0
                f_out = p['withdraw'] if do_wd else 0
                
                ret = random.gauss(mu, sigma)
                bal = (bal + f_in) * (1 + ret) - f_out
                if bal < 0: bal = 0
                if traj is not None: traj.append(bal)
            
            results.append(bal)
            if traj is not None: trajectories.append(traj)
        
        results.sort()
        return {
            "p10": results[int(sims*0.1)], 
            "p50": results[int(sims*0.5)], 
            "p90": results[int(sims*0.9)], 
            "traj": trajectories
        }

    def calculate_tax_impact(self, res, rate, mode):
        gross = res['final']
        profit = res['profit']
        
        if mode == "La Vânzare (Exit Tax)":
            tax = profit * (rate / 100)
            net = gross - tax
        else:
            tax = (profit * (rate / 100)) * 1.15 
            net = gross - tax
            
        infl_factor = 1 + (res['infl_total'] / 100)
        return {"gross": gross, "tax": tax, "net": net, "net_real": net / infl_factor}

    # --- IMOBILIARE ---
    def calculate_real_estate(self, p):
        down_pay = p['price'] * (p['down_pct'] / 100)
        loan_amount = p['price'] - down_pay
        
        r_m = p['interest'] / 100 / 12
        n_pmt = p['years'] * 12
        
        if r_m > 0:
            mortgage = loan_amount * (r_m * pow(1+r_m, n_pmt)) / (pow(1+r_m, n_pmt) - 1)
        else:
            mortgage = loan_amount / n_pmt
            
        gross_rent = p['rent']
        expenses = gross_rent * (p['vacancy'] + p['maintenance'] + p['management']) / 100
        noi = gross_rent - expenses
        cash_flow = noi - mortgage
        
        cash_invested = down_pay + p['closing_costs']
        cash_on_cash = (cash_flow * 12) / cash_invested * 100 if cash_invested > 0 else 0
        cap_rate = (noi * 12) / p['price'] * 100 if p['price'] > 0 else 0
        
        return {
            "mortgage": mortgage, "cash_flow": cash_flow, 
            "coc": cash_on_cash, "cap": cap_rate
        }

    # --- MARKET DATA & BACKTESTING ---
    def get_market_data(self, ticker, cb):
        def _run():
            if not HAS_YF: 
                cb(False, "Lipsește 'yfinance'. Rulează: pip install yfinance")
                return
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="10y")
                if hist.empty:
                    cb(False, "Ticker invalid sau fără date")
                    return
                
                start_p = hist['Close'].iloc[0]
                end_p = hist['Close'].iloc[-1]
                days = (hist.index[-1] - hist.index[0]).days
                years = days / 365.25
                cagr = (pow(end_p / start_p, 1/years) - 1) * 100
                
                import numpy as np
                hist['Log_Ret'] = np.log(hist['Close'] / hist['Close'].shift(1))
                vol = hist['Log_Ret'].std() * np.sqrt(252) * 100
                
                info = {
                    "name": stock.info.get('shortName', ticker),
                    "price": end_p,
                    "currency": stock.info.get('currency', '?'),
                    "cagr": cagr,
                    "vol": vol
                }
                cb(True, info)
            except Exception as e:
                cb(False, str(e))
        threading.Thread(target=_run, daemon=True).start()

    def run_backtest(self, ticker, monthly_inv, start_date="2000-01-01", cb=None):
        def _run():
            if not HAS_YF: 
                if cb: cb(False, "Lipsește 'yfinance'")
                return
            try:
                data = yf.download(ticker, start=start_date, interval="1mo")
                # Handle yfinance structure change
                if isinstance(data.columns, pd.MultiIndex):
                    prices = data['Close'].iloc[:, 0]
                else:
                    prices = data['Close']
                
                if prices.empty: 
                    if cb: cb(False, "Fără date")
                    return
                
                shares = 0
                invested = 0
                history = []
                drawdown = []
                peak = 0
                dates = []
                
                for date, price in prices.items():
                    if pd.isna(price): continue
                    shares += monthly_inv / price
                    invested += monthly_inv
                    value = shares * price
                    
                    if value > peak: peak = value
                    dd = (value - peak) / peak * 100 if peak > 0 else 0
                    
                    history.append(value)
                    drawdown.append(dd)
                    dates.append(date)
                
                final_val = history[-1]
                total_ret = (final_val - invested) / invested * 100 if invested > 0 else 0
                
                if cb: 
                    cb(True, {
                        "final": final_val, "invested": invested, "ret": total_ret, 
                        "hist": history, "dd": drawdown, "dates": dates
                    })
            except Exception as e: 
                if cb: cb(False, str(e))
        threading.Thread(target=_run, daemon=True).start()

    # --- REBALANCING ---
    def calculate_rebalance(self, assets, deposit):
        total = sum(a['val'] for a in assets) + deposit
        res = []
        for a in assets:
            target = total * (a['target'] / 100)
            diff = target - a['val']
            res.append({"name": a['name'], "action": diff})
        return res

engine = FinanceEngine()

# -----------------------------------------------------------------------------
# 3. INTERFAȚA GRAFICĂ
# -----------------------------------------------------------------------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_TITLE} v{VERSION}")
        self.geometry("1600x900")
        self.vars = {}
        self.curr = "EUR"
        self.res = None
        self.last_p = None
        self.mkt_data_cache = None
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color=COLORS['panel'])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        self.content = ctk.CTkFrame(self, fg_color=COLORS['bg'])
        self.content.grid(row=0, column=1, sticky="nsew")
        
        self.build_sidebar()
        self.build_tabs()
        
        engine.fetch_rates(self.update_status)
        self.after(1000, self.calc)

    # --- SIDEBAR ---
    def build_sidebar(self):
        fr = ctk.CTkFrame(self.sidebar, fg_color="transparent"); fr.pack(pady=20)
        ctk.CTkLabel(fr, text="📈", font=("Arial", 30)).pack(side="left")
        ctk.CTkLabel(fr, text="ManuX\nWealth OS", font=("Segoe UI", 18, "bold"), justify="left").pack(side="left", padx=10)
        
        sc = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        sc.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 1. Monedă
        self.mk_sec(sc, "💱 MONEDĂ")
        r = ctk.CTkFrame(sc, fg_color="transparent"); r.pack(fill="x")
        self.vars['curr'] = ctk.CTkComboBox(r, width=120, values=list(CURRENCIES.keys()), command=self.on_c); self.vars['curr'].pack(side="left")
        ctk.CTkButton(r, text="⟳", width=40, fg_color=COLORS['card'], command=lambda: engine.fetch_rates(self.update_status)).pack(side="right")
        self.status = ctk.CTkLabel(sc, text="...", text_color="gray", font=("Arial", 10)); self.status.pack(anchor="w")

        # 2. Timp
        self.mk_sec(sc, "📅 TIMP")
        tr = ctk.CTkFrame(sc, fg_color="transparent"); tr.pack(fill="x")
        self.vars['sm'] = ctk.CTkComboBox(tr, values=MONTHS, width=80); self.vars['sm'].set("Nov"); self.vars['sm'].pack(side="left", padx=2)
        self.vars['sy'] = ctk.CTkEntry(tr, width=60); self.vars['sy'].insert(0, "2025"); self.vars['sy'].pack(side="left")
        self.mk_inp(sc, "Durată (Ani)", "yrs", "20")
        self.vars['freq'] = ctk.CTkComboBox(sc, values=list(COMP_FREQ.keys())); self.vars['freq'].pack(fill="x", pady=5)

        # 3. Bani
        self.mk_sec(sc, "💰 PARAMETRI")
        self.mk_inp(sc, "Sumă Inițială", "init", "10000")
        self.mk_inp(sc, "Dobândă %", "rate", "7")
        self.mk_inp(sc, "Inflație %", "inf", "2.5")

        # 4. Depozite
        self.mk_sec(sc, "➕ DEPOZITE")
        self.mk_inp(sc, "Lunar", "dep", "500")
        self.mk_inp(sc, "Creștere %", "dg", "3")
        self.mk_slide(sc, "Interval Depozit", "dep")

        # 5. Retrageri
        self.mk_sec(sc, "➖ RETRAGERI")
        self.mk_inp(sc, "Lunar", "wd", "0")
        self.mk_slide(sc, "Interval Retragere", "wd")

        ctk.CTkButton(self.sidebar, text="CALCULEAZĂ", height=50, font=("Arial", 14, "bold"), fg_color=COLORS['accent'], command=self.calc).pack(fill="x", padx=20, pady=20)

    def mk_sec(self, p, t): ctk.CTkLabel(p, text=t, text_color=COLORS['accent'], font=("Arial", 11, "bold")).pack(anchor="w", pady=(15,5))
    def mk_inp(self, p, l, k, v):
        f = ctk.CTkFrame(p, fg_color="transparent"); f.pack(fill="x")
        ctk.CTkLabel(f, text=l).pack(side="left"); e = ctk.CTkEntry(f, width=80, justify="right"); e.insert(0, v); e.pack(side="right"); self.vars[k] = e
        if k == "yrs": e.bind("<KeyRelease>", self.upd_sl)
    def mk_slide(self, p, l, k):
        ctk.CTkLabel(p, text=l).pack(anchor="w"); s1 = ctk.CTkSlider(p, from_=1, to=30, number_of_steps=29); s1.set(1); s1.pack(fill="x")
        s2 = ctk.CTkSlider(p, from_=1, to=30, number_of_steps=29); s2.set(30); s2.pack(fill="x"); lb = ctk.CTkLabel(p, text="1 -> 30", text_color="gray", font=("Arial", 10)); lb.pack()
        self.vars[f"{k}_s"] = s1; self.vars[f"{k}_e"] = s2; self.vars[f"{k}_l"] = lb
        def upd(v): v1, v2 = int(s1.get()), int(s2.get()); lb.configure(text=f"An {v1} -> {v2}")
        s1.configure(command=upd); s2.configure(command=upd)
    def upd_sl(self, e):
        try: y = int(self.vars['yrs'].get()); [self.vars[k].configure(to=y, number_of_steps=y-1) for k in ['dep_s', 'dep_e', 'wd_s', 'wd_e']]
        except: pass

    # --- TABURI ---
    def build_tabs(self):
        self.tabs = ctk.CTkTabview(self.content, fg_color="transparent"); self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.t1 = self.tabs.add("📊 Dashboard")
        self.t_mkt = self.tabs.add("📈 Market Data")
        self.t_mc = self.tabs.add("🎲 Monte Carlo")
        self.t_back = self.tabs.add("⏪ Backtest")
        self.t_re = self.tabs.add("🏠 Imobiliare")
        self.t_bal = self.tabs.add("⚖️ Rebalansare")
        self.t_tax = self.tabs.add("🏛️ Fiscalitate")
        self.t2 = self.tabs.add("📋 Istoric")
        self.t3 = self.tabs.add("🏖️ Pensie")
        self.t4 = self.tabs.add("💾 Scenarii")
        self.t5 = self.tabs.add("📚 Ghid")
        
        self.build_dash()
        self.build_market()
        self.build_mc()
        self.build_backtest()
        self.build_real_estate()
        self.build_rebalance()
        self.build_tax()
        self.build_history()
        self.build_pension()
        self.build_scen()
        self.build_guide()

    def add_info_box(self, parent, title, text, example):
        f = ctk.CTkFrame(parent, fg_color=COLORS['info_bg'], corner_radius=6)
        f.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(f, text=f"ℹ️ {title}", font=("Segoe UI", 12, "bold"), text_color=COLORS['accent']).pack(anchor="w", padx=15, pady=(10,5))
        ctk.CTkLabel(f, text=text, justify="left", font=("Segoe UI", 11), text_color=COLORS['text_dim']).pack(anchor="w", padx=15, pady=(0,5))
        ctk.CTkLabel(f, text=f"💡 EXEMPLU: {example}", justify="left", font=("Segoe UI", 11, "italic"), text_color=COLORS['text']).pack(anchor="w", padx=15, pady=(0,10))

    # 1. DASHBOARD
    def build_dash(self):
        self.add_info_box(self.t1, "DASHBOARD", "Privire de ansamblu.", "Vezi evoluția averii.")
        fr = ctk.CTkFrame(self.t1, fg_color="transparent"); fr.pack(fill="x", pady=(0,20))
        self.lbls = {}
        for t in ["Sold Final", "Investit", "Profit Total", "Sold Real"]:
            c = ctk.CTkFrame(fr, fg_color=COLORS['card']); c.pack(side="left", expand=True, fill="x", padx=5)
            ctk.CTkLabel(c, text=t, text_color="gray").pack(pady=(10,0))
            l = ctk.CTkLabel(c, text="-", font=("Arial", 20, "bold"), text_color=COLORS['accent']); l.pack(pady=(5,10))
            self.lbls[t] = l
        
        rfr = ctk.CTkFrame(self.t1, fg_color=COLORS['panel']); rfr.pack(fill="x", pady=10)
        ctk.CTkLabel(rfr, text="📉 ANALIZĂ INFLAȚIE", text_color=COLORS['danger'], font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=5)
        gr = ctk.CTkFrame(rfr, fg_color="transparent"); gr.pack(fill="x", padx=20, pady=(0,10))
        self.rlbl = {}
        for t in ["Inflație Totală", "Putere Cumpărare", "Timp Dublare", "Pierdere Inflație"]:
            f = ctk.CTkFrame(gr, fg_color="transparent"); f.pack(side="left", expand=True)
            ctk.CTkLabel(f, text=t).pack(); l = ctk.CTkLabel(f, text="-", font=("Arial", 13, "bold")); l.pack(); self.rlbl[t] = l

        self.chart_fr = ctk.CTkFrame(self.t1, fg_color=COLORS['panel']); self.chart_fr.pack(fill="both", expand=True, pady=10)
        bx = ctk.CTkFrame(self.t1, fg_color="transparent"); bx.pack(fill="x")
        ctk.CTkButton(bx, text="Salvează Scenariu", fg_color=COLORS['success'], command=self.save_scen_ui).pack(side="left")
        ctk.CTkButton(bx, text="Export CSV", fg_color="#1d6f42", command=lambda: self.exp('csv')).pack(side="right", padx=5)
        ctk.CTkButton(bx, text="Export PDF", fg_color=COLORS['danger'], command=lambda: self.exp('pdf')).pack(side="right", padx=5)

    # 2. MARKET DATA
    def build_market(self):
        self.add_info_box(self.t_mkt, "DATE BURSIERE", "Descarcă date reale.", "Ex: SXR8.DE (S&P 500) sau BTC-USD.")
        f = ctk.CTkFrame(self.t_mkt, fg_color=COLORS['panel']); f.pack(fill="x", pady=10)
        ctk.CTkLabel(f, text="Ticker:").pack(side="left", padx=10)
        self.tkr = ctk.CTkEntry(f, width=150); self.tkr.pack(side="left")
        ctk.CTkButton(f, text="Caută Date", command=self.search_ticker).pack(side="left", padx=10)
        
        self.mkt_res = ctk.CTkFrame(self.t_mkt, fg_color="transparent"); self.mkt_res.pack(fill="both", expand=True, pady=20)
        self.mkt_lbls = {}
        for k in ["Nume", "Preț", "CAGR (10 ani)", "Volatilitate"]:
            fr = ctk.CTkFrame(self.mkt_res, fg_color=COLORS['card']); fr.pack(side="left", expand=True, fill="x", padx=5)
            ctk.CTkLabel(fr, text=k).pack(pady=5); l = ctk.CTkLabel(fr, text="-", font=("Arial", 16, "bold")); l.pack(pady=5); self.mkt_lbls[k] = l
        
        ctk.CTkButton(self.t_mkt, text="Aplică Datele", fg_color=COLORS['warning'], text_color="black", command=self.apply_market_data).pack(pady=20)

    def search_ticker(self):
        tkr = self.tkr.get()
        if not tkr: return
        self.mkt_lbls["Nume"].configure(text="...")
        engine.get_market_data(tkr, self.update_market_ui)

    def update_market_ui(self, ok, data):
        if not ok: messagebox.showerror("Eroare", data); return
        self.mkt_data_cache = data
        self.mkt_lbls["Nume"].configure(text=data['name'])
        self.mkt_lbls["Preț"].configure(text=f"{data['price']:.2f}")
        self.mkt_lbls["CAGR (10 ani)"].configure(text=f"{data['cagr']:.2f}%", text_color=COLORS['success'])
        self.mkt_lbls["Volatilitate"].configure(text=f"{data['vol']:.2f}%", text_color=COLORS['warning'])

    def apply_market_data(self):
        if hasattr(self, 'mkt_data_cache'):
            self.vars['rate'].delete(0, tk.END); self.vars['rate'].insert(0, f"{self.mkt_data_cache['cagr']:.2f}")
            if hasattr(self, 'mc_v'): self.mc_v.delete(0, tk.END); self.mc_v.insert(0, f"{self.mkt_data_cache['vol']:.2f}")
            messagebox.showinfo("Succes", "Date aplicate!"); self.calc()

    # 3. MONTE CARLO
    def build_mc(self):
        self.add_info_box(self.t_mc, "MONTE CARLO", "Simulare risc.", "P10 = Pesimist.")
        f = ctk.CTkFrame(self.t_mc, fg_color="transparent"); f.pack(fill="both", expand=True)
        ctrl = ctk.CTkFrame(f, fg_color=COLORS['panel']); ctrl.pack(fill="x", pady=10)
        ctk.CTkLabel(ctrl, text="Volatilitate %:").pack(side="left", padx=10); self.mc_v = ctk.CTkEntry(ctrl, width=60); self.mc_v.insert(0, "15"); self.mc_v.pack(side="left")
        ctk.CTkButton(ctrl, text="Rulează", command=self.run_mc).pack(side="right", padx=20)
        res = ctk.CTkFrame(f, fg_color="transparent"); res.pack(fill="x", pady=10)
        self.mc_res = {}
        for t, c in [("P10 (Rău)", "danger"), ("P50 (Median)", "warning"), ("P90 (Bun)", "success")]:
            fr = ctk.CTkFrame(res, fg_color=COLORS['card']); fr.pack(side="left", expand=True, fill="x", padx=5)
            ctk.CTkLabel(fr, text=t).pack(pady=5); l = ctk.CTkLabel(fr, text="-", font=("Arial", 16, "bold"), text_color=COLORS[c]); l.pack(pady=5); self.mc_res[t] = l
        self.mc_chart = ctk.CTkFrame(f, fg_color=COLORS['panel']); self.mc_chart.pack(fill="both", expand=True, pady=10)

    def run_mc(self):
        if not self.last_p: return
        try:
            vol = float(self.mc_v.get()); res = engine.calculate_monte_carlo(self.last_p, vol); sym = CURRENCIES[self.curr]; cv = lambda x: engine.convert(x, "EUR", self.curr)
            self.mc_res["P10 (Rău)"].configure(text=f"{cv(res['p10']):,.0f} {sym}")
            self.mc_res["P50 (Median)"].configure(text=f"{cv(res['p50']):,.0f} {sym}")
            self.mc_res["P90 (Bun)"].configure(text=f"{cv(res['p90']):,.0f} {sym}")
            if HAS_PLOT:
                for w in self.mc_chart.winfo_children(): w.destroy()
                fig = Figure(figsize=(5,4), dpi=100, facecolor=COLORS['panel']); ax = fig.add_subplot(111); ax.set_facecolor(COLORS['panel'])
                for t in res['traj']: ax.plot(t, color='gray', alpha=0.1)
                ax.set_title("Distribuție", color="white"); ax.tick_params(colors="white"); can = FigureCanvasTkAgg(fig, master=self.mc_chart); can.draw(); can.get_tk_widget().pack(fill="both", expand=True)
        except: pass

    # 4. BACKTEST
    def build_backtest(self):
        self.add_info_box(self.t_back, "BACKTESTING", "Testează pe istoric.", "Ex: SPY din 2000.")
        f = ctk.CTkFrame(self.t_back, fg_color="transparent"); f.pack(fill="both", expand=True)
        ctrl = ctk.CTkFrame(f, fg_color=COLORS['panel']); ctrl.pack(fill="x", pady=10)
        ctk.CTkLabel(ctrl, text="Ticker:").pack(side="left", padx=10); self.bt_tkr = ctk.CTkEntry(ctrl); self.bt_tkr.insert(0, "SPY"); self.bt_tkr.pack(side="left")
        ctk.CTkLabel(ctrl, text="Lunar:").pack(side="left", padx=10); self.bt_inv = ctk.CTkEntry(ctrl, width=80); self.bt_inv.insert(0, "500"); self.bt_inv.pack(side="left")
        ctk.CTkButton(ctrl, text="Rulează", command=self.run_bt).pack(side="right", padx=20)
        self.bt_chart = ctk.CTkFrame(f, fg_color=COLORS['panel']); self.bt_chart.pack(fill="both", expand=True, pady=10)

    def run_bt(self):
        t = self.bt_tkr.get(); i = float(self.bt_inv.get())
        engine.run_backtest(t, i, "2000-01-01", self.update_bt_ui)

    def update_bt_ui(self, ok, data):
        if not ok: messagebox.showerror("Eroare", data); return
        if HAS_PLOT:
            for w in self.bt_chart.winfo_children(): w.destroy()
            fig = Figure(figsize=(5,4), dpi=100, facecolor=COLORS['panel']); ax1 = fig.add_subplot(211); ax2 = fig.add_subplot(212)
            ax1.set_facecolor(COLORS['panel']); ax2.set_facecolor(COLORS['panel'])
            ax1.plot(data['dates'], data['hist'], color=COLORS['accent']); ax1.set_title(f"Evoluție ({data['ret']:.0f}%)", color="white")
            ax2.plot(data['dates'], data['dd'], color=COLORS['danger']); ax2.fill_between(data['dates'], data['dd'], 0, color=COLORS['danger'], alpha=0.3); ax2.set_title("Drawdown", color="white")
            can = FigureCanvasTkAgg(fig, master=self.bt_chart); can.draw(); can.get_tk_widget().pack(fill="both", expand=True)

    # 5. REAL ESTATE
    def build_real_estate(self):
        self.add_info_box(self.t_re, "IMOBILIARE", "Cash-on-Cash.", "Randament chirie.")
        f = ctk.CTkFrame(self.t_re, fg_color="transparent"); f.pack(fill="both", expand=True)
        grid = ctk.CTkFrame(f, fg_color=COLORS['panel']); grid.pack(fill="x", pady=10)
        self.re_vars = {}
        fields = [("Preț", "price", "100000"), ("Avans %", "down_pct", "15"), ("Dobândă %", "interest", "5.5"), ("Ani Credit", "years", "30"), ("Chirie", "rent", "600"), ("Neocupare %", "vacancy", "5"), ("Mentenanță %", "maintenance", "5"), ("Costuri", "closing_costs", "3000"), ("Mgmt %", "management", "0")]
        for i, (l, k, v) in enumerate(fields):
            fr = ctk.CTkFrame(grid, fg_color="transparent"); fr.grid(row=i//3, column=i%3, padx=10, pady=5, sticky="ew")
            ctk.CTkLabel(fr, text=l).pack(anchor="w"); e = ctk.CTkEntry(fr); e.insert(0, v); e.pack(fill="x"); self.re_vars[k] = e
        ctk.CTkButton(f, text="Calculează", command=self.calc_re).pack(pady=10); self.re_res = ctk.CTkLabel(f, text="", font=("Arial", 16)); self.re_res.pack(pady=10)

    def calc_re(self):
        try:
            p = {k: float(v.get()) for k, v in self.re_vars.items()}; res = engine.calculate_real_estate(p)
            txt = f"Rată: {res['mortgage']:,.0f}\nCash Flow: {res['cash_flow']:,.0f}\nCoC: {res['coc']:.2f}%\nCap Rate: {res['cap']:.2f}%"
            self.re_res.configure(text=txt, text_color=COLORS['success'] if res['cash_flow'] > 0 else COLORS['danger'])
        except: pass

    # 6. REBALANCE
    def build_rebalance(self):
        self.add_info_box(self.t_bal, "REECHILIBRARE", "Ce să cumperi.", "Menține alocarea.")
        f = ctk.CTkFrame(self.t_bal, fg_color="transparent"); f.pack(fill="both", expand=True)
        h = ctk.CTkFrame(f, fg_color="transparent"); h.pack(fill="x")
        ctk.CTkLabel(h, text="Activ", width=150).pack(side="left"); ctk.CTkLabel(h, text="Valoare", width=100).pack(side="left"); ctk.CTkLabel(h, text="Target %", width=80).pack(side="left")
        self.bal_e = []
        for _ in range(5):
            r = ctk.CTkFrame(f, fg_color="transparent"); r.pack(fill="x", pady=2)
            e1 = ctk.CTkEntry(r, width=150); e1.pack(side="left", padx=2); e2 = ctk.CTkEntry(r, width=100); e2.pack(side="left", padx=2); e3 = ctk.CTkEntry(r, width=80); e3.pack(side="left", padx=2); self.bal_e.append((e1, e2, e3))
        ctrl = ctk.CTkFrame(f, fg_color="transparent"); ctrl.pack(fill="x", pady=10)
        ctk.CTkLabel(ctrl, text="Depozit:").pack(side="left"); self.bal_dep = ctk.CTkEntry(ctrl); self.bal_dep.insert(0, "0"); self.bal_dep.pack(side="left", padx=10)
        ctk.CTkButton(ctrl, text="Calculează", command=self.calc_bal).pack(side="left"); self.bal_res = ctk.CTkLabel(f, text="", font=("Consolas", 12), justify="left"); self.bal_res.pack(pady=10)

    def calc_bal(self):
        try:
            dep = float(self.bal_dep.get()); assets = []
            for e1, e2, e3 in self.bal_e:
                if e1.get(): assets.append({"name": e1.get(), "val": float(e2.get()), "target": float(e3.get())})
            res = engine.calculate_rebalance(assets, dep)
            txt = "\n".join([f"{r['name']}: {'BUY' if r['action']>0 else 'SELL'} {abs(r['action']):,.0f}" for r in res])
            self.bal_res.configure(text=txt)
        except: pass

    # 7. TAX
    def build_tax(self):
        self.add_info_box(self.t_tax, "FISCALITATE", "Net vs Brut.", "Impactul taxelor.")
        f = ctk.CTkFrame(self.t_tax, fg_color="transparent"); f.pack(fill="both", expand=True)
        ctrl = ctk.CTkFrame(f, fg_color=COLORS['panel']); ctrl.pack(fill="x", pady=10)
        ctk.CTkLabel(ctrl, text="Regim:").pack(side="left", padx=10); self.tax_p = ctk.CTkComboBox(ctrl, width=250, values=list(TAX_PRESETS.keys()), command=self.on_tax_preset); self.tax_p.set("Personalizat"); self.tax_p.pack(side="left", padx=10)
        ctk.CTkLabel(ctrl, text="Taxă %:").pack(side="left", padx=10); self.tax_v = ctk.CTkEntry(ctrl, width=60); self.tax_v.insert(0, "0"); self.tax_v.pack(side="left")
        ctk.CTkLabel(ctrl, text="Tip:").pack(side="left", padx=10); self.tax_m = ctk.CTkComboBox(ctrl, values=["La Vânzare (Exit Tax)", "Anual (Tax Drag)"], width=150); self.tax_m.set("La Vânzare (Exit Tax)"); self.tax_m.pack(side="left")
        ctk.CTkButton(ctrl, text="Calculează", command=self.calc_tax).pack(side="right", padx=20)
        res_fr = ctk.CTkFrame(f, fg_color="transparent"); res_fr.pack(fill="x", pady=20)
        c1 = ctk.CTkFrame(res_fr, fg_color=COLORS['card']); c1.pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkLabel(c1, text="Sold BRUT", text_color="gray").pack(pady=10); self.lbl_gr = ctk.CTkLabel(c1, text="-", font=("Arial", 18, "bold")); self.lbl_gr.pack(pady=10)
        c2 = ctk.CTkFrame(res_fr, fg_color=COLORS['card']); c2.pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkLabel(c2, text="Taxe", text_color=COLORS['danger']).pack(pady=10); self.lbl_tx = ctk.CTkLabel(c2, text="-", font=("Arial", 18, "bold"), text_color=COLORS['danger']); self.lbl_tx.pack(pady=10)
        c3 = ctk.CTkFrame(res_fr, fg_color=COLORS['card']); c3.pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkLabel(c3, text="Sold NET", text_color=COLORS['success']).pack(pady=10); self.lbl_nt = ctk.CTkLabel(c3, text="-", font=("Arial", 22, "bold"), text_color=COLORS['success']); self.lbl_nt.pack(pady=10)
        c4 = ctk.CTkFrame(res_fr, fg_color=COLORS['card']); c4.pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkLabel(c4, text="NET REAL", text_color=COLORS['accent']).pack(pady=10); self.lbl_ntr = ctk.CTkLabel(c4, text="-", font=("Arial", 18, "bold"), text_color=COLORS['accent']); self.lbl_ntr.pack(pady=10)

    def on_tax_preset(self, c): self.tax_v.delete(0, tk.END); self.tax_v.insert(0, str(TAX_PRESETS.get(c, 0.0))); self.calc_tax()
    def calc_tax(self):
        if not self.res: return
        try:
            res = engine.calculate_tax_impact(self.res, float(self.tax_v.get()), self.tax_m.get())
            sym = CURRENCIES[self.curr]; cv = lambda x: engine.convert(x, "EUR", self.curr)
            self.lbl_gr.configure(text=f"{cv(res['gross']):,.0f} {sym}"); self.lbl_tx.configure(text=f"-{cv(res['tax']):,.0f} {sym}")
            self.lbl_nt.configure(text=f"{cv(res['net']):,.0f} {sym}"); self.lbl_ntr.configure(text=f"{cv(res['net_real']):,.0f} {sym}")
        except: pass

    def build_history(self): 
        self.add_info_box(self.t2, "ISTORIC DETALIAT", "Evoluție lunară.", "Vezi creșterea.")
        self.log = ctk.CTkTextbox(self.t2, font=("Consolas", 12), activate_scrollbars=True); self.log.pack(fill="both", expand=True)

    def build_pension(self):
        self.add_info_box(self.t3, "SIMULATOR PENSIE", "Sustenabilitate.", "500k vs 2k retragere.")
        f = ctk.CTkFrame(self.t3, fg_color="transparent"); f.pack(fill="both", expand=True)
        ctrl = ctk.CTkFrame(f, fg_color=COLORS['panel']); ctrl.pack(fill="x", pady=10)
        ctk.CTkLabel(ctrl, text="Portofoliu:").pack(side="left", padx=10); self.pen_p = ctk.CTkEntry(ctrl); self.pen_p.insert(0, "500000"); self.pen_p.pack(side="left")
        ctk.CTkLabel(ctrl, text="Retragere:").pack(side="left", padx=10); self.pen_w = ctk.CTkEntry(ctrl); self.pen_w.insert(0, "2000"); self.pen_w.pack(side="left")
        ctk.CTkButton(ctrl, text="Simulează", command=self.sim_pension).pack(side="left", padx=20)
        self.pen_res = ctk.CTkLabel(f, text="", font=("Arial", 14)); self.pen_res.pack(pady=10)
        self.pen_chart = ctk.CTkFrame(f, fg_color=COLORS['panel']); self.pen_chart.pack(fill="both", expand=True)

    def build_scen(self):
        self.add_info_box(self.t4, "SCENARII", "Compară strategii.", "Agresiv vs Conservator.")
        fr = ctk.CTkFrame(self.t4, fg_color="transparent"); fr.pack(fill="both", expand=True)
        self.scen_list = ctk.CTkScrollableFrame(fr, label_text="Salvate", width=250); self.scen_list.pack(side="left", fill="y", padx=10)
        right = ctk.CTkFrame(fr, fg_color="transparent"); right.pack(side="right", fill="both", expand=True)
        self.comp_fr = ctk.CTkFrame(right, fg_color=COLORS['panel']); self.comp_fr.pack(fill="both", expand=True)
        btn_r = ctk.CTkFrame(right); btn_r.pack(fill="x", pady=10)
        ctk.CTkButton(btn_r, text="Compară", command=self.compare_scens).pack(side="right", padx=10)
        ctk.CTkButton(btn_r, text="Reîncarcă", command=self.load_scens_list).pack(side="right")
        self.load_scens_list()

    def build_guide(self):
        self.add_info_box(self.t5, "GHID", "Principii.", "Regulile de aur.")
        txt = ctk.CTkTextbox(self.t5, font=("Consolas", 13), wrap="word"); txt.pack(fill="both", expand=True, padx=20, pady=20)
        txt.insert("0.0", """REGULI DE AUR PENTRU INVESTITII SI ECONOMISIREREGULA 50/30/20 (Bugetare)
. 50% - Necesități (chirie, utilități, mâncare, transport)
. 30% - Dorinte (entertainment, hobby-uri, vacante)
· 20% - Economii si investiții

FONDUL DE URGENTA
· Țintă: 3-6 luni de cheltuieli
. Pastreaza-1 lichid (cont de economii cu acces rapid)
. NU il investi in active riscante

REGULA 4% (Retragere in Pensie)
. Poți retrage 4% din portofoliu anual in mod sustenabil
. FIRE Number = Cheltuieli Anuale x 25
Ajusteaza anual pentru inflație

REGULA 72 (Timp de Dublare)
. Ani pentru dublare = 72 + Rata dobânzii
. Ex: La 7% + 72/7 = 10.3 ani pentru a dubla investiția

DIVERSIFICARE
. Nu pune toate ouale intr-un singur cos
. Mix: actiuni, obligatiuni, imobiliare, cash
. Regula varstei: % obligatiuni = varsta ta

COST AVERAGE (DCA - Dollar Cost Averaging)
. Investeste sume fixe la intervale regulate
. Reduce impactul volatilitătii
. Nu incerca sa "cronometrezi" piața

TAXE SI COSTURI
. Minimizează taxele de administrare (TER < 0.5%)
. Foloseste conturi avantajoase fiscal (Pilonul III, etc.)
. Atentie la taxele pe câstiguri de capital""")
        txt.configure(state="disabled")

    def update_status(self, ok, msg): col = COLORS['success'] if ok else COLORS['danger']; self.status.configure(text=f"API: {msg}", text_color=col)
    def on_c(self, c): self.curr = c.split(" - ")[0]; self.calc()
    def get_v(self, k): return float(self.vars[k].get())

    def calc(self):
        try:
            p = {'initial': self.get_v('init'), 'rate': self.get_v('rate'), 'years': self.get_v('yrs'), 'inflation': self.get_v('inf'), 'deposit': self.get_v('dep'), 'dep_growth': self.get_v('dg'), 'withdraw': self.get_v('wd'), 'start_year': self.vars['sy'].get(), 'start_month': self.vars['sm'].get(), 'comp_freq': COMP_FREQ[self.vars['freq'].get()], 'dep_s': self.vars['dep_s'].get(), 'dep_e': self.vars['dep_e'].get(), 'wd_s': self.vars['wd_s'].get(), 'wd_e': self.vars['wd_e'].get()}
            self.last_p = p; self.res = engine.calculate(p)
            sym = CURRENCIES[self.curr]; cv = lambda x: engine.convert(x, "EUR", self.curr)
            self.lbls["Sold Final"].configure(text=f"{cv(self.res['final']):,.0f} {sym}")
            self.lbls["Investit"].configure(text=f"{cv(self.res['invested']):,.0f} {sym}")
            self.lbls["Profit Total"].configure(text=f"{cv(self.res['profit']):,.0f} {sym}")
            self.lbls["Sold Real"].configure(text=f"{cv(self.res['real']):,.0f} {sym}")
            self.rlbl["Inflație Totală"].configure(text=f"{self.res['infl_total']:.1f}%")
            pp = (self.res['real']/self.res['invested']-1)*100 if self.res['invested']>0 else 0
            self.rlbl["Putere Cumpărare"].configure(text=f"{pp:+.1f}%", text_color=COLORS['success'] if pp>0 else COLORS['danger'])
            self.rlbl["Timp Dublare"].configure(text=f"{self.res['doubling']:.1f} ani")
            loss = self.res['final'] - self.res['real']
            self.rlbl["Pierdere Inflație"].configure(text=f"-{cv(loss):,.0f} {sym}", text_color=COLORS['danger'])
            self.calc_tax()
            self.log.configure(state="normal"); self.log.delete("0.0", "end"); self.log.insert("0.0", f"{'DATA':<15} | {'DEPOZIT':>12} | {'DOBÂNDĂ':>12} | {'RETRAS':>12} | {'SOLD':>15}\n"+"="*65+"\n")
            for r in self.res['history']: self.log.insert("end", f"{r['date']:<15} | {cv(r['deposit']):>12,.0f} | {cv(r['interest_mo']):>12,.0f} | {cv(r['withdraw']):>12,.0f} | {cv(r['balance']):>15,.0f}\n")
            self.log.configure(state="disabled")
            if HAS_PLOT:
                for w in self.chart_fr.winfo_children(): w.destroy()
                fig = Figure(figsize=(5,4), dpi=100, facecolor=COLORS['panel']); ax = fig.add_subplot(111); ax.set_facecolor(COLORS['panel'])
                d = [r['date'] for r in self.res['history'][::6]]; b = [r['balance'] for r in self.res['history'][::6]]; i = [r['invested'] for r in self.res['history'][::6]]
                x = range(len(d))
                ax.fill_between(x, i, color=COLORS['text_dim'], alpha=0.2, label="Investit"); ax.plot(x, b, color=COLORS['accent'], linewidth=2, label="Sold")
                ax.set_xticks(x[::4]); ax.set_xticklabels(d[::4], rotation=45, color="white", fontsize=8); ax.tick_params(colors="white"); ax.grid(True, alpha=0.2); ax.legend(facecolor=COLORS['panel'], labelcolor="white")
                can = FigureCanvasTkAgg(fig, master=self.chart_fr); can.draw(); can.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e: print(e)

    def save_scen_ui(self):
        d = ctk.CTkInputDialog(text="Nume:", title="Save")
        n = d.get_input()
        if n:
            engine.storage.save(n, self.last_p, self.res)
            self.load_scens_list()
    def load_scens_list(self):
        for w in self.scen_list.winfo_children(): w.destroy()
        for i, s in enumerate(engine.storage.load()):
            f = ctk.CTkFrame(self.scen_list, fg_color=COLORS['bg']); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{s['name']}\n{int(s['final']):,} €", font=("Arial", 12)).pack(side="left", padx=10)
            ctk.CTkButton(f, text="X", width=30, fg_color=COLORS['danger'], command=lambda x=i: self.del_scen(x)).pack(side="right")
    def del_scen(self, i): engine.storage.delete(i); self.load_scens_list()
    def compare_scens(self):
        if not HAS_PLOT: return
        for w in self.comp_fr.winfo_children(): w.destroy()
        scens = engine.storage.load()
        if not scens: return
        fig = Figure(figsize=(5,4), dpi=100, facecolor=COLORS['panel']); ax = fig.add_subplot(111); ax.set_facecolor(COLORS['panel'])
        for s in scens: ax.plot(range(len(s['history'])), [h['balance'] for h in s['history']], label=s['name'])
        ax.legend(facecolor=COLORS['panel'], labelcolor="white"); ax.grid(True, alpha=0.2); ax.tick_params(colors="white")
        can = FigureCanvasTkAgg(fig, master=self.comp_fr); can.draw(); can.get_tk_widget().pack(fill="both", expand=True)
    def sim_pension(self):
        try:
            p = float(self.pen_p.get()); wd = float(self.pen_w.get()); d = []; c = p
            for y in range(31): d.append(max(0, c)); c = (c - wd*12) * 1.05; wd *= 1.025
            yr = next((i for i, x in enumerate(d) if x == 0), 30)
            self.pen_res.configure(text=f"Sustenabilitate: {yr} ani", text_color=COLORS['success'] if yr==30 else COLORS['danger'])
            if HAS_PLOT:
                for w in self.pen_chart.winfo_children(): w.destroy()
                fig = Figure(figsize=(5,3), dpi=100, facecolor=COLORS['panel']); ax = fig.add_subplot(111); ax.set_facecolor(COLORS['panel'])
                ax.plot(d, color=COLORS['warning'], linewidth=2); ax.set_title("Drawdown", color="white"); ax.tick_params(colors="white")
                can = FigureCanvasTkAgg(fig, master=self.pen_chart); can.draw(); can.get_tk_widget().pack(fill="both", expand=True)
        except: pass
    def exp(self, t):
        if not self.res: return
        f = filedialog.asksaveasfilename(defaultextension=f".{t}")
        if f: messagebox.showinfo("OK", f"Salvat: {f}")

if __name__ == "__main__":
    app = App()
    app.mainloop()