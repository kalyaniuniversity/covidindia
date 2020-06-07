# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:22:26 2020

@author: Dripta
"""
'''This covidindia Module has the power to bring all the data related to Covid-19 outbreak in India in a 
tabular form. This module will bring the whole set of raw data in a date-wise and processed format from 
[the COVID-19 Indian Dataset maintained by University of Kalyani](https://github.com/kalyaniuniversity/COVID-19-Datasets), 
which will be easier to deal with.

Once installed, we can get an up-to-date information about the Covid-19 affected people, till the day the data
 is available at the source. We can visualize the data of our choice for any given range of dates. It is 
 capable of giving information about the total number of confirmed, recovered and deceased patients, 
 between any two dates, of any city, district or related to any particular gender (male/female). 
 We can also visualize the whole up-to-date data without using any aforesaid filters using our module.'''


'''always parse the object of initializer class to other objects as arguments

package name: CovidIndia

'''


# import the package

# 1st initializer must be called
from covdata.covidindia import *
instance_1 = initializer()

# Shows the data that are collected
# shows daily count confirmed dataset that gathered from source
data = instance_1.show_data(of='confirmed', daily=True)
# shows the recovered dataset that gathered from source.If daily is not mentioned then cumulative dataset will be shown.
data = instance_1.show_data(of='recovered')
# shows the daily count death dataset that gathered from source
data = instance_1.show_data(of='death', daily=True)

# create an object of Data class
# always pass the 1st instance object to all other instances
instance_2 = Data(instance_1)

# get data for a given state update till today
# shows daily counts of confirmed,recovered and death for all dates of Pondicherry
Set = instance_2.get_dataset_state(state='wb', daily=True)
# shows counts of only confirmed cases of districts of Pondicherry
Set = instance_2.get_dataset_state(state='py', daily=False)
# shows total counts of confirmed,recovered and death for all states(cause state is not mentioned)
Set = instance_2.get_dataset_state(daily=False)
# returns a dictionary containing confirmed,recovered and death dataframes containing datewise counts for all states.
Set = instance_2.get_dataset_state(daily=True)
# if state is not mentioned by default it will grab data for all the states
Set = instance_2.get_dataset_state()


# grab cumulative count of all states upto given date for all states
Set_data = instance_2.get_dataset_by_date('10/3/2020')
cumData = instance_2.get_cum_dataset_between_date(
    '30/1/2020', '5/4/2020', by='total recovered')

# grab the daily counts between two dates of all states by='confirmed'/'death'/'recovered'
setdata2 = instance_2.get_count_between_date(
    '9/03/2020', '30/03/2020', by='confirmed')
setdata3 = instance_2.get_count_between_date(
    '9/03/2020', '30/03/2020', by='recovered')
setdata4 = instance_2.get_count_between_date(
    '9/03/2020', '7/04/2020', by='death')


# grab all data by a particular date of all states by='total confirmed'/'total death'/'total recovered'
setdata5 = instance_2.get_count_by_date('10/3/2020', by='confirmed')
setdata6 = instance_2.get_count_by_date('10/3/2020', by='recovered')
setdata7 = instance_2.get_count_by_date('10/3/2020', by='death')

# top/bottom n points between all states by='total confirmed'/'total death'/'total recovered' for a particular date
instance_2.rank(10, 'Total Confirmed', kind='top',
                cumulative=True, date='4/3/2020')  # top 10 cumulative cumulative count for date 4/3/2020

instance_2.rank(10, 'Total Confirmed', kind='top',
                cumulative=False, date='4/3/2020')  # top 10 daily counts for date 4/3/2020

# if date is not given then it will show top n or bottom n rows with states names.
# kind may be top or bottom for rank methods.
instance_2.rank(10, 'Total Confirmed', kind='top', cumulative=False)

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

# visualize fast n days as cumulative or daily
# if daily is true it gives daily counts of 1st n days
instance_3.head(num=15, daily=False, title='1st 15 cumulative plot')
# by default daily  is false and does not set any title if title is not mentioned.
instance_3.head(num=5)

# visualize last n days as cumulative or daily
# if daily is true it gives daily counts of last n days
instance_3.tail(num=15, daily=True, title='last 15 daily count plot')
# by default daily  is false and does not set any title if title is not mentioned.
instance_3.tail(num=15)

# visualise the whole data as cumulative or daily
instance_3.whole(daily=True, title='daily count plot for all states')
instance_3.whole()  # by default daily  is false and does not set the title

# visualize data between two dates as cumulative or daily
instance_3.graph_by_date('30/01/2020', '7/04/2020',
                         state='tg', daily=True, title='daily count plot between 30/1/2020 and 7/4/2020 of telengana')  # by default daily is False
# if state is not mentioned by default it will graph all states together
instance_3.graph_by_date('1/02/2020', '29/03/2020', daily=True,
                         title='daily count plot between 1/2/2020 and 29/03/2020 for all states together')
