#Calculate RSI for n periods
#----------------------------------------

#Import necessary packages
import pandas as pd
import pandas_datareader as pdr
import time
from datetime import datetime,timedelta
import urllib.request
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Get user inputs, Symbol, look back period
Symbol_type = input('Instrument type (Stock, ETF, Fx) to Analyze: ')
symbol = input('Enter symbol code: ')
go_back_period = input('Enter analysis period(5Y,1Y,1M,1Wk,1d,days): ')


#Define Analysis period based on user input
def end_date(periods):
    if periods == '5Y':
        end_period = (datetime.now() + timedelta(days=-(365*5)))        
    elif periods == '1Y':
        end_period = (datetime.now() + timedelta(days=-365))
    elif periods == '1M':
        end_period = (datetime.now() + timedelta(days=-30))
    elif periods == '1Wk':
        end_period = (datetime.now() + timedelta(days=-7))
    elif periods == '1d':
        end_period = (datetime.now() + timedelta(days=-1))
    elif periods == '':
        print('Incorrect Analysis period')
        sys.exit()
    else:
        end_period = (datetime.now() + timedelta(days=-int(periods)))


    return end_period

look_back_period = end_date(go_back_period)
#datem = datetime. datetime. strptime(date, "%Y-%m-%d %H:%M:%S")
min_date = look_back_period.date()
year = datetime.strftime(min_date,"%Y")
#year = man_date.strftime('%Y')
print(year)
#print(min_date)
#convert time periods to int pass it to data link
start = int(time.mktime(datetime.now().timetuple()))
end = int(time.mktime(look_back_period.timetuple()))

     
#Get the link based on Symbol type
def link_type(sym_type):

    if sym_type.upper() == 'FX':
        data_link = f'https://query1.finance.yahoo.com/v7/finance/download/symbol=X?period1=start_period&period2=end_period&interval=1d&events=history&includeAdjustedClose=true'    
    elif (sym_type.upper() == 'STOCK' or sym_type.upper() == 'ETF'):
        data_link = f'https://query1.finance.yahoo.com/v7/finance/download/symbol?period1=start_period&period2=end_period&interval=1d&events=history&includeAdjustedClose=true'
    else:
        print('Symbol type unknown')
        sys.exit()

    return data_link

#Get the modified link
stock_etf_link = link_type(Symbol_type)

pd.set_option('display.max_columns',None)

if stock_etf_link == '':
    sys.exit()
else:
    #Prepare Symbol data download link
    repl_symbol = stock_etf_link.replace("symbol",symbol.upper())
    repl_period_start = repl_symbol.replace("start_period",str(end))
    final_sym_link = repl_period_start.replace("end_period",str(start))

#Test URL validity
try:
    #if valid load fx data into dataframe
    sym_data = pdr.get_data_yahoo(symbol.upper(),min_date)#pd.read_csv(final_sym_link)    
except urllib.error.HTTPError as e:
    print('Incorrect Symbol Code')
    sys.exit()

#Add symbol name to data frame
sym_data.insert(loc=1,column='Symbol',value=symbol.upper())

#Calculate % Change based on previous day close
sym_data['Val_Change'] = round((sym_data['Adj Close'].diff()),2)

#Calculate positive value changes
sym_data['Val_Change_Up'] = 0.0
sym_data.loc[sym_data['Val_Change'] > 0,'Val_Change_Up'] = sym_data['Val_Change']

#Calculate negative value changes
sym_data['Val_Change_Down'] = 0.0
sym_data.loc[sym_data['Val_Change'] < 0,'Val_Change_Down'] = sym_data['Val_Change']*-1

#Average Up move
sym_data['Avg_Move_Up'] = sym_data['Val_Change_Up'].ewm(com=13, adjust=False).mean()

#Average Down move
sym_data['Avg_Move_Down'] = sym_data['Val_Change_Down'].ewm(com=13, adjust=False).mean()

#Calculate Relative Strength RS
sym_data['RS'] = sym_data['Avg_Move_Up']/sym_data['Avg_Move_Down']


#Calculate Relative Strength Index RSI
sym_data['RSI'] = 100-(100/(1+sym_data['RS']))

sym_data.dropna

print(sym_data.head())


fig, (ax1, ax2) = plt.subplots(2,1)
ax1.get_xaxis().set_visible(False)
fig.suptitle(symbol.upper())
sym_data['Close'].plot(ax=ax1)
ax1.set_ylabel('Price ($)')
sym_data['RSI'].plot(ax=ax2)

ax2.axhline(30, color='r', linestyle='--')
ax2.axhline(70, color='g', linestyle='--')
ax2.set_ylabel('RSI')
plt.show()

