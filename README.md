# CovidIndia Module

**Description**

This CovidIndia Module has the power to bring all the data related to Covid-19 outbreak in India in a tabular form. This module will bring the whole set of raw data in a date-wise and processed format from [the COVID-19 Indian Dataset maintained by University of Kalyani](https://github.com/kalyaniuniversity/COVID-19-Datasets), which will be easier to deal with.

Once installed, we can get an up-to-date information about the Covid-19 affected people, till the day the data is available at the source. We can visualize the data of our choice for any given range of dates. It is capable of giving information about the total number of confirmed, recovered and deceased patients, between any two dates, of any city, district or related to any particular gender (male/female). We can also visualize the whole up-to-date data without using any aforesaid filters using our module.

# How it works?

It gathers information from our own maintained database. Database data are collected from various websites, news channels and [covid19india.org crowdsourcing initiative](https://www.covid19india.org). From the collected data this module will help user to represent in user friendly format with all types of filters in one place. No need to search any website. Just use this module for India based Covid-19 projects.

## Installation

As of now, the code is kept open-source directly accessible from this repository. We are working on bringing it ot PyPI. Shall update the README as soon as we are done with it.

## Usage

> from Covid.CovidIndia import \*
> #Initialize the module to collect the data
> Init=initializer()
> #shows the collected data in Dataframe formate
> Init.show_data()
> #sample output
> |STATE/UT | Total Confirmed|
> |------------- |------------------- |
> |West Bengal| 126 |
> |Maharashtra| 1761 |
> |Odisha | 54

## Examples

Examples are in github repository project folder.
