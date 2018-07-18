########################################################################
#    USAGE:
#       python3 cleanUpData.py
#   DESCRIPTION:
#       Re organize NYC Open data NYC leading causes of death by
#       leading causes through the years regardless of age,
#       race_ethnicity and sex and loop through scatter plots to
#       visualize trends
#   Data Source:
#       data.cityofnewyork.us
#-----------------------------------------------------------------------
#   CREATED BY: Deborah Perez
#   VERSION:    20180718
########################################################################
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
#-----------------------------------------------------------------------
# Create list of dictionaries
response = json.loads(requests.get("https://data.cityofnewyork.us/resource/uvxr-2jwn.json").text)
#-----------------------------------------------------------------------
# ---clean_up_data------------------------------------------------------
# Finds all empty data for deaths in raw data set and removes those
# records
# @param givenKey as string, emptyString as string, list of dictionaries
# @return list of records with valid death entries
# ----------------------------------------------------------------------
def clean_up_data(givenKey, emptyString, listOfDicts):
    cleanedData = []
    dataWithoutDeaths = []
    emptyCount = 0
    listCount = 0
    for dictionary in listOfDicts:
        listCount += 1
        deathValue = dictionary[deaths]
        if deathValue == '.':
            dataWithoutDeaths.append(dictionary)
            emptyCount += 1
        else:
             cleanedData.append(dictionary)
    return cleanedData
#-----------------------------------------------------------------------
# ---sort_causes_by_year------------------------------------------------
# Sorts causes into a list of lists with index 0 as cause, index 1 as
# 2007 data, index 2 as 2008 data, index 3 as 2009 data, index 4 as
# 2010 data, index 5 as 2011 data, index 6 as 2012 data and index 7
# as 2013 data.
# @param cleanData as list of dictionaries
# @return list of lists of causes sorted
# ----------------------------------------------------------------------
def sort_causes_by_year(cleanData):
    count = 0
    leadingCause = 'leading_cause'
    deaths = 'deaths'
    year = 'year'
    sortedCauses = []
    causesList = []
    for data in cleanData:
        count += 1
        cause = data[leadingCause]
        causeYear = data[year]
        causeDeaths = float(data[deaths])
        if cause in causesList:
            for sortedC in sortedCauses:
                if sortedC[0] == cause:
                    for i in range(2007,2014):
                        if causeYear == str(i):
                            index = i-2006
                            sortedC[index] += causeDeaths
        else:
            causesList.append(cause)
            causeListArray = [cause, 0, 0, 0, 0, 0, 0, 0]
            for i in range(2007,2014):
                if causeYear == str(i):
                    index = i-2006
                    causeListArray[index] = causeDeaths
            sortedCauses.append(causeListArray)
    return sortedCauses
#-----------------------------------------------------------------------
def scan_plots(metaData, sortedCauses):
    for cause in sortedCauses:
        x = metaData[1:]
        y = cause[1:]
        colors = (0,0,0)
        area = np.pi*3
        plt.scatter(x, y, s=area, c=colors, alpha=0.5)
        plt.title(cause[0])
        plt.xlabel('year')
        plt.ylabel('deaths')
        plt.show()
#-----------------------------------------------------------------------
# ---MAINCODE-----------------------------------------------------------
deaths = 'deaths'
emptyData = '.'
metaData = ["Leading Cause", 2007, 2008, 2009, 2010, 2011, 2012, 2013]
cleanData = clean_up_data(deaths, emptyData, response)
sortedCauses = sort_causes_by_year(cleanData)
print (scan_plots(metaData, sortedCauses))
