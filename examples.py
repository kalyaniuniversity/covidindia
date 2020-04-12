# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:22:26 2020

@author: Dripta
"""
'''This package has the power to bring the datasets till previous day you are working.
But due to some unavailibility of prefect data the state wise datasets are up to date.
It can't be filtered by date. Beside that it will bring the whole raw data, date wise data.
It can also visualize the data of your choice of range of dates.You can also see the total confirmed,
death and recovered by filtered the dataset giving the date or range of dates.'''


'''always parse the object of initializer class to other objects as arguments

package name: CovidIndia

'''
 


#import the package
from Covid.CovidIndia import *

#1st initializer must be called
instance_1=initializer()

#Shows the data that are collected as list
datalist=instance_1.show_data()

#call the 2nd instance object of name data class that reveals all state wise info and death records by dates like thiss
#always pass the 1st instance object to all other instances
instance_2=Data(instance_1)

#get data for a given state update till today
Set=instance_2.get_dataset_state('py') #mention state
Set=instance_2.get_dataset_state() #if state not mentioned by default it will grab all states


#grab cummulative count of all status upto given date of all states
Set_data=instance_2.get_dataset_by_date('10/3/2020') 
cumData=instance_2.get_cum_dataset_between_date('30/1/2020','5/4/2020',by='total recovered')

#grab the counts between two dates of all states by='total confirmed'/'total death'/'total recovered'
setdata2=instance_2.get_count_between_date('9/03/2020','30/03/2020',by='total confirmed')
setdata3=instance_2.get_count_between_date('9/03/2020','30/03/2020',by='total recovered')
setdata4=instance_2.get_count_between_date('9/03/2020','7/04/2020',by='total death')


#grab all data by a particular date of all states by='total confirmed'/'total death'/'total recovered'
setdata5=instance_2.get_count_by_date('10/3/2020',by='confirmed')
setdata6=instance_2.get_count_by_date('10/3/2020',by='recovered')
setdata7=instance_2.get_count_by_date('10/3/2020',by='death')

#top/bottom n points between all states by='total confirmed'/'total death'/'total recovered' for a particular date
instance_2.rank(10,'Total Confirmed',kind='top',cummulative=True,date='4/3/2020')
#if date is not given them it will show top n or bottom n upto now with states names.
instance_2.rank(10,'Total Confirmed',kind='top',cummulative=True)

#creating object for Demographic_overview class
obj=Demographic_overview()

#getting data by running the following and giving some filters in the console
demographyData=obj.demograpy()









#visualization part

#initialize the visualizer
instance_3=visualizer(instance_1)

#visualize fast n days as cummulative or daily
instance_3.head(num=15,daily=False) #if daily is true it gives daily counts of 1st n days
instance_3.head(num=5) #by default daily  is false

#visualize last n days as cummulative or daily
instance_3.tail(num=15,daily=True)#if daily is true it gives daily counts of last n days
instance_3.tail(num=15)#by default daily  is false

#visualise the whole data as cummulative or daily
instance_3.whole(daily=True) 
instance_3.whole() ##by default daily  is false

#visualize data between two dates as cummulative or daily
instance_3.graph_by_date('30/01/2020', '7/04/2020',state='tg',daily=True) #by default daily is False
instance_3.graph_by_date('1/02/2020', '29/03/2020',daily=True) #if state is not mentioned by default it will graph all states together 

instance_3.plot_by_latitude() #plot the total counts for each states vs latitude

