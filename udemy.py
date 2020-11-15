# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:44:45 2020

@author: pipem
"""

import pandas as pd
import datetime as dt

udemy_data = pd.read_csv("udemy_output_All_Finance__Accounting_p1_p626.csv")
#print(udemy_data)
#print(udemy_data.columns)
#print(udemy_data.info())

# for academic pourpose, we delet non-string columns whhere there are price
cols_to_delete= ["discount_price__amount","price_detail__amount","discount_price__currency","price_detail__currency"]
for col in cols_to_delete:
    del(udemy_data[col])
#print(udemy_data.info())
#print(udemy_data.columns)
#print(udemy_data.shape)
#Now we have 17 colunns  
#lets clean....

#1. As I do not the content of the data or how to replace the missing data. I am gonna drop it
udemy_data = udemy_data.dropna()
    #print(udemy_data.isna().sum()) There is no missing data, nice 

#2.lest check that each column is on the proper data type. in the case it does not i am going to 
#  change it ot the proper type.

  #the CREATE column is on the wrong data type. i am gonna pass it to date type
udemy_data["created"] = pd.to_datetime(udemy_data["created"])
assert udemy_data["created"].dtype == "datetime64[ns, UTC]"
# the PUBLISHED TIME just as up 
udemy_data["published_time"] = pd.to_datetime(udemy_data["published_time"])
assert  udemy_data["published_time"].dtype == "datetime64[ns, UTC]"

  #I deleted columns Non-strings columns so I can practice passing from STR to INT and deleteing the sing 
cols = ["discount_price__price_string","price_detail__price_string"]
for col in cols:
    udemy_data[col] = udemy_data[col].str.strip("₹")
    udemy_data[col] = udemy_data[col].str.replace(",","")
    udemy_data[col] = udemy_data[col].astype("int64")
    assert udemy_data[col].dtype == "int64"
    #we pass the indian ruppies to dollars.
    udemy_data[col] = round(udemy_data[col]/74.54,2)
    assert udemy_data[col].dtype == "float64"
    #the money columns are now on dollars and the entire dataframe columns are in the proper type.

#3. No values out of range. 

  #the "rating" column can not have values over 5.
assert udemy_data["rating"].max() <= 5
  #the data columns can not be bigger than today date.
today_date = dt.date.today()
dates_cols = ["created","published_time"]
for date in dates_cols:
    assert udemy_data[date].max() <= today_date
    
#4. Finally with the clean proccess lets check if there are duplicates and lets handle them

#  I think that the best way to check with id, name and url columns. 
unique_columns = ["id", "title","url"]
duplicates = udemy_data.duplicated(subset = unique_columns, keep = "first")
assert duplicates.sum() == 0