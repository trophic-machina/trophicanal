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

# read file using pandas
df_orders = pd.read_excel('Fitlife\orders-2017-08-16-07-09-37.xlsx')
# prints unique order status types
#print(list(set(df_orders['Order Status'])))
df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'])

# just keep the good stuff and sort by date
df_orders = df_orders[['Order Date', 'Customer User Id', 'Order Total Amount']]
df_orders = df_orders.sort_values('Order Date')

order_list = df_orders.values
#print(order_list[1][1])
#print(order_list)

# initialize multilevel dict with earliest order

# order_list[ [time, custid, cost], [time, custid, cost], ... [time, custid, cost] ]
cohort_dict[1][order_list[0][1]] = [order_list[0][0], order_list[0][2]]
cohort = 1
for o in range(1, len(order_list)):
    current_custid = order_list[o][1]
    print("cust id: ", current_custid)
    if current_custid in cohort_dict[1]:
        print(current_custid, order_list[o][2])
        cohort_dict[cohort][current_custid].append([order_list[o][0], order_list[o][2]])
    else:
        cohort_dict[cohort][current_custid] = [ [order_list[o][0], order_list[o][2]] ]

pprint(cohort_dict)
