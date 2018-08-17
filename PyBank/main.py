# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 23:54:17 2018

@author: anthony alvarez
The total number of months included in the dataset
The total net amount of "Profit/Losses" over the entire period
The average change in "Profit/Losses" between months over the entire period
The greatest increase in profits (date and amount) over the entire period
The greatest decrease in losses (date and amount) over the entire period
8/15/2018 changed variable names and use of for loops
8/16/2018 added lists and dictionaries to hold data
8/17/2018 reworked code due to wrong referenced field for greatest/least change

"""

#************IMPORTS*******************************************
#import the os Module
import os

#import the csv csvreader
import csv

#************FUNCTIONS*****************************************
def my_average(num_list):
    #the number to divide by
    num_divisor = len(num_list)

    #create a variable to hold the sum of numbers
    num_total = 0.00

    #create a variable for the mean(average)
    num_mean = 0

    #iterate through the list and get a sum of the numbers
    for x in range(len(num_list)):
        #print(num_list[x])
        num_total += num_list[x]
    num_mean = (num_total/num_divisor)

    return num_mean

#format a nice currency string
def pretty_money(num_float):
    text_money =     '${:,.2f}'.format(num_float)
    
    return text_money

#fix the date to be more readable
def fix_yearmonth(ym_val):
    ym_fix = ym_val.split('-')
    ym_text = str(ym_fix[0]) + ' 20' + ym_fix[1]
    return ym_text


#clean a key value string from a dictionary
def clean_keyvalue(dirtystring):
    dirtystring = dirtystring.replace("['","")
    dirtystring = dirtystring.replace("']","")
    cleanstring = dirtystring
    return cleanstring

#************VARIABLES******************************************
#set aside variable as not to confuse myself later

#dictionaries
greaterchange = {}
leastchange = {}

#lists
totals = []
poschange = []
negchange = []
revenue_changes = []

#vars
tamount = 0
tprofit = 0
tloss = 0   

changeinnumber = 0
newnumber = 0
originalnumber = 0    

#************FILE OPERTATIONS*******************************
file_name = 'budget_data.csv'

#get the csv path
csv_path = os.path.join('Resources',file_name)

#open the file
with open(csv_path, newline='') as csv_file:
    
    #set the contents equal to a variable
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    csv_header = next(csv_reader)
    #print(f'CSV Header: {csv_header}')
    
    #get the csv data into a list
    csv_data = [row for row in csv_reader]
    
    #get the bounds of the data
    upperbound = len(csv_data)
      
    for i in range(upperbound):
        #set the current revenue amount
        current_revenue = float(csv_data[i][1])
        
        #add it to the totals list
        totals.append(current_revenue)
        
        
        #sum of the revenue amounts
        tamount += current_revenue
        
        #get values for positive and negative revenue
        if current_revenue>0:
            tprofit += current_revenue
        else:
            tloss += current_revenue
    

        #current revenue value
        newnumber = float(csv_data[i][1])
        
        #revenue date
        revenue_date = csv_data[i][0]
        
        #change in revenue
        if i == 0: 
        #or i == upperbound-1:
            #only if we are at the first record, then there was no change            
            originalnumber = float(0)
            changeinnumber = float(0)
            
            #all ther rows that arent first or last
        else:   
            #if not (i == 0) and not (i >= upperbound-1):    
            #previous revenue value
            originalnumber = float(csv_data[i-1][1])
            changeinnumber = float(newnumber) - float(originalnumber)
            
        
        #get a list of the revenue changes month to month
        revenue_changes.append(changeinnumber)
        
        #print(f'{tpos} = Current: {current_revenue}    |   Next:{next_revenue}   |   Change:{changeinrevenue}')
        #print(f'Current: {originalnumber}    |   Next:{newnumber}   |   Change:{changeinnumber}')

        #indicates a positve change
        if changeinnumber > 0:
            poschange.append(changeinnumber)
            greaterchange.update({revenue_date: changeinnumber})
        #negative change
        elif changeinnumber <0:
            negchange.append(changeinnumber)
            leastchange.update({revenue_date: changeinnumber})

#get the number of months
total_months = len(csv_data)
#total net profit/losses
total_net_amount = pretty_money(tamount)
#average change
average_change = my_average(revenue_changes)


#https://stackoverflow.com/questions/42044090/return-the-maximum-value-from-a-dictionary/42044202
#greatest increase in profits
max_value = max(greaterchange.values())  # maximum value
max_keys = [k for k, v in greaterchange.items() if v == max_value] # getting all keys containing the maximum

greatestincrease_value = pretty_money(max_value)
greatestincrease_month = fix_yearmonth(clean_keyvalue(str(max_keys)))

#print(greatestincrease_month)
#print(greatestincrease_value)
#print(max_value, max_keys)

#greatest decrease in profits
min_value = min(leastchange.values())  # maximum value
min_keys = [k for k, v in leastchange.items() if v == min_value] # getting all keys containing the minimum

greatestdecrease_value = pretty_money(min_value)
greatestdecrease_month = fix_yearmonth(clean_keyvalue(str(min_keys)))

gc_text = f'{greatestincrease_month} ({greatestincrease_value})'
gl_text = f'{greatestdecrease_month} ({greatestdecrease_value})'

#print out the summary to the user *********************************
msg_output = '********************************************************|\n'
msg_output += f'*** Financial Analysis                     *************|\n'
msg_output += f'*** Budget Data:    {file_name}        \n'
#msg_output += f'*** for the period of {begin_text} to {end_text} *************|\n'
msg_output += '********************************************************|\n'
msg_output += f'Total Months: {total_months}\n'

msg_output += f'Total: {total_net_amount}\n'

msg_output += f'Average Change: {pretty_money(average_change)}\n'

msg_output += f'Greatest Increase in Profits: {gc_text}\n'

msg_output += f'Greatest Decrease in Profits: {gl_text}\n'
msg_output += '********************************************************|\n'

print(msg_output)


#export this to a text file ******************************************
#set a variable for the file path to save the csv, name of the file minus the [.csv]
#and change it to text
new_file = file_name[0:-4] + '.txt'
print(new_file) 

with open(new_file, 'w') as text_file:
    print(msg_output, file=text_file)

#END******************************************************************
