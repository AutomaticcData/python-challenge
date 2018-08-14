# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 08:33:52 2018

@author: anthonyalvarez
"""

#******* imports ********************************
import os
import csv


#******* functions ******************************
#format a long number string
#https://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
def pretty_longnumber(num_longnumber):
    text_numk =     '{:,}'.format(num_longnumber)
    
    return text_numk

#https://stackoverflow.com/questions/5306756/how-to-show-percentage-in-python
def pretty_percentfromdec(num_decimal):
    text_numpercent = '{0:.3%}'.format(num_decimal)
    return text_numpercent


#******* read csv ******************************
#file name
#testing   ---- 'sample_data.csv'
file_name = 'election_data.csv'

#get the csv path
csv_path = os.path.join('Resources',file_name)


#******* open csv ******************************
with open(csv_path, newline='') as csv_file:
    
    #set the contents equal to a variable
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    csv_header = next(csv_reader)
    #print(f'CSV Header: {csv_header}')
    
    #get the csv data into a list
    csv_data = [row for row in csv_reader]
    
    divisor = len(csv_data)


#create a variable to hold the voting information, name and number of votes
votes = {}

#open the file              ***********************
with open(csv_path, newline='') as csv_file:
    #new stuff
    reader = csv.DictReader(csv_file)

#first loop to setup counts
    for row in reader:
        votes.update({row["Candidate"]:0})


#******* re-open the csv due to unexpected error **
#open file again??? why??? ************************
#open the file
with open(csv_path, newline='') as csv_file:
    #new stuff
    reader = csv.DictReader(csv_file)
    for row in reader:
        #get the value from the votes dictionary
        numvotes = votes[row["Candidate"]]
        
        #add 1 count for each candidate
        numvotes += 1
        
        #update the votes dictionary to the number of votes for each Key(candidate)
        votes.update({row["Candidate"]:numvotes})
        
        #print something for testing
        #print(str(row["Candidate"]) + ' ' + str(votes[row["Candidate"]]) + ' number of votes:' + str(numvotes))
        
#testing
#print(votes)

#print("-----------------------------------------")

#******* calculations ******************************
#create the divisor
divisor = len(csv_data)

#create a dictionary to hold the winner information
winner = {"Name":None,"Votes":None,"Percentage":None}

#set the highest number of votes, this should be the winner
num_win = 0

#sort the results by the values DESC
sorted(votes.values(), reverse=True)

#create a result summary
msg_body = ""

#loop through the dictionary values and keys
#---https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops
for the_key, the_value in votes.items():
    
    #get the percentage
    num_percent = the_value/divisor

    #update a variable to hold the highest # of votes 
    #and use that to determine the winner
    if the_value >= num_win:
        num_win = the_value
        
        #set the values for the winner dictionary object
        winner.update({"Name":the_key,"Votes":the_value,"Percentage":num_percent})
        
    #create the message body within the for loop ******************************
    msg_body += f'                {the_key}: {pretty_percentfromdec(num_percent)} ({the_value})\n'




#create the message header ******************************
msg_header = '********************************************************|\n'
msg_header += f'**                Election Results                    **|\n'
msg_header += f'**                                                    **|\n'
msg_header += f'                Total Votes: {pretty_longnumber(len(csv_data))}\n'
msg_header += '********************************************************|\n'


#create the message footer ******************************
msg_footer = '********************************************************|\n'
msg_footer += f'                    Winner: {winner["Name"]}                      \n'
msg_footer += '********************************************************|\n'

#create the message by concatenating the message parts*********************
msg_summary = msg_header
msg_summary += msg_body
msg_summary += msg_footer

#show the user the results
print(msg_summary)   
    
    
#export this to a text file ******************************************
#set a variable for the file path to save the csv, name of the file minus the [.csv]
#and change it to text
new_file = file_name[0:-4] + '.txt'
print(new_file) 

with open(new_file, 'w') as text_file:
    print(msg_summary, file=text_file)

#END******************************************************************
    
    
    
    
    