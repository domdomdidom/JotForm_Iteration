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

order_table = ascii.read(directory+'orders-2018-08-28.csv') # Change order file name

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

couponcode_df = df2[df2['coupon_name'] == "ROCKSTOCK10"] # CHANGE COUPON CODE HERE
print str(len(couponcode_df)) + str(" redemptions") + "\n"
print str(len(set(couponcode_df["ID_2"]))) + str(" unique customers") + "\n"

unique_redemptions = len(set(couponcode_df["ID_2"]))

print str(sum(couponcode_df["coupon_value"])) + str("$ - Sumtotal discount amount") + "\n"
print str(mean(couponcode_df["coupon_value"])) + str("$ - Average discount per use") + "\n"


sumsubtotal = sum(couponcode_df["subtotal"])
sumcoupontotal = sum(couponcode_df["coupon_value"])

print str(sum(sumsubtotal - sumcoupontotal)) + str("$ - Sum revenue")+ "\n"
print str((sumsubtotal - sumcoupontotal)/ unique_redemptions) + str("$ - Average order value")+ "\n"