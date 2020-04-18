# covdata.covidindia Module

**Description**

This covidindia Module has the power to bring all the data related to Covid-19 outbreak in India in a tabular form. This module will bring the whole set of raw data in a date-wise and processed format from [the COVID-19 Indian Dataset maintained by University of Kalyani](https://github.com/kalyaniuniversity/COVID-19-Datasets), which will be easier to deal with.

Once installed, we can get an up-to-date information about the Covid-19 affected people, till the day the data is available at the source. We can visualize the data of our choice for any given range of dates. It is capable of giving information about the total number of confirmed, recovered and deceased patients, between any two dates, of any city, district or related to any particular gender (male/female). We can also visualize the whole up-to-date data without using any aforesaid filters using our module.

# How it works?

It gathers information from our own maintained database. Database data are collected from various websites, news channels and [covid19india.org crowdsourcing initiative](https://www.covid19india.org). From the collected data this module will help user to represent in user friendly format with all types of filters in one place. No need to search any website. Just use this module for India based Covid-19 projects.

## Installation

     pip install covdata

PyPi Link: [covdata](https://pypi.org/project/covdata/)

## Usage

     #import module
     from covdata.covidindia import *

     #Initialize the module to collect the data
     Init=initializer()

     #shows the collected data in Dataframe format of Total Confimed data
     Init.show_data(of='Total Confirmed')

     obj1=Data(init)       #defining the object for Data class
     cumData=obj1.get_cum_dataset_between_date('30/1/2020','5/4/2020',by='total recovered')   #gives the cumulative count between 30/1/2020 and 5/4/2020

     obj1.rank(10,'Total Confirmed',kind='top',cummulative=True,date='4/3/2020')   #gives the top 10 total confirmed cases for date 4/3/2020

     obj2=Demographic_overview(init)     # object for demographic_overview class

     obj2.demography('Salt Lake','30/1/2020-10/4/2020')    #Gives Male and Female counts of confirmed cases for salt lake city in west bengal between 30/1/2020 and 10/4/2020

     obj3=visualizer(init)       #initiazing visualizer class

     obj3.whole(daily=True)       #shows line plot for daily counts of confirmed cases,recovered cases and death cases against date.

## Examples

Examples are in [github](https://github.com/kalyaniuniversity/covidindia) repository project folder.

## Terminal Usage

     #get help
     covdata -h

     #get dataset of user choice
     covdata -f Total_Confirmed --options show_data

     #save the above data as csv
     covdata -f Total_Confirmed --options show_data --save PATH\

     #get demographic overview by place and date
     covdata -p wb -d all --options demography   #please use state code.here 'wb' means 'West bengal'

     #get above data for fast n rows for simplicity
     covdata -p wb -d all --options demography -H 10      #head(10)

     #get data by state
     covdata -s mp --options state_dataset       #for madhyapradesh

     #get data by date
     covdata -d 10/4/2020 --options data_by_date

     #get count by date
     covdata -d 11/4/2020 -f Total_Recovered --options count_by_date

     #get top n values in India
     covdata -r 15 -f Total_Confirmed --options rank    #top 10 values of total confirmed cases

     #graph of whole data
     covdata -g whole -D y --options graph    #plot the whole data with dailly counts

     #graph whole data of any state
     covdata -g whole -D y -s wb --options graph    #plots the daily graph of west bengal

     #graph of 1st n data of any selected state ,if state not mentioned all together state count will be shown
     covdata -g head -r 15 -D y -s wb --options graph   #plots 1st 15 days daily counts for west bengal
     covdata -g head -r 15 -D n -s wb --options graph   #plots 1st 15 days cumulative counts for west bengal

     #similarly -g tail will work same and please use state code.Terminal feature demonstrates some methods only that are written in --options flag(type 'covdata -h' to see options)

## Documentation

Help on module covidindia:

NAME
covidindia - Created on Tue Mar 31 15:24:51 2020

DESCRIPTION
@author: Dripta Senapati

CLASSES
builtins.object
Demographic_overview
initializer
Data
visualizer

     class Data(initializer)
     |  Data(init)
     |
     |  # Data class can apply various filters on collected datasets(Confirmed,Recovered,Deceased)
     |  # based on User's choice
     |
     |  Method resolution order:
     |      Data
     |      initializer
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, init)
     |      This is a class that will scrap the data from source upto the previous day of
     |      day of using that package.
     |
     |      Returns
     |      -------
     |      None.
     |
     |  get_count_between_date(self, startDate, endDate, by)
     |      Gives daily count data for all states between two dates
     |
     |      Parameters
     |      ----------
     |      startDate : character
     |          date format dd/mm/yyyy
     |      endDate : character
     |          date format dd/mm/yyyy.
     |      by : character
     |          'Total Confirmed' or 'Total Recovered' or 'Total Death'.
     |
     |      Raises
     |      ------
     |      Exception
     |          Startdate must be less than enddate.If not it raise anexception.
     |          it also raise error for wrong input in by parameter.
     |
     |      Returns
     |      -------
     |      df : DataFrame
     |          DataFrame consisting daily counts for between two given dates
     |          for given by parameter.
     |
     |  get_count_by_date(self, by, date=None)
     |      Gives the daily count of a given date or all dates by 'confirmed' or 'recovered'
     |      or 'death'
     |
     |      Parameters
     |      ----------
     |      by : character
     |          'Confirmed' or 'Recovered' or 'Death'.
     |      date : character, optional
     |          if date(dd/mm/yyyy) is given count will be shown for that date. The default is None.
     |
     |      Raises
     |      ------
     |      Exception
     |          If by argument is not within above mentioned and if year is not 2020 it will
     |          raise an exception.
     |
     |      Returns
     |      -------
     |      df : dataframe
     |          dataframe consisting of counts of given date or all dates for all states .
     |
     |  get_cum_dataset_between_date(self, startDate, endDate, by)
     |      This method of Data class will give cumulative counts between two given dates
     |      for all states
     |
     |      Parameters
     |      ----------
     |      startDate : character
     |          date format dd/mm/yyyy.
     |      endDate : character
     |          date format dd/mm/yyyy.
     |      by : character
     |          'Total Confirmed' or 'Total Recovered' or 'Total Death'.
     |
     |      Raises
     |      ------
     |      Exception
     |          startdate should be less than endDate---if not it will raise exception.
     |
     |      Returns
     |      -------
     |      df : Dataframe
     |          returns a dataframe of cumulative counts between two dates for all states by
     |          'Total Confirmed' or 'Total Recovered' or 'Total Death'.
     |
     |  get_dataset_by_date(self, date)
     |      This method of Data Class will allow user to get cumulative count of all states of
     |      total confirmed,total death and total recovered
     |      India for a particular given date
     |
     |      Parameters
     |      ----------
     |      date : character
     |          Should be in dd/mm/yyyy format.
     |
     |      Returns
     |      -------
     |      df : Dataframe
     |          Dataframe consisting all cumulative values of total confirmed,total recovered,total
     |          death for a given date.
     |
     |  get_dataset_state(self, state='Whole')
     |      this method of Data class will allow user to get cumulative counts of a particular
     |      state.
     |
     |      Parameters
     |      ----------
     |      state : character, optional
     |          name of state in India. The default is 'Whole'.
     |          state code also applicable.
     |      Returns
     |      -------
     |      df : DataFrame
     |          if state is whole then it Returns a dataframe consisting all states having
     |          cumulative count of totalconfirmed,total recovered,total death till the previous day of the day of using this package.
     |          if state is mentioned then it will return a dataframe consisting the names
     |          of districts with total cumultive counts of confirmed only
     |
     |  rank(self, num, by, kind='top', cumulative=False, date=None)
     |      Gives top n or bottom n values as cumulative or daily basis for a date or
     |      combining whole dates filtered with by parameter.
     |
     |      Parameters
     |      ----------
     |      num : integer
     |          number of rows user want to see.
     |          e.g num=10 -> top/bottom 10 data will be shown
     |      by : character
     |          'Total Confirmed' or 'Total Recovered' or 'Total Death'.
     |      kind : character, optional
     |          'top' or 'bottom' by which data will be filtered. The default is 'top'.
     |      cumulative : bool, optional
     |         if True it will show cumulative counts. The default is False.
     |      date : character, optional
     |          (must be in dd/mm/yyyy format)if date is given then method will return cumulative or daily count
     |          for that date. The default is None.
     |          if None it will return all cumulative/daily counts
     |
     |      Raises
     |      ------
     |      Exception
     |          if date is None and cumulative is false then it is not possible to show
     |          data for top n or botom n rows..
     |
     |      Returns
     |      -------
     |      dataframe/dictionary
     |          if date is not given and cummulative is False then it prompt to input state(state code or name)
     |          if state is set to 'all' it will return dictionary consisting all states having top/bottom counts
     |          otherwise a dataframe for a given state.
     |          whenever date is mentioned a dataframe will be returned consisting top/bottom cumulative count or
     |          daily count for that date.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from initializer:
     |
     |  show_data(self,of)
     |      This method only assembles the collected data of Tota Confirmed/Total Recovered/Total Death
     |
     |      Parameters
     |      ----------
     |      of : character, Tota Confirmed/Total Recovered/Total Death(any one)
     |      Returns
     |      -------
     |      Dataframe
     |          returns dataframe consisting of data by Tota Confirmed/Total Recovered/Total Death.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from initializer:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class Demographic_overview(initializer)
     |  Demographic_overview(init)
     |
     |  Method resolution order:
     |      Demographic_overview
     |      initializer
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, init)
     |      This Demographic_overview class has the power of filtering in terms of state,
     |      district,city,date or range of date
     |
     |      Returns
     |      -------
     |      None.
     |
     |  demography(self, place='all', date='all')
     |      This method can show the male and female count of confirmed cases for a state or a district or
     |      a city for a given date of range of date.
     |
     |      Parameters
     |      ----------
     |      place : character, optional
     |          place can be state or district or city.this method automatically recognize the place
     |          and gives user data for that place. The default is 'all'.If place is mentioned data for all places
     |          will be shown.
     |      date : character, optional
     |          by which date or range of date the data will be filtered.Date must be dd/mm/yyyy format.
     |          The default is 'all'.if date is not mentioned data for all dates will be shown.
     |          set date: '30/1/2020-9/3/2020'. to represent a range.range dates should be separated by '-'.
     |
     |      Raises
     |      ------
     |      Exception
     |          If no data is found for a date or a place it will raise exceptions.
     |
     |      Returns
     |      -------
     |      Dataframe
     |          dataframe consists of male female counts of confirmed cases for given date and place.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from initializer:
     |
     |  show_data(self)
     |      This method only assembles the collected data
     |
     |      Returns
     |      -------
     |      list
     |          returns collected data as 3 dataframe format.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from initializer:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class initializer(builtins.object)
     |  Methods defined here:
     |
     |  __init__(self)
     |      This is a class that will scrap the data from source upto the previous day of
     |      day of using that package.
     |
     |      Returns
     |      -------
     |      None.
     |
     |  show_data(self)
     |      This method only assembles the collected data
     |
     |      Returns
     |      -------
     |      list
     |          returns collected data as 3 dataframe format.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class visualizer(initializer)
     |  visualizer(init)
     |
     |  Method resolution order:
     |      visualizer
     |      initializer
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, init)
     |      Gather all information to perform the visualization
     |
     |      Parameters
     |      ----------
     |      init : TYPE
     |          None.
     |
     |      Returns
     |      -------
     |      None.
     |
     |  graph_by_date(self, startDate, endDate, state=None, daily=False)
     |      Gives the visualization of cumulative data or daily data between two given
     |      dates for a given state or as whole india.
     |
     |      Parameters
     |      ----------
     |      startDate : character
     |          dd/mm/yyyy format(e.g 02/04/2020).
     |      endDate : character
     |          dd/mm/yyyy format(e.g 02/04/2020).
     |      state : character, optional
     |          for which state graph will be plotted.If None graph will be plotted for whole india. The default is None.
     |          states input also takes state codes.
     |      daily : bool, optional
     |          if True graph will plotted daily basis. The default is False.
     |
     |      Raises
     |      ------
     |      Exception
     |          startdate must be less than enddate and if states are given wrong it will raise exception.
     |
     |      Returns
     |      -------
     |      3 subplots consisting date vs total confirmed,date vs total recovered,date vs total deceased for a state or whole india
     |      between two dates.
     |      may be daily or cumulative based on daily parameter passed.
     |
     |  head(self, num, daily=False)
     |      Gives graphical visualization of first n(=num) dayes based on daily or cumulative data
     |
     |      Parameters
     |      ----------
     |      num : integer
     |          setd the number of dates from start user wants to see.
     |      daily : bool, optional
     |          if true graph is plotted based on daily data. The default is False.
     |
     |      Returns
     |      -------
     |      3 subplots consisting date vs total confirmed,date vs total recovered,date vs total deceased.
     |      may be daily or cumulative based on daily parameter passed.
     |
     |  plot_by_latitude(self)
     |      Gives the visualization of counts with respect to state latitudes
     |
     |      Returns
     |      -------
     |      3 subplots consisting latitude vs latitude confirmed,latitudes vs total recovered,latitudes vs total deceased.
     |
     |  tail(self, num, daily=False)
     |      Gives graphical visualization of latest n(=num) dayes based on daily or cumulative data
     |
     |      Parameters
     |      ----------
     |      num : integer
     |          setd the number of latest dates user wants to see.
     |      daily : bool, optional
     |          if true graph is plotted based on daily data. The default is False.
     |
     |      Returns
     |      -------
     |      3 subplots consisting date vs total confirmed,date vs total recovered,date vs total deceased.
     |      may be daily or cumulative based on daily parameter passed.
     |
     |  whole(self, daily=False)
     |      Generate 3 subplots of whole collected data
     |
     |      Parameters
     |      ----------
     |      daily : bool, optional
     |          if True garph will be plotted on daily counts otherwise on cumulative counts. The default is False.
     |
     |      Returns
     |      -------
     |      3 subplots consisting date vs total confirmed,date vs total recovered,date vs total deceased.
     |      may be daily or cumulative based on daily parameter passed.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from initializer:
     |
     |  show_data(self)
     |      This method only assembles the collected data
     |
     |      Returns
     |      -------
     |      list
     |          returns collected data as 3 dataframe format.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from initializer:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
