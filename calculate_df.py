import pandas as pd
import numpy as np

pd.set_option("display.max_rows", 600)
pd.set_option("display.width", 0)

df_orders = pd.read_excel('Fitlife\orders-2017-08-16-07-09-37.xlsx')
# prints unique order status types
#print(list(set(df_orders['Order Status'])))
print(len(list(set(df_orders['Customer User Id']))))

"""
df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'])

# just keep the good stuff
df_orders = df_orders[['Order Date', 'Customer User Id', 'Order Total Amount']]
df_orders = df_orders.sort_values('Order Date')
df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'])
order_list = df_orders.values
print(order_list)

# sort by dates but didn't need to
#group = df_orders.sort_values('Order Date').groupby('Customer User Id')

#group = df_orders.groupby('Customer User Id')
#fod = group.agg({'Order Date': np.min})
#groups = dict(list(gb))
# Prints earliest order date for each customer
#print(dict(list(first_order_dates)))
#print(fod.index[0])
#df_fod = fod.apply(list)
#df_fod['Order Date'] = df_fod['Order Date']
#print(df_fod['Order Date'].week)
#print(df_fod['Order Date'].dt.week.tolist())
"""
