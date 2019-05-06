from numpy import *
import numpy as np
from astropy.io import ascii
import datetime
import pandas as pd

###########################################################
directory = '/Users/domvandendries/Desktop/'
###########################################################

vyne_table = ascii.read(directory+'Massage_Lead_List.csv',
                        header_start=0,
                       data_start=1)

vyne_email = vyne_table['Email Address']

vyne_email = list(vyne_table['Email Address'])

vyne_email = [x for x in vyne_email if x != str] # Clean masked (missing) elements

###########################################################

custy_table = ascii.read(directory+'custy_export.csv',
                        header_start=0,
                        data_start=1)

customer_group = custy_table['Customer Group']

affiliation = custy_table['Your Affiliation']

email = custy_table['Email']

custyDF = pd.DataFrame({'email' : email,
                  'customer_group' : customer_group,
                  'affiliation' : affiliation})

###########################################################

order_table = ascii.read(directory+'all_orders_ever.csv')

order_email = order_table['Customer Email']

order_date = order_table['Order Date']
order_date = pd.to_datetime(order_date, errors='coerce')

total = order_table['Order Total (ex tax)']


orderDF = pd.DataFrame({'order_email' : order_email,
					'order_date' : order_date,
                  'total' : total})

filtered_orderDF = orderDF[(orderDF['order_date'] > '2017-01-01') & (orderDF['order_date'] < '2018-09-01')]



not_in_BC = [] # Vyne people who do not have an account in BC
BC_customer = [] # Vyne people who have an account in shop.rocktape.com
custyDF.set_index(email, inplace=True)

for email_address in vyne_email:
    
    if email_address not in custyDF['email']:
        not_in_BC.append(email_address) 
    
    else:
        BC_customer.append(email_address)




never_made_purchase = [] # Vyne people who have an account in BC, but have not made a purchase
paying_customer = [] # Vyne people who have made a purchase at shop.rocktape.com

AOV_list = []
lifetime_spend = 0

for email_address in BC_customer:
    
    filtered_orderDF.set_index(filtered_orderDF['order_email'], inplace=True)
    
    if email_address not in set(filtered_orderDF['order_email']):
        never_made_purchase.append(email_address)
    
    else:
        
        paying_customer.append(email_address)
        
        matches = filtered_orderDF.loc[[email_address]]
        
        AOV = sum(matches[["total"]])/len(matches)

        lifetime_spend += sum(matches[["total"]])

        AOV_list.append(AOV)



print str(len(vyne_email)) + str(" Contacts from Lead List examined")
print str(len(not_in_BC)) + str(" people do not have an account in BC") #+ str("(") + (len(not_in_BC)/len(vyne_email)) + str("%") + str(")")
print str(len(BC_customer)) + str(" people have an account in BC") + "\n" #+ str("(") + str(float(len(BC_customer)/len(vyne_email))) + str("%") + str(")") + "\n"

print str("Of the ") + str(len(BC_customer)) + str(" people who have an account in BC, ") + str(len(never_made_purchase)) + str(" people never made a purchase in BC") #+ str("(") + str(float(len(never_made_purchase)/len(BC_customer))) + str("%") + str(")")
print str("Of the ") + str(len(BC_customer)) + str(" people who have an account in BC, ") + str(len(paying_customer)) + str(" people completed a purchase in BC") + "\n" #+ str("(") + str(float(len(paying_customer)/len(BC_customer))) + str("%") + str(")") + "\n"

print str("Of the ") + str(len(paying_customer)) + str(" who completed a purchase in BC, their AOV is between $") + str(median(AOV_list)) + str(" and $") + str(mean(AOV_list))
print str("Lifetime spend = $ ") + str(lifetime_spend)

