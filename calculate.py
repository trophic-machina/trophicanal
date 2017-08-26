import pandas as pd
#import numpy as np
from datetime import date
from collections import defaultdict
from pprint import pprint

# pandas display options
pd.set_option("display.max_rows", 600)
pd.set_option("display.width", 0)

def multi_level_dict():
    return defaultdict(multi_level_dict)

def read_file():
    # read file using pandas and parse date field
    df_orders = pd.read_excel('Fitlife\orders-2017-08-16-07-09-37.xlsx')
    df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'])
    df_orders['Del Date'] = pd.to_datetime(df_orders['Del Date'])
    # prints unique order status types
    #print(list(set(df_orders['Order Status'])))
    
    # just keep the good stuff and sort by date, convert to list
    df_orders = df_orders[ ['Order Date', 'Customer User Id', 'Order Total Amount', 'Del Date'] ]
    df_orders = df_orders.sort_values('Del Date')
    
    # df_orders.values: [ [time, custid, cost, deldate], [time, custid, cost, deldate], ... ]
    return df_orders.values

def build_data_structure(order_list):
    # initialize counters and trackers
    cohort = 1
    cohort_start_date   = order_list[0][0]
    first_custid        = order_list[0][1]
    order_cost          = order_list[0][2]
    order_delivery_date = order_list[0][3]
    
    order_week_number = cohort_start_date.isocalendar()[1]
    delivery_week_number = order_delivery_date.isocalendar()[1]
    
    # Initialize dict to track cust cohort,
    # and multilevel dict with earliest order placed for main data structure.
    cust_cohort_dict = {}
    cust_cohort_dict[first_custid] = cohort
    cohort_dict = multi_level_dict()
    cohort_dict[1][ first_custid ] = [ order_week_number, order_cost, delivery_week_number ]
     
    for o in range(1, len(order_list)):
        current_order_week   = order_list[o][0].isocalendar()[1]
        current_custid       = order_list[o][1]
        current_order_cost   = order_list[o][2]
        delivery_week_number = order_list[o][3].isocalendar()[1]
        
        #print("cust id: ", current_custid)
        if current_custid in cust_cohort_dict:  #[1]:
            #print("current_custid, current_order_cost= ", current_custid, current_order_cost)
            cust_cohort = cust_cohort_dict[current_custid]
            #print("cust_cohort= ", cust_cohort)
            cohort_dict[cust_cohort][current_custid].append([current_order_week, current_order_cost, delivery_week_number ])
        else:
            # now deal with week to find cohort
            if current_order_week > order_week_number:
                order_week_number = current_order_week
                cohort = cohort + 1
            cust_cohort_dict[current_custid] = cohort
            cohort_dict[cohort][current_custid] = [ [current_order_week, current_order_cost, delivery_week_number] ]
    return cohort_dict

if __name__ == '__main__':
    order_list = read_file()
    cohort_dict = build_data_structure(order_list)
    pprint(cohort_dict)
    # six cohorts
    print(
        "Cohort 1 = ", len(cohort_dict[1]), "\n",
        "Cohort 2 = ", len(cohort_dict[2]), "\n",
        "Cohort 3 = ", len(cohort_dict[3]), "\n",
        "Cohort 4 = ", len(cohort_dict[4]), "\n",
        "Cohort 5 = ", len(cohort_dict[5]), "\n",
        "Cohort 6 = ", len(cohort_dict[6])
    )
    
