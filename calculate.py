import pandas as pd
pd.set_option("display.max_rows", 600)
pd.set_option("display.width", 0)

df_orders = pd.read_excel('Fitlife\orders-2017-08-16-07-09-37.xlsx')

print(list(set(df_orders['Order Status'])))
df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'])
print(df_orders.dtypes)
