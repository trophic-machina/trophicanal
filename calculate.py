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

def print_number_of_cohorts(cohort_dict):
    return print(' Number of Cohorts = ', len(cohort_dict))

def print_all_cohort_stats(cohort_dict):
    print_cohort_dict(cohort_dict)
    print_cohort_lengths(cohort_dict)
    print('----------------------')
    print_number_of_cohorts(cohort_dict)
    return


def build_summary_data_structure(cohort_dict):
    GROSS_MARGIN = 0.35
    
    # get week number for first table column
    for key in cohort_dict[1]:
        first_week_number = cohort_dict[1][key][0][2]
        break

    # cohort_dict indexed on 1
    # FOR NOW at least, table square, # of columns = # of cohorts = len(cohort_dict)
    summary_table_list = []
    for cohort in range(1, len(cohort_dict) + 1):
        current_cohort_dict = dict.copy(cohort_dict[cohort])
        #pprint(current_cohort_dict)
        # -> [cust][order][order info]
        #print("c = ", cohort)
        #print('current_cohort_dict = \n', current_cohort_dict, '\n')
        # need list (dict?) for customers in cohort, one entry for each column
        #number_of_customers = []
        summary_table_row = []
        for table_column in range(0, len(cohort_dict)):
            column_week_number = first_week_number + table_column
            print('column_week_number = ', column_week_number)
            number_of_customers = 0
            number_of_orders = 0
            net_revenues = 0.
            AOV = 0.
            margin_per_cust = 0.
            renewal_rate = 0.
            cummulative_renewal_rate = 0.

            for cust in current_cohort_dict:
                number_of_customers += 1

                # pull out order list from dict
                orders = current_cohort_dict[cust]
                #print('\norders = ', orders)
                """
                print('COHORT = ', cohort, 'TABLE COLUMN = ', table_column,
                      'column_week_number = ', column_week_number,
                      'number_of_customers = ', number_of_customers,
                      'number_of_orders = ', number_of_orders,
                      ' CUST = ', cust, 'len(orders) = ', len(orders))
                """
                #print(cust, current_cohort_dict[cust])
                #print(len(current_cohort_dict[cust]))
                for order in range(0, len(orders)):
                    ##print('order = ', order, 'orders[order] = ', orders[order])
                    
                    if cust == 410:
                        #print('CUSTOMER 410')
                        pass
                        
                    elif orders[order][2] == column_week_number:
                        number_of_orders += 1
                        #print(orders[order][2])
                        order_cost = orders[order][1]
                        #print(order_cost)
                        net_revenues += order_cost
                        
                    #break
                #break
            AOV = net_revenues / number_of_orders
            # Diagonal table so.... cool!
            print('table_column = ', table_column, 'cohort = ', cohort)
            if table_column == cohort - 1:
                margin_per_cust = AOV * GROSS_MARGIN
                renewal_rate = 0.
                cummulative_renewal_rate = 0.
                first_week_orders = number_of_orders
            else:
                print('table_column = ', table_column, 'cohort = ', cohort)
                print('summary_table_row[table_column) = ', summary_table_row[table_column - 1])
                #renewal_rate = number_of_orders / summary_table_row[table_column - 1][3]
                cummulative_renewal_rate = number_of_orders/first_week_orders
                #margin_per_cust =  /first_week_orders # (sum of net rev/first week orders)

            """
            #print('COHORT = ', cohort, 'TABLE COLUMN = ', table_column,
                  'number_of_customers = ', number_of_customers,
                  'number_of_orders = ', number_of_orders,
                  'net_revenues = ', net_revenues,
                  'AOV = ', AOV,
                  'margin_per_cust = ', margin_per_cust)

            """
            summary_table_cell = [cohort, table_column, number_of_customers,
                                  number_of_orders,
                                  net_revenues, AOV, margin_per_cust,
                                  renewal_rate, cummulative_renewal_rate]
            print('SUMMARY TABLE CELL = \n', summary_table_cell)
            #break
            summary_table_row.append(summary_table_cell)
            print('summary_table_row = ', summary_table_row)
        #break
        summary_table_list.append([summary_table_row])
        
"""
                # for cust order
            #week_number =
            if cohort == 1:
                if column == 0:
                    print(column)
                    pprint(current_cohort_dict[413]) #[0][2])
"""

if __name__ == '__main__':
    order_list = read_file()
    cohort_dict = build_data_structure(order_list)
    #print_all_cohort_stats(cohort_dict)
    build_summary_data_structure(cohort_dict)

