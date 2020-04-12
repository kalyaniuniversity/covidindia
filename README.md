# CovidIndia Module
**Description**

This package has the power to bring all data of India as tabular form up-to previous day you are working.But due to some unavailability of prefect data the state wise data sets are up to date. It can't be filtered by date. Beside that it will bring the whole raw data, date wise data. It can also visualize the data of your choice of range of dates.You can also see the total confirmed,death and recovered by filtered the data set giving the date or range of dates.


# How it works?

Basically it gathers information from our own maintained database. Database data are collected from various websites and news channels. From the collected data this module will help user to represent in user friendly format with all types of filters in one place. No need to search any website.Just use this module for India based Covid-19 projects.

## Installation

This package can be installed by pip package manager shortly after it is published on PyPi

## Basic Usage
>from Covid.CovidIndia import *
>#Initialize the module to collect the data
>Init=initializer()
>#shows the collected data in Dataframe formate
>Init.show_data()
>#sample output
>|STATE/UT  | Total Confirmed|
>|------------- |------------------- |
>|West Bengal|        126            |
>|Maharashtra| 1761                 |
>|Odisha         | 54      


## Examples

Examples are in github repository project folder.

