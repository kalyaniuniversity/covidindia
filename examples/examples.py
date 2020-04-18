# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:22:26 2020

@author: Dripta
"""
'''This package has the power to bring all data of India as tabular form up-to previous day you are working.It will bring the whole raw data, date wise data. 
It can also visualize the data of your choice of range of dates.You can also see the total confirmed,death and recovered by filtered the data set giving the 
date or range of dates.It can show the Total confirmed cases with count of male and female with state,district and evencity filter also,also produce by date 
or range of date.'''


'''always parse the object of initializer class to other objects as arguments

package name: CovidIndia

'''


# import the package

# 1st initializer must be called
from covdata.covidindia import *
instance_1 = initializer()

# Shows the data that are collected as list
datalist = instance_1.show_data()

# call the 2nd instance object of name data class that reveals all state wise info and death records by dates like thiss
# always pass the 1st instance object to all other instances
instance_2 = Data(instance_1)

# get data for a given state update till today
Set = instance_2.get_dataset_state('py')  # mention state
# if state not mentioned by default it will grab all states
Set = instance_2.get_dataset_state()


# grab cummulative count of all status upto given date of all states
Set_data = instance_2.get_dataset_by_date('10/3/2020')
cumData = instance_2.get_cum_dataset_between_date(
    '30/1/2020', '5/4/2020', by='total recovered')

# grab the counts between two dates of all states by='total confirmed'/'total death'/'total recovered'
setdata2 = instance_2.get_count_between_date(
    '9/03/2020', '30/03/2020', by='total confirmed')
setdata3 = instance_2.get_count_between_date(
    '9/03/2020', '30/03/2020', by='total recovered')
setdata4 = instance_2.get_count_between_date(
    '9/03/2020', '7/04/2020', by='total death')


# grab all data by a particular date of all states by='total confirmed'/'total death'/'total recovered'
setdata5 = instance_2.get_count_by_date('10/3/2020', by='confirmed')
setdata6 = instance_2.get_count_by_date('10/3/2020', by='recovered')
setdata7 = instance_2.get_count_by_date('10/3/2020', by='death')

# top/bottom n points between all states by='total confirmed'/'total death'/'total recovered' for a particular date
instance_2.rank(10, 'Total Confirmed', kind='top',
                cumulative=True, date='4/3/2020')
# if date is not given then it will show top n or bottom n upto now with states names.
instance_2.rank(10, 'Total Confirmed', kind='top', cumulative=True)

# creating object for Demographic_overview class
# it will grab the counts of confirmed cases based on Male,Female and Unknown(if data is not known) for any city or state or district
# you can also use state code
obj = Demographic_overview(instance_1)


obj.demography('Delhi', 'all')  # grab the data for delhi and for all date
# grab the data for delhi for the date 15/4/2020
obj.demography('Delhi', '15/4/2020')
# grab the data for delhi between 10/3/2020 and 15/4/2020
obj.demography('Delhi', '10/3/2020-15/4/2020')
# it also works for any city or state or district
obj.demography('gaya', '10/3/2020-15/4/2020')
# it grabs the data for city gaya between 10/3/2020 and 15/4/2020


# visualization part

# initialize the visualizer
instance_3 = visualizer(instance_1)

# visualize fast n days as cummulative or daily
# if daily is true it gives daily counts of 1st n days
instance_3.head(num=15, daily=False)
instance_3.head(num=5)  # by default daily  is false

# visualize last n days as cummulative or daily
# if daily is true it gives daily counts of last n days
instance_3.tail(num=15, daily=True)
instance_3.tail(num=15)  # by default daily  is false

# visualise the whole data as cummulative or daily
instance_3.whole(daily=True)
instance_3.whole()  # by default daily  is false

# visualize data between two dates as cummulative or daily
instance_3.graph_by_date('30/01/2020', '7/04/2020',
                         state='tg', daily=True)  # by default daily is False
# if state is not mentioned by default it will graph all states together
instance_3.graph_by_date('1/02/2020', '29/03/2020', daily=True)
instance_3.plot_by_latitude()  # plot the total counts for each states vs latitude
