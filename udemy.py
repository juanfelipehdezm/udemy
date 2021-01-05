# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:44:45 2020

@author: pipem
"""

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

udemy_data = pd.read_csv("udemy_output_All_Finance__Accounting_p1_p626.csv")
#print(udemy_data)
#print(udemy_data.columns)
#print(udemy_data.info())

# for academic pourpose, I deleted non-string columns where there are price
cols_to_delete= ["discount_price__amount","price_detail__amount","discount_price__currency","price_detail__currency"]
for col in cols_to_delete:
    del(udemy_data[col])
#print(udemy_data.info())
#print(udemy_data.columns)
#print(udemy_data.shape)
#Now we have 17 colunns  
#lets clean....
""" -----------------------CLEAN PROCCESS ---------------------------------------------------"""
#1. As I do not the content of the data or how to replace the missing data. I am gonna drop it
udemy_data = udemy_data.dropna()
    #print(udemy_data.isna().sum()) There is no missing data, nice 

#2. lest check that each column is on the proper data type. in the case it does not i am going to 
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

""" ------------------------------QUESTIONS TO ANSWER --------------------------------------------"""
udemy_data.set_index("published_time", inplace = True)
udemy_data["final_price"] = udemy_data["price_detail__price_string"]-udemy_data["discount_price__price_string"]

#for analysis I wont take un count courses with rate of 0. this only indicates
#that the course is quite new but no one has taken the course. 
#I also will drop columns that I wont use.

udemy_courses = udemy_data.query("rating > 0")
colsToDelete = ["avg_rating","avg_rating_recent","created"]
for cols in colsToDelete:
    del(udemy_courses[cols])

#Basic statistic measures for numerical cols
"""
#mean, median,std
for col in udemy_courses.columns[1:]:
    if udemy_courses[col].dtype == "int64" or udemy_courses[col].dtype == "float64":
        print(col.upper(),"--","mean:",round(udemy_courses[col].mean(),2),"std:",round(udemy_courses[col].std(),2),
              "median:",round(udemy_courses[col].median(),2))

---------- RESULTS-------- FOR EACH NUMERICAL COLUMN---------------------------

NUM_SUBSCRIBERS -- mean: 2994.56 std: 9663.59 median: 661.5
RATING -- mean: 4.11 std: 0.53 median: 4.2
NUM_REVIEWS -- mean: 259.35 std: 1677.97 median: 27.0
NUM_PUBLISHED_LECTURES -- mean: 33.58 std: 43.78 median: 22.0
NUM_PUBLISHED_PRACTICE_TESTS -- mean: 0.11 std: 0.6 median: 0.0
DISCOUNT_PRICE__PRICE_STRING -- mean: 6.62 std: 3.61 median: 6.1
PRICE_DETAIL__PRICE_STRING -- mean: 62.82 std: 40.65 median: 47.22
FINAL_PRICE -- mean: 56.2 std: 40.32 median: 41.12 """

sns.set_style("whitegrid")  #lets set the style for the visualizations.

#I think that to avoid some bias its better to take in count courses with more than 50 subs.
most_rated_course = udemy_courses.sort_values("rating",ascending=False)
most_rated_course = most_rated_course.query("num_subscribers > 50")

#group_rate_price = most_rated_course.groupby("rating")["final_price"].agg([np.mean,np.max,np.min,np.median]).sort_values("rating",ascending=False)
#DEFINIR UN RANGO EJE = 5-4,5  BUEN CURSO , ETC ....
#print(group_rate_price.head())

#Aswe have too many rating opcions I am gonna group que ratings ej : 0-1 = 1
#1-1.5 = 1.5, 1.5-2 = 2, 2-3 = 3, 3-4 = 4, 4-4.5 = 4.5, 4.5-5 = 5

#0-1 = 1
r1 = most_rated_course[np.logical_and(most_rated_course["rating"]>=1,most_rated_course["rating"]<=1)]
#print(r1["rating"].unique)
#As we con see , the 0-1 category is equal to 1 so lets move to the other one

def grouping(num):
    """
    
group the numbers depending on where they belong
    Parameters
    ----------
    num : float or int <= 5
         number to group
    Returns
    -------
    If the number is in between some range. the function return certain number

    """
    if num > 1 and num <= 1.5:
        return 1.5
    elif num > 1.5 and num <= 2:
        return 2
    elif num > 2 and num <= 2.5:
        return 2.5
    elif num > 2.5 and num <=3:
        return 3
    elif num > 3 and num <=3.5:
        return 3.5
    elif num > 3.5 and num <=4:
        return 4
    elif num > 4 and num <=4.5:
        return 4.5
    else:
        return 5
#print(grouping(4))
most_rated_course["rating"] = most_rated_course["rating"].apply(grouping)
#print(most_rated_course["rating"].unique)  NICEEEE

#The next step is pass to a new cvs and in jupyter notebook name some visualizations

