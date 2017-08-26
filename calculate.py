import pandas as pd
#import numpy as np
from datetime import date
from collections import defaultdict
from pprint import pprint

def multi_level_dict():
    return defaultdict(multi_level_dict)

cohort_dict = multi_level_dict()

# pandas options
pd.set_option("display.max_rows", 600)
pd.set_option("display.width", 0)

# read file using pandas and parse date field
df_orders = pd.read_excel('Fitlife\orders-2017-08-16-07-09-37.xlsx')
df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'])

# prints unique order status types
#print(list(set(df_orders['Order Status'])))

# just keep the good stuff and sort by date, convert to list
df_orders = df_orders[ ['Order Date', 'Customer User Id', 'Order Total Amount'] ]
df_orders = df_orders.sort_values('Order Date')
order_list = df_orders.values

# order_list[ [time, custid, cost], [time, custid, cost], ... [time, custid, cost] ]

# initialize counters and trackers
cohort = 1
cohort_start_date = order_list[0][0]
week_number = cohort_start_date.isocalendar()[1]
first_custid = order_list[0][1]
cust_cohort_dict = {}
# initialize multilevel dict with earliest order placed
cohort_dict[1][ first_custid ] = [ week_number, order_list[0][2] ]
# initialize dictionary of customer cohorts
cust_cohort_dict[first_custid] = cohort

for o in range(1, len(order_list)):
    current_custid = order_list[o][1]
    current_order_week = order_list[o][0].isocalendar()[1]
    current_order_cost = order_list[o][2]
    #print("cust id: ", current_custid)
    if current_custid in cust_cohort_dict:  #[1]:
        #print("current_custid, current_order_cost= ", current_custid, current_order_cost)
        cust_cohort = cust_cohort_dict[current_custid]
        #print("cust_cohort= ", cust_cohort)
        cohort_dict[cust_cohort][current_custid].append([current_order_week, current_order_cost ])
    else:
        # now deal with week to find cohort
        if current_order_week > week_number:
            week_number = current_order_week
            cohort = cohort + 1
        cust_cohort_dict[current_custid] = cohort
        cohort_dict[cohort][current_custid] = [ [current_order_week, current_order_cost] ]

pprint(cohort_dict)
