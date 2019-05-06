import os
from numpy import *
import numpy as np
from astropy.io import ascii
import datetime
import pandas as pd
from astropy.table import Table
############################################
directory = '/Users/domvandendries/Desktop/' # CD '/Users/stefanoscalia/Desktop/'
############################################

custy_table = ascii.read(directory+'custy_export.csv', # Change customer file name
                        header_start=0,
                        data_start=1)

ID = custy_table['Customer ID']

customer_group = custy_table['Customer Group']

affiliation = custy_table['Your Affiliation']


df = pd.DataFrame({'ID' : ID,
                  'customer_group' : customer_group,
                  'affiliation' : affiliation})

##################################

order_table = ascii.read(directory+'orders-2018-08-29.csv') # Change order file name

ID_2 = order_table['Customer ID'] 

order_ID = order_table['Order ID']

order_date = order_table['Order Date']  
order_date = pd.to_datetime(order_date, errors='coerce')

subtotal  = order_table['Subtotal (ex tax)'] 

shiptotal = order_table['Shipping Cost (inc tax)']

coupon_name = order_table['Coupon Name']

coupon_value = order_table['Coupon Value']

products= order_table['Product Details'] 


df2 = pd.DataFrame({'ID_2' : ID_2,
                  'order_date' : order_date,
                    'order_ID' : order_ID,
                  'subtotal' : subtotal,
                    'shiptotal' : shiptotal,
                    'coupon_name' : coupon_name,
                    'coupon_value' : coupon_value,
                   'products' : products})


df.set_index(customer_group, inplace=True)
df2.set_index(ID_2, inplace=True)

#########################################################
df = df.fillna('')

# Keep Med40 and Med50, drop med disty
med_filter_df = df[df['customer_group'].str.contains("Medical")] 
med_filter_df = med_filter_df[~med_filter_df['customer_group'].str.contains("Distributor")]
medical_ID_array = med_filter_df["ID"]

# Filter order dataframe by those in medical_ID_array
filtered_df2 = df2[df2['ID_2'].isin(medical_ID_array)]

# Filter orders by subtotals >= 400 
orders_over_400_df = filtered_df2[filtered_df2['subtotal'] >= 400.00]

print str(len(orders_over_400_df)) + str(" uses") + "\n"
print str(len(set(orders_over_400_df["ID_2"]))) + str(" unique customers") + "\n"

sum_subtotal = sum(orders_over_400_df['subtotal'])
sum_15_promo_discount = .15*sum_subtotal
sum_additional_coupons = sum(orders_over_400_df['coupon_value'])

print str(sum_15_promo_discount) + str(" - sum of cart level discounts") + "\n"
print str(sum_additional_coupons) + str(" - sum of additional coupons") + "\n"

print str((sum_subtotal - sum_15_promo_discount) - sum_additional_coupons) + str(" - revenue generated from sale including any additional coupons used")


