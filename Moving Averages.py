#Calculate RSI for n periods
#----------------------------------------

#Import necessary packages
import pandas as pd
import pandas_datareader as pdr
import time
from datetime import datetime,timedelta
import numpy as np
import sys
import matplotlib.pyplot as plt


#Get user inputs, Symbol, look back period
symbol = input('Enter symbol code: ')
go_back_period = input('Enter analysis period(5Y,1Y,1M,1Wk,1d,days): ')
calculate_period = input('Enter number of periods to calculate Moving Average: ')
pd.set_option('display.max_columns',None)
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

min_date = look_back_period.date()


sym_data = pdr.get_data_yahoo(symbol.upper(),min_date)#pd.read_csv(final_sym_link)


sym_data['SMA'] = sym_data['Close'].rolling(int(calculate_period)).mean()

sym_data['EMA'] = sym_data['Close'].ewm(com=int(calculate_period)).mean()

sym_data['Calc EMA'] = sym_data['EMA'].ewm(com=int(calculate_period)).mean()

sym_data['Calc EMA2'] = sym_data['Calc EMA'].ewm(com=int(calculate_period)).mean()

sym_data['DEMA'] = (2 * sym_data['EMA']) - sym_data['Calc EMA']

sym_data['Calc DEMA'] = sym_data['DEMA'].ewm(com=int(calculate_period)).mean()

sym_data['TEMA'] = (3 * sym_data['EMA']) - (3 * sym_data['Calc EMA']) + (sym_data['Calc EMA2'])

sym_data = sym_data.drop(['Calc EMA','Calc EMA2', 'Calc DEMA'],axis=1)
##sym_data.drop(['Calc EMA2'],axis=1)
##sym_data.drop(['Calc DEMA'],axis=1)


print (sym_data.tail())


