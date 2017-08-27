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
    # read file using pandas and parse date fields
    df_orders = pd.read_excel('Fitlife\orders-2017-08-16-07-09-37.xlsx')
    df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'])
    df_orders['Del Date'] = pd.to_datetime(df_orders['Del Date'])
    
    # just keep the good stuff, sort by delivery date, convert to list
    df_orders = df_orders[ ['Order Date', 'Customer User Id', 'Order Total Amount',
                            'Del Date', 'Subscription Type', 'Order Number'] ]
    
    df_orders = df_orders.loc[df_orders['Subscription Type'].str.upper() == 'WEEKLY']
    del df_orders['Subscription Type']
    
    df_orders = df_orders.sort_values('Del Date')
    
    # df_orders.values: [ [order_date, custid, cost, deldate, 'Order Number'], [order_date, custid, cost, deldate, 'Order Number'], ... ]
    return df_orders.values

def extract_record_from_order_list(o, order_list):
    return [order_list[o][0].isocalendar()[1],
            order_list[o][1],
            order_list[o][2],
            order_list[o][3].isocalendar()[1]]

def build_data_structure(order_list):
    # initialize counters and trackers
    cohort = 1

    # order_record has: [ order_week_number, current_custid, order_cost, delivery_week_number ]
    order_record = extract_record_from_order_list(0, order_list)
    delivery_week_number = order_record[3]

    # Initialize dict to track cust cohort,
    # and multilevel dict with earliest order placed for main data structure.
    cust_cohort_dict = {}
    cust_cohort_dict[order_record[1]] = cohort
    cohort_dict = multi_level_dict()
    cohort_dict[1][ order_record[1] ] = [ order_record[0], order_record[2], order_record[3] ]
    
    for o in range(1, len(order_list)):
        order_record = extract_record_from_order_list(o, order_list)
        if order_record[1] in cust_cohort_dict:
            cust_cohort = cust_cohort_dict[order_record[1]]
            cohort_dict[cust_cohort][order_record[1]].append([order_record[0], order_record[2], order_record[3] ])
        else:
            # now deal with week to find cohort
            if order_record[3] > delivery_week_number:
                delivery_week_number = order_record[3]
                cohort = cohort + 1
            cust_cohort_dict[order_record[1]] = cohort
            cohort_dict[cohort][order_record[1]] = [ [ order_record[0], order_record[2], order_record[3] ] ]
    return cohort_dict


def print_cohort_dict(cohort_dict):
    #print(cohort_dict[5][626])
    return pprint(cohort_dict)

def print_cohort_lengths(cohort_dict):
    # six cohorts
    print(
        " Cohort 1 = ", len(cohort_dict[1]), "\n",
        "Cohort 2 = ", len(cohort_dict[2]), "\n",
        "Cohort 3 = ", len(cohort_dict[3]), "\n",
        "Cohort 4 = ", len(cohort_dict[4]), "\n",
        "Cohort 5 = ", len(cohort_dict[5]), "\n",
        "Cohort 6 = ", len(cohort_dict[6])
    )
    return

def print_cohort_number(cohort_dict):
    return print(' Number of Cohorts = ', len(cohort_dict))

def print_all_cohort_stats(cohort_dict):
    print_cohort_dict(cohort_dict)
    print_cohort_lengths(cohort_dict)
    print('----------------------')
    print_cohort_number(cohort_dict)
    return

if __name__ == '__main__':
    order_list = read_file()
    cohort_dict = build_data_structure(order_list)
    print_all_cohort_stats(cohort_dict)

