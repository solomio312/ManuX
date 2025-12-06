"""
ManuX Wealth OS - Guide View (Ghid Investiții Complet)
"""

import customtkinter as ctk
from typing import Callable

from theme_styles import COLORS, COLORS_DARK, FONTS
from widgets import CTkCard


class GuideView(ctk.CTkScrollableFrame):
    """Ghid Investiții Complet pentru Începători"""
    
    def __init__(self, parent, back_command: Callable):
        super().__init__(parent, fg_color=COLORS["guide_purple_bg"])
        self.back_command = back_command
        self.columnconfigure(0, weight=1)
        self._create_ui()
    
    def _create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0,20))
        
        ctk.CTkButton(header, text="← Înapoi", width=100, fg_color=COLORS_DARK["card_bg"],
                      hover_color=COLORS["accent"], command=self.back_command).pack(side="left")
        ctk.CTkLabel(header, text="📚 Ghid Investiții pentru Începători", font=FONTS["header"]).pack(side="left", padx=20)
        
        # Conținut complet ghid
        guides = [
            # 1. Introducere
            ("📊", "Ce sunt ETF-urile?", 
             """Exchange-Traded Funds (ETF) sunt fonduri tranzacționate la bursă care urmăresc un indice.

Avantaje ETF-uri:
• Diversificare instantanee - un singur ETF poate conține sute de companii
• Costuri reduse - TER (Total Expense Ratio) tipic 0.07% - 0.50%/an
• Lichiditate - se cumpără/vând ca acțiunile normale
• Transparență - vezi exact ce deține fondul

ETF-uri populare pentru început:
• VWCE / VWRA - Vanguard FTSE All-World (acțiuni globale)
• IWDA - iShares MSCI World (țări dezvoltate)
• EUNL - iShares Core MSCI World EUR Hedged
• AGGH - iShares Global Aggregate Bond (obligațiuni)

Unde cumperi: Interactive Brokers, DEGIRO, XTB (fără comision)"""),
            
            # 2. Dobânda compusă
            ("💹", "Puterea Dobânzii Compuse",
             """Albert Einstein a numit-o 'a 8-a minune a lumii'.

Formula: A = P × (1 + r)^n
Unde: A = valoare finală, P = principal, r = rată, n = ani

Exemplu practic la 7% randament anual:
• 10,000€ → după 10 ani: 19,672€ (aproape dublu!)
• 10,000€ → după 20 ani: 38,697€
• 10,000€ → după 30 ani: 76,123€

Regula 72: Împarte 72 la rata dobânzii pentru a afla în câți ani se dublează banii.
• 7% randament: 72 / 7 = ~10 ani pentru dublare
• 10% randament: 72 / 10 = ~7 ani pentru dublare

Concluzie: TIMPUL este cel mai important factor. Începe ACUM!"""),
            
            # 3. DCA
            ("📉", "Dollar-Cost Averaging (DCA)",
             """DCA = Investiții regulate, indiferent de prețul pieței.

Cum funcționează:
• Investești o sumă fixă lunar (ex: 500€)
• Când piața e sus, cumperi mai puține unități
• Când piața e jos, cumperi mai multe unități
• Media costului de achiziție se netezește în timp

Avantaje DCA:
✓ Elimină stresul de a "ghici" momentul potrivit
✓ Reduce impactul volatilității
✓ Creează disciplină de investiție
✓ Funcționează automat (standing order)

Studii arată: DCA bate "lump sum" în 33% din cazuri, 
dar în 67% din cazuri e mai bine să investești tot acum.
Totuși, DCA e MULT mai bun decât să nu investești deloc!"""),
            
            # 4. Diversificare
            ("🎯", "Diversificare și Alocarea Activelor",
             """"Nu pune toate ouăle în același coș" - Proverb investițional

Tipuri de diversificare:
• Geografică: SUA, Europa, Asia, Emerging Markets
• Sectorială: Tech, Healthcare, Energy, Finance, etc.
• Asset class: Acțiuni, Obligațiuni, Imobiliare, Aur

Alocări clasice:
• Agresiv (tânăr, 20-30 ani): 90% acțiuni / 10% obligațiuni
• Moderat (30-50 ani): 70% acțiuni / 30% obligațiuni
• Conservator (aproape de pensie): 50% acțiuni / 50% obligațiuni

Regula "110 - vârsta ta":
Procentul în acțiuni = 110 - vârsta ta
• 30 ani: 80% acțiuni
• 50 ani: 60% acțiuni
• 60 ani: 50% acțiuni"""),
            
            # 5. FIRE
            ("🔥", "Mișcarea FIRE",
             """FIRE = Financial Independence, Retire Early

Variante FIRE:
• Fat FIRE: Stil de viață luxos la pensie (necesită portofoliu mare)
• Lean FIRE: Viață frugală, cheltuieli minime
• Barista FIRE: Semi-pensionare, job part-time pentru asigurare
• Coast FIRE: Oprești investițiile, lași compunerea să lucreze

Regula 4% (Trinity Study):
• Portofoliu necesar = Cheltuieli anuale × 25
• Exemplu: 24,000€/an → necesari 600,000€

Pași către FIRE:
1. Calculează rata de economisire (savings rate)
2. Reduce cheltuielile inutile
3. Mărește venitul (side hustle, promovare)
4. Investește diferența în ETF-uri diversificate
5. Așteaptă și lasă compunerea să lucreze"""),
            
            # 6. Riscuri
            ("⚠️", "Gestionarea Riscurilor",
             """Tipuri de risc în investiții:

• Risc de piață: Piețele pot scădea 30-50% în criză
  → Soluție: Orizont lung (10+ ani), diversificare

• Risc de inflație: Banii în cont pierd putere de cumpărare
  → Soluție: Investește, nu ține cash

• Risc de lichiditate: Nu poți vinde rapid
  → Soluție: ETF-uri lichide, păstrează fond de urgență

• Risc valutar: Fluctuații EUR/USD
  → Soluție: Diversificare geografică

Fond de Urgență:
✓ 3-6 luni de cheltuieli în cont curent/depozit
✓ ÎNAINTE de a începe să investești
✓ Pentru situații neprevăzute (pierdere job, urgențe medicale)"""),
            
            # 7. Greșeli comune
            ("❌", "Greșeli Comune de Evitat",
             """1. Timing-ul pieței
   ❌ "Aștept să scadă piața"
   ✓ "Time in the market beats timing the market"

2. Panică în criză
   ❌ Vânzare când piața scade 20%
   ✓ Oportunitate de cumpărare la reducere

3. Urmărirea randamentelor trecute
   ❌ "Acest fond a avut 40% anul trecut"
   ✓ Performance-ul trecut nu garantează viitorul

4. Supradiversificare
   ❌ 15 ETF-uri diferite (overlap mare)
   ✓ 1-3 ETF-uri globale sunt suficiente

5. Ignorarea costurilor
   ❌ Fonduri active cu 2% TER
   ✓ ETF-uri pasive cu 0.1-0.3% TER

6. Trading frecvent
   ❌ Cumpără/vinde săptămânal
   ✓ Buy and hold pe termen lung"""),
            
            # 8. Instrumente
            ("🛠️", "Instrumente și Brokeri",
             """Brokeri recomandați pentru România:

Interactive Brokers (IBKR)
• Pro: Cel mai serios, acces global, costuri mici
• Contra: Interfață complexă

XTB
• Pro: Fără comisioane ETF-uri, interfață simplă
• Contra: Spread-uri mai mari

DEGIRO
• Pro: Costuri mici, ușor de folosit
• Contra: Nu suportă EUR hedged în RO

Trading 212
• Pro: Fără comisioane, fractional shares
• Contra: Companie mai nouă

Aplicații utile:
• JustETF.com - Căutare și comparare ETF-uri
• Portfolio Performance - Tracking gratuit
• Finviz.com - Screener acțiuni
• TradingView - Grafice tehnice"""),
            
            # 9. Psihologie
            ("🧠", "Psihologia Investitorului",
             """Biasuri cognitive care îți sabotează investițiile:

Loss Aversion (Aversiunea la pierdere)
• Durerea pierderii e 2x mai puternică decât bucuria câștigului
• Soluție: Automatizează investițiile, nu te uita la portofoliu zilnic

Confirmation Bias
• Cauți doar informații care îți confirmă opinia
• Soluție: Citește opinii contrare, fii obiectiv

Recency Bias
• Crezi că trendurile recente vor continua
• Soluție: Privește date pe 10-20+ ani

Herd Mentality (Efectul de turmă)
• Cumperi când toți cumpără (la vârf)
• Vinzi când toți vând (la minim)
• Soluție: Stick to the plan, ignoră zgomotul

Sfat de aur: Scrie-ți strategia pe hârtie ÎNAINTE de criză.
Când piața scade 30%, citește-o și respectă planul."""),
            
            # 10. Plan de acțiune
            ("🚀", "Planul Tău de Acțiune",
             """Pași concreți pentru a începe ACUM:

Săptămâna 1:
□ Deschide cont la un broker (IBKR/XTB)
□ Constituie fond de urgență (3-6 luni cheltuieli)
□ Calculează cât poți investi lunar

Săptămâna 2:
□ Alege 1-2 ETF-uri (ex: VWCE + AGGH)
□ Setează transfer automat lunar
□ Fă prima investiție (oricât de mică!)

Lunar (ongoing):
□ Investiție automată (DCA)
□ NU verifica portofoliul zilnic
□ Rebalansare anuală dacă e cazul

Anual:
□ Review strategie
□ Verifică alocare
□ Ajustează suma lunară dacă crește venitul

Reminder: Cel mai bun moment să începi era acum 10 ani.
Al doilea cel mai bun moment este ASTĂZI!"""),
        ]
        
        for i, (icon, title, content) in enumerate(guides):
            card = CTkCard(self, fg_color=COLORS["guide_purple_card"])
            card.grid(row=i+1, column=0, sticky="ew", pady=8, padx=10)
            
            ctk.CTkLabel(card, text=f"{icon} {title}", font=FONTS["subheader"]).pack(
                padx=20, pady=(20,10), anchor="w"
            )
            ctk.CTkLabel(
                card, text=content, font=FONTS["body"],
                text_color=COLORS_DARK["text_secondary"], 
                wraplength=650, justify="left"
            ).pack(padx=20, pady=(0,20), anchor="w")
        
        # Footer
        footer = ctk.CTkLabel(
            self, 
            text="⚠️ Acest ghid este doar pentru informare. Nu constituie sfat financiar. "
                 "Consultă un specialist înainte de a lua decizii de investiție.",
            font=FONTS["caption"], text_color=COLORS["warning"], wraplength=700
        )
        footer.grid(row=len(guides)+1, column=0, pady=20)
