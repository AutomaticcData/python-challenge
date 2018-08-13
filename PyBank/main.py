# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 23:54:17 2018

@author: anthony alvarez
"""

#import the os Module
import os

#import the csv csvreader
import csv



#*** define the function here ********
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


#*******************************************************
#set aside variable as not to confuse myself later

#lists for columns to zip later
col_dates = []
col_revenue = []

#total amounts
totals = []

#profit/losses variable
profit = []
losses = []

#greater/least profits/losses
gprofit = 0
gloss = 0
gc_text = ""
gl_text = ""

begin_date = ""
end_date = ""

#*******************************************************

#file name
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
    
    #not sure how to put this into a list comprehension yet
    for revenue in csv_data:        
        #sets the current amount of revenue
        this_amount = float(revenue[1])
        this_date = revenue[0]

        #get both columns in lists
        col_dates.append(this_date)
        col_revenue.append(this_amount)
        
        #add it to the totals list
        totals.append(this_amount)
        
        if this_amount > 0:
            profit.append(this_amount)
            #print(str(this_amount))
            
        if this_amount <= 0:
            losses.append(this_amount)
            #print(str(this_amount))

        if this_amount > 0 and gprofit ==0:
            gprofit = this_amount
        else:
            if this_amount > gprofit:
                gprofit = this_amount
                gc_text = f'{this_date} ({pretty_money(gprofit)})'
                
        if this_amount < 0 and gloss ==0:
            gloss = this_amount
        else:
            if this_amount < gloss:
                gloss = this_amount
                gl_text = f'{this_date} ({pretty_money(gloss)})'


#***************************************************************
#Tidy up the data
                
#get the number of months
total_months = len(csv_data)
            
#total net profit/losses
#https://stackoverflow.com/questions/4362586/sum-a-list-of-numbers-in-python
n_profits = sum(profit)
n_losses = sum(losses)

#total net amount formula (could be put in a function)
total_net_amount = (n_profits - n_losses)

#format as a nice currency string
#'${:,.2f}'.format(xxxxxx)
#https://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
#text_total_net_amount = '${:,.2f}'.format(total_net_amount)
#using the new function
text_total_net_amount = pretty_money(total_net_amount)
    
#average change in profits/losses
#pass the totals list to the average function defined above
avg_change_amount = my_average(totals)
#text_avg_change_amount = '${:,.2f}'.format(total_net_amount)
#using the new function
text_avg_change_amount = pretty_money(avg_change_amount)



#set begin and end dates for text range
begin_date = col_dates[0].split('-')
#begin_text = str(begin_date[0]) + ' 20' + begin_date[1]
begin_text = fix_yearmonth(col_dates[0])

end_date = col_dates[-1].split('-')
end_text = str(end_date[0]) + ' 20' + end_date[1]

 
#print out the summary to the user *********************************
msg_output = '********************************************************|\n'
msg_output += f'*** Financial Analysis                     *************|\n'
msg_output += f'*** Budget Data:    {file_name}        *************|\n'
msg_output += f'*** for the period of {begin_text} to {end_text} *************|\n'
msg_output += '********************************************************|\n'
msg_output += f'Total Months: {total_months}\n'

msg_output += f'Total: {text_total_net_amount}\n'

msg_output += f'Average Change: {text_avg_change_amount}\n'

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
