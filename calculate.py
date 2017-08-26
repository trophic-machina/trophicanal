import pandas as pd
import numpy as np

pd.set_option("display.max_rows", 600)
pd.set_option("display.width", 0)

df_orders = pd.read_excel('Fitlife\orders-2017-08-16-07-09-37.xlsx')

print(list(set(df_orders['Order Status'])))
df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'])
group = df_orders.sort_values('Order Date').groupby('Customer User Id')

group = df_orders.groupby('Customer User Id')

# Prints earliest order date for each customer
print(group.agg({'Order Date': np.min})
      )
