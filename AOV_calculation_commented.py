import os
from numpy import *
import numpy as np
from astropy.io import ascii
import datetime
import pandas as pd
from astropy.table import Table

directory = '/Users/domvandendries/Desktop/'

custy_table = ascii.read(directory+'custy_export.csv', # Customer Export file from BC
                        header_start=0,
                        data_start=1)

ID = custy_table['Customer ID']

customer_group = custy_table['Customer Group']

affiliation = custy_table['Your Affiliation']

join_date = custy_table['Date Joined']
join_date = pd.to_datetime(join_date, errors='coerce')

email = custy_table['Email']

df = pd.DataFrame({'ID' : ID,
                  'customer_group' : customer_group,
                  'affiliation' : affiliation,
                  'email' : email})



order_table = ascii.read(directory+'order_export (2017).csv') # Order Export from BC

ID_2 = order_table['Customer ID']

order_date = order_table['Order Date']
order_date = pd.to_datetime(order_date, errors='coerce')

subtotal = order_table['Subtotal (ex tax)']

products = order_table['Product Details']

df2 = pd.DataFrame({'ID_2' : ID_2,
                  'order_date' : order_date,
                  'subtotal' : subtotal,
                   'products' : products})



	# Initialize indexes for df and df2
df.set_index(affiliation, inplace=True)
df2.set_index(ID_2, inplace=True)

	# Set first filter and compile "x_ID_array"
n = df.loc[["Medical - Chiropractor"]]
x_ID_array = n.iloc[:,0]
x_ID_array = array(x_ID_array)

	# Set second filter and compile "y_ID_array" (optional)
df.set_index(customer_group, inplace=True)
n = df.loc[["Medical 40", "Medical 50"]]
y_ID_array = n.iloc[:,0]
y_ID_array = array(y_ID_array)

	# xy_ID_array spans the commonalities between x_ID_array and y_ID_array
xy_ID_array = []
for ID_number in x_ID_array:
    if ID_number in y_ID_array:
        xy_ID_array.append(ID_number)
    
    # Reindex df to search on ID
df.set_index(ID, inplace=True)
    
    # Initialize blank lists to hold values
subs_list = []
AOV_list = []
MOV_list = []
frequency_list = []

for ID_number in xy_ID_array: # Iterate through each person in the xy_ID_array (Change this to x_ID_array if there is only one filter)

    df2.set_index(ID_2, inplace=True)

    if ID_number not in ID_2: # Pass if there is no 2017 order
        pass 


    else: 
        matches = df2.loc[[ID_number]] # Returns all orders placed by specific ID in 2017
        products_purchased = matches.iloc[:,2] # All products purchased

        subs = array(matches.iloc[:,3]) # All subtotals (excluding tax and shipping)
            
        for i in subs:
            subs_list.append(i) # subs_list holds every single subtotal


        frequency = len(subs) # The frequency is the amount of subtotals in the returned dataframe. No need to normalize, since we're examining a one year span (2017)


        customer_AOV = mean(array(matches.iloc[:,3])) # AOV is the mean of the subtotals 
        customer_MOV = median(array(matches.iloc[:,3])) # MOV is the median of the subtotals


        AOV_list.append(customer_AOV) # Indivual AOVs are put in an aggregate AOV list
        AOV_list = [x for x in AOV_list if str(x) != 'nan']

        MOV_list.append(customer_MOV) # Individual MOVs are put in an aggregate MOV list
        MOV_list = [x for x in MOV_list if str(x) != 'nan']

        frequency_list.append(frequency)
        
    # RETURNS
print "AOV : " + str(mean(AOV_list)) # Average order value
print "MOV : " + str(median(MOV_list)) # Median order value

print "Total Net - $" + str(sum(subs_list)) # Total gross sales to cohort
print str(len(subs_list)) + " orders from " + str(len(AOV_list)) + " unique customers"

print "Avg frequency of purchase - " + str(mean(frequency_list)) # average frequency of purchase




