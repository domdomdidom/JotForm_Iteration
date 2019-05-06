import os
from numpy import *
import numpy as np
from astropy.io import ascii
import datetime
import pandas as pd
from astropy.table import Table
############################################
directory = '/Users/domvandendries/Desktop/'
############################################

custy_table = ascii.read(directory+'custy_export.csv',
                        header_start=0,
                        data_start=1)

ID = custy_table['Customer ID']

customer_group = custy_table['Customer Group']

affiliation = custy_table['Your Affiliation']

email = custy_table['Email']


df = pd.DataFrame({'ID' : ID,
                  'customer_group' : customer_group,
                  'affiliation' : affiliation,
                  'email' : email})

##################################


order_table = ascii.read(directory+'orders_2016-july18.csv')

ID_2 = order_table['Customer ID']

order_date = order_table['Order Date']
order_date = pd.to_datetime(order_date, errors='coerce')

subtotal = order_table['Subtotal (ex tax)']

coupon_value = order_table['Coupon Value']

products = order_table['Product Details']


df2 = pd.DataFrame({'ID_2' : ID_2,
                  'order_date' : order_date,
                  'subtotal' : subtotal,
                  'coupon_value' : coupon_value,
                  'products' : products})


	# Select index for df and df2 (use "affiliation" or "customer_group" for df)	
df.set_index(affiliation, inplace=True)
df2.set_index(ID_2, inplace=True)


# S P E C I F Y Y O U R V A R I A B L E H E R E

target_groups = df.loc[["Equine - Chiropractor", "Equine - Horse Owner", "Equine - Massage Therapist", "Equine - Trainer/Farrier", "Equine - Veterinarian", "Equine - Retail Store", "Consumer - Equine", "Medical - Massage Therapist (equine)"]]

# S P E C I F Y Y O U R V A R I A B L E H E R E

target_ID_array = array(target_groups['ID'])
    
	#filter out orders that aren't from target groups    
filtered_df2 = df2[df2['ID_2'].isin(target_ID_array)]

	#group orders by month // change freq to "Y"
orders_grouped_monthly = filtered_df2.groupby(pd.Grouper(key="order_date",freq="M")).sum()

	#these are subtotals
subtotals_monthly = orders_grouped_monthly["subtotal"]

	#these are coupon values
coupons_monthly = orders_grouped_monthly["coupon_value"]

	#this is net spend
totals_monthly = subtotals_monthly - coupons_monthly

	#percent couponage per month
print coupons_monthly/subtotals_monthly














