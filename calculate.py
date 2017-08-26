import pandas as pd
import numpy as np

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
print(order_list)

