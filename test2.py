import yfinance as yf
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import tkcalendar as tkc
from babel.dates import format_date, parse_date, get_day_names, get_month_names
from babel.numbers import *

import sliding_window_split as sp

DJIA = ["AAPL", "MSFT", "UNH", "JNJ", "V", "WMT", "JPM", "PG", "CVX", "HD",
        "MRK", "KO", "CSCO", "MCD", "NKE", "DIS", "VZ", "AMGN", "HON", "IBM",
        "CRM", "GS", "CAT", "INTC", "AXP", "BA", "MMM", "TRV", "DD", "WBA"]
NIKKEI = ["7203.T", "6758.T", "9432.T", "8306.T", "9984.T", "9433.T", "9983.T",
          "4568.T", "8035.T", "4063.T", "6501.T", "6367.T", "8058.T", "8316.T",
          "8001.T", "4502.T", "4519.T", "8031.T", "6902.T", "8766.T", "7267.T",
          "2914.T", "3382.T", "8411.T", "6954.T", "4503.T", "6702.T", "5108.T",
          "7733.T", "9022.T"]
MIB = ["ENEL.MI", "ENI.MI", "STLA.MI", "ISP.MI", "STM.MI", "G.MI", "UCG.MI",
       "CNHI.MI", "TEN.MI", "ATL.MI", "SRG.MI", "TRN.MI", "CPR.MI", "PRY.MI",
       "REC.MI", "MB.MI", "DIA.MI", "AMP.MI", "BMED.MI", "BAMI.MI", "IP.MI",
       "LDO.MI", "TIT.MI", "A2A.MI", "HER.MI", "BGN.MI", "UNI.MI", "BZU.MI",
       "AZM.MI", "BPE.MI"]
FTSE = ["AZN.L", "SHEL.L", "ULVR.L", "HSBA.L", "RIO.L", "DGE.L", "BP.L",
        "BATS.L", "GLEN.L", "GSK.L", "REL.L", "AAL.L", "RKT.L", "LSEG.L",
        "NG.L", "CPG.L", "LLOY.L", "PRU.L", "EXPN.L", "NWG.L", "BA.L", "VOD.L",
        "BARC.L", "CRH.L", "AHT.L", "FLTR.L", "IMB.L", "SSE.L", "STAN.L", "TSCO.L"]
DAX = ["SAP.DE", "SIE.DE", "DTE.DE", "AIR.DE", "VOW3.DE", "ALV.DE", "MRK.DE", "MBG.DE",
       "BMW.DE", "BAYN.DE", "DBK.DE", "BAS.DE", "MUV2.DE", "IFX.DE", "DB1.DE", "HEN3.DE",
       "RWE.DE", "BEI.DE", "SRT3.DE", "EOAN.DE", "HNR1.DE", "ADS.DE", "DBK.DE", "PAH3.DE",
       "SY1.DE", "FRE.DE", "CON.DE", "QIA.DE", "MTX.DE", "HEI.DE"]
CAC = ["MC.PA", "OR.PA", "RMS.PA", "TTE.PA", "SAN.PA", "AIR.PA", "EL.PA", "SU.PA",
       "AI.PA", "KER.PA", "BNP.PA", "CS.PA", "DG.PA", "SAF.PA", "RI.PA", "DSY.PA",
       "STLA.PA", "ENGI.PA", "STM.PA", "BN.PA", "CAP.PA", "ACA.PA", "HO.PA", "ORA.PA",
       "SGO.PA", "LR.PA", "ML.PA", "GLE.PA", "VIE.PA", "PUB.PA"]
TSX = ["RY.TO", "TD.TO", "CNR.TO", "ENB.TO", "CP.TO", "BAM.TO", "CNQ.TO", "BMO.TO",
       "BNS.TO", "TRI.TO", "ATD.TO", "BCE.TO", "NTR.TO", "TRP.TO", "SU.TO", "CM.TO",
       "CVE.TO", "WCN.TO", "MFC.TO", "CSU.TO", "IMO.TO", "T.TO", "ABX.TO", "L.TO", "FNV.TO",
       "SLF.TO", "IFC.TO", "RCI-B.TO", "NA.TO", "AEM.TO", ]


def button_click2():
    stock_name = entry.get()
    if stock_name == "DJIA":
        stock_list = DJIA
    elif stock_name == "NIKKEI":
        stock_list = NIKKEI
    elif stock_name == "MIB":
        stock_list = MIB
    elif stock_name == "FTSE":
        stock_list = FTSE
    elif stock_name == "DAX":
        stock_list = DAX
    elif stock_name == "TSX":
        stock_list = TSX
    elif stock_name == "CAC":
        stock_list = CAC
    else:
        stock_list = stock_name.split(" ")
    begin_get = cal.get_date()
    year = begin_get.strftime("%Y")
    month = begin_get.strftime("%m")
    day = begin_get.strftime("%d")
    start_time = year + '-' + month + '-' + day

    end_get = cal_end_list.get_date()
    year_end = end_get.strftime("%Y")
    month_end = end_get.strftime("%m")
    day_end = end_get.strftime("%d")
    end_time = year_end + '-' + month_end + '-' + day_end

    stock_data, not_enough = stock_get(stock_list, start_time, end_time)

    spilt_begin = year+"/"+month
    spilt_end = year_end+"/"+month_end
    file_name = str(entry_file_name.get())+".csv"
    path_name = str(entry_file_name.get())
    ipath = "./"+file_name
    stock_data.to_csv(file_name, index=False)
    zip_path = "./"+path_name
    spilt_mode = entry_split.get()
    spath = "./"+path_name+"/"

    sp.spilt_month(spilt_begin, spilt_end, ipath, spath, spilt_mode)
    sp.zip_dir(zip_path, path_name)

    if not_enough == 1:
        messagebox.showinfo("showinfo", "數據有缺漏")


def stock_get(list1, start_time, end_time):
    df = pd.DataFrame()
    pre_length = 0
    not_enough = 0
    for i in range(len(list1)):
        data = yf.download(list1[i], start=start_time, end=end_time)
        price = data["Close"]
        length = price.shape[0]
        if i == 0:
            pre_length = length
        elif i != 0:
            if pre_length != length:
                not_enough = 1
        df = pd.concat([df, price], axis=1)
    df.columns = list1
    df = df.reset_index()
    df = df.rename(columns={"index": "Date"})
    return df, not_enough


window = tk.Tk()
window.title("Hello World!")
window.minsize(width=700, height=700)
window.resizable(width=False, height=False)

stocks = []

label = tk.Label(text="輸入股票ticker", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")
entry = tk.Entry(width=30, font=("Arial", 14, "bold"), fg="black", state=tk.NORMAL)

label.grid(row=0, column=0)
entry.grid(row=0, column=1)

years = []
for i in range(0, 20):
    years.append(str(2012 + i))

months = []
for i in range(1, 13):
    months.append(str(i))

days = []
for i in range(1, 32):
    days.append(str(i))

label2 = tk.Label(text="選擇開始時間", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")
# entry2 = tk.Entry(width=30, font=("Arial", 14, "bold"), fg="black", state=tk.NORMAL)
label_file_name = tk.Label(text="請輸入檔案名稱", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")
entry_file_name = tk.Entry(width=30, font=("Arial", 14, "bold"), fg="black", state=tk.NORMAL)

'''
box_year = ttk.Combobox(window, values=years)
box_label_year = tk.Label(text="年", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")
box_month = ttk.Combobox(window, values=months)
box_label_month = tk.Label(text="月", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")
box_day = ttk.Combobox(window, values=days)
box_label_day = tk.Label(text="日", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")

label_end = tk.Label(text="選擇結束時間", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")

box_year_end = ttk.Combobox(window, values=years)
box_label_year_end = tk.Label(text="年", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")
box_month_end = ttk.Combobox(window, values=months)
box_label_month_end = tk.Label(text="月", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")
box_day_end = ttk.Combobox(window, values=days)
box_label_day_end = tk.Label(text="日", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")
'''
button2 = tk.Button(text="抓取股價", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="red",
                    command=button_click2)
label_split = tk.Label(text="輸入想要切的滑動視窗", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")
entry_split = tk.Entry(width=30, font=("Arial", 14, "bold"), fg="black", state=tk.NORMAL)

cal_begin = tk.Label(text="輸入開始時間", font=("Times New Man", 12, "bold"), pady=5, padx=5, fg="black")
cal = tkc.DateEntry(window, width=12, background="darkblue", foreground="white", borderwidth=2)
cal_end = tk.Label(text="輸入結束時間", font=("Times New Man", 12, "bold"), padx=5, pady=5, fg="black")
cal_end_list = tkc.DateEntry(window, width=12, background="darkblue", foreground="white", borderwidth=2)

'''
label2.grid(row=1, column=0)
# entry2.grid(row=1, column=1)

box_year.grid(row=1, column=1)
box_label_year.grid(row=1, column=2)
box_month.grid(row=2, column=1)
box_label_month.grid(row=2, column=2)
box_day.grid(row=3, column=1)
box_label_day.grid(row=3, column=2)

label_end.grid(row=4, column=0)
box_year_end.grid(row=4, column=1)
box_label_year_end.grid(row=4, column=2)
box_month_end.grid(row=5, column=1)
box_label_month_end.grid(row=5, column=2)
box_day_end.grid(row=6, column=1)
box_label_day_end.grid(row=6, column=2)
'''

label_split.grid(row=7, column=0)
entry_split.grid(row=7, column=1)

label_file_name.grid(row=8, column=0)
entry_file_name.grid(row=8, column=1)

cal_begin.grid(row=9, column=0)
cal.grid(row=9, column=1)
cal_end.grid(row=10, column=0)
cal_end_list.grid(row=10, column=1)

button2.grid(row=11, column=0)

window.mainloop()

