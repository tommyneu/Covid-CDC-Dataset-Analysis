# Thomas Neumann
# NCC CSCE364 Spring 2022
# Lab 2 - neumann_thomas_lab2.py
#
# The file will contain a series of python functions that are organized in a menu-driven fashion via the main function.
# We will use them to access data in a CSV file

from os import path, system, name
from shutil import copyfile

# these imports are for matplotlib use only
import time
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def clear():
    '''
    This function when called will clear the terminal
    '''
    system('cls' if name=='nt' else 'clear')


def getFilePath():

    '''
    When this function is called we will ask the user for the file path
    then we will verify the path exists before returning the valid path

    @returns {string} Returns the valid file path
    '''

    # gets the file and validates it is there
    filePath = input('\nPlease enter the path to the file to begin or exit to leave: ')
    while(not path.exists(filePath) and not filePath.upper() == "EXIT"):
        filePath = input('That file path does not exist please enter one that does: ')

    return filePath


def verifyStructure(filePath):

    '''
    Asks the user if their datafile matches the format structure

    @param   {string} file path of the file to verify structure
    @returns {bool} Return True for "YES" and False for "NO"
    '''

    # verifies the file still exists
    if not path.exists(filePath):
        print("\nERROR: Count Not Find File!")
        print("\t{}".format(filePath))
        return False

    # prints out block of text
    print("Your file path is {}".format(filePath))
    print("Please verify that the data structure follows these requirements")
    print("\t1) First row has the name of the dataset")
    print("\t2) Second row has the date when the data was taken")
    print("\t3) Third row has the headers for the columns")
    print("\t4) First column is the state")
    print("\t5) Second column is the date")
    print("\t6) Third column is the cases")
    print("\t7) Fourth column is the 7 day moving average")
    print("\t7) Fifth column is the historic cases")
    fileStructVerification = input("\nDo these all match the data in the filepath? [Y/n]: ").upper()

    # validates the user's input is a valid yes no
    while(not fileStructVerification in ["YES", "NO", "Y", "N"]):
        fileStructVerification = input("Do these all match the data in the filepath? [Y/n]: ").upper()

    if fileStructVerification in "NO":
        print("Please get the correct structured data")

    return fileStructVerification in "YES"


def duplicateFile(filePath, duplicatePath):

    '''
    Asks the user if they want to duplicate the data file
    if yes then we will make a copy / override the old copy
    if no we will not

    @param   {string} file path of the file to copy
    @param   {string} relative file path of the location to copy to
    @returns {string} Return user responce "YES"/"Y" or "NO"/"N"
    '''

    # verifies the file still exists
    if not path.exists(filePath):
        print("\nERROR: Count Not Find File!")
        print("\t{}".format(filePath))
        return "NO"

    # checks if their is already data there
    if path.exists(duplicatePath):

        # if there is we will ask if we want to override it
        overRightDuplicate = input("It looks like you already have duplicate data, would you like to override it [Y/n]: ").upper()
        while(not overRightDuplicate in ["YES", "NO", "Y", "N"]):
            overRightDuplicate = input("It looks like you already have duplicate data, would you like to override it [Y/n]: ").upper()

        # we will stop if they do not want to override it
        if overRightDuplicate in "NO":
            return overRightDuplicate
    else:

        # if their is no duplicate then we will just ask if we can
        duplicateOK = input("We will make a duplicate of the data is that ok? [Y/n]: ").upper()

        while(not duplicateOK in ["YES", "NO", "Y", "N"]):
            duplicateOK = input("We will make a duplicate of the data is that ok? [Y/n]: ").upper()

        if duplicateOK in "NO":
            return duplicateOK


    # if we get here all responces from them were yes/y so we will copy and return "YES"
    copyfile(filePath, duplicatePath)

    return "YES"


def copyTheData(duplicatePath, copiedDataPath):

    '''
    Asks the user if they want to copy the data from the duplicate file
    if yes then we will make a copy / override the old data
    if no we will not

    @param   {string} relative file path of the location of the duplicate data
    @param   {string} relative file path of the location to copy the data to
    @returns {string} Return user responce "YES"/"Y" or "NO"/"N"
    '''

    # verifies the file still exists
    if not path.exists(duplicatePath):
        print("\nERROR: Count Not Find File!")
        print("\t{}".format(duplicatePath))
        return "NO"

    # checks if the raw data file is already there
    if path.exists(copiedDataPath):

        # if it is we will ask to override the data
        overRightData = input("It looks like you already have copied the raw data (not inclding the first three lines), \nwould you like to override it [Y/n]: ").upper()
        while(not overRightData in ["YES", "NO", "Y", "N"]):
            overRightData = input("It looks like you already have copied the raw data (not inclding the first three lines), \nwould you like to override it [Y/n]: ").upper()

        # no we will not override
        if overRightData in "NO":
            return overRightData
    else:

        # if is not there we will ask the user if we can copy the data
        copyOK = input("We will make a copy of the raw data is that ok? (not inclding the first three lines) [Y/n]: ").upper()

        while(not copyOK in ["YES", "NO", "Y", "N"]):
            copyOK = input("We will make a copy of the raw data is that ok? (not inclding the first three lines) [Y/n]: ").upper()

        # if no then we will not copy the data
        if copyOK in "NO":
            return copyOK

    # if we get here all responces from the user were "YES"/"Y" so we will copy
    copyfile(duplicatePath, copiedDataPath)

    # we are removing the first three lines from the duplicated files
    with open(copiedDataPath, 'r') as fileIn:
        dataToBeStripped = fileIn.read().splitlines(True)
    with open(copiedDataPath, 'w') as fileOut:
        fileOut.writelines(dataToBeStripped[3:])

    return "YES"


def parseTheData(copiedDataPath):

    '''
    We will let the user know that we are about to extract the data
    Just letting the user know whats happening

    @param   {string} relative file path of the location copied data is at
    @returns {list} Return 2d list of data
    '''

    # verifies the file still exists
    if not path.exists(copiedDataPath):
        print("\nERROR: Count Not Find File!")
        print("\t{}".format(copiedDataPath))
        return []

    # lets the user know since it might be resource intensive
    input("We will extract the data click enter to begin [Enter]: ")

    # loops through the lines of the doc and splits it by comma
    outputData = []
    with open(copiedDataPath, 'r') as fileIn:
        rows = fileIn.read().splitlines()
        for singleRow in rows:
            columns = singleRow.split(",")
            outputData.append(columns)

    return outputData


def printMenu():

    '''
    Prints the menu and gets the selection from the user on which option was selected

    @returns {int/string} Return number 1-11 or exit
    '''

    # prints menu
    print("Hello Welcome to the COVID Data Analysis CLI\n")
    print("Please select an action to preform from the menu below")
    print("\t1)  Re-duplicate the file")
    print("\t2)  Re-copy the data from the original data (data is all rows except rows 1,2,3)")
    print("\t3)  Get the data title")
    print("\t4)  Get the data generation/run-date")
    print("\t5)  Get the column names")
    print("\t6)  Re-extract and Display data from csv file as a list of lists")
    print("\t7)  Get the most recent five days of data")
    print("\t8)  Get the highest number of cases on a single day")
    print("\t9)  Get the highest ten days of cases")
    print("\t10) Get a summary of each month of data provided")
    print("\t11) Get matplot graph")

    # gets the users input and validates it
    optionChosen = input("\nWhich action would you like to take [1-11] or exit to leave: ")
    invalidChoice = True
    while(invalidChoice):

        # if it is a number we will check that it is in the valid range
        if optionChosen.isnumeric():
            if int(optionChosen) > 0 and int(optionChosen) < 12:
                invalidChoice = False

        # if it is not a number we will check if it says exit
        else:
            if optionChosen.upper() == "EXIT":
                invalidChoice = False

        # if it was not a valid choice we will ask and loop again
        if invalidChoice:
            optionChosen = input("Which action would you like to take [1-11] or exit to leave: ")

    # probably should return a int or a string 😭
    return optionChosen


def sortByColumn(columnNumber, dataIn):

    '''
    We will sort the list by the data in the column
    We only really use this for sorting by case number but you never know

    @param   {int} Column to sort by
    @param   {list} Data to sort
    @returns {list} Return sorted data
    '''

    # check if the column is a number and if it is we will sort it as a number
    # but if not we will sort just regular
    if(dataIn[0][columnNumber].isnumeric()):
        return sorted(dataIn, key=lambda x:int(x[columnNumber]), reverse=True)
    return sorted(dataIn, key=lambda x:x[columnNumber], reverse=True)


def getTopRows(numberOfRows, dataIn):

    '''
    We will get the first couple rows of data from the data set

    @param   {int} Number of rows to get
    @param   {list} Data slice
    @returns {list} Return sliced data
    '''

    return dataIn[:numberOfRows]


def printSummaryByDate(dataIn):

    '''
    We collect the data by month and year
    Then we will print the data summary

    @param   {list} Data to summarize
    '''

    # we will create two dictionaries one for the running total for cases
    # the other is the number of data for the average
    caseCounts = dict()
    dayCounts = dict()

    # we will loop through the rows in the data
    # and extract the date column and cases column
    # we will also reformat the date so it is MMM - YYYY format
    for row in dataIn:
        date = row[1]
        cases = int(row[2])
        formattedDate = date[:3] + " - " + date[-4:]

        # if the dictionary does not have a value for MMM - YYYY
        # we will set the default value to 0
        caseCounts.setdefault(formattedDate, 0)
        dayCounts.setdefault(formattedDate, 0)

        # we will then add the data from that row
        caseCounts[formattedDate] += cases
        dayCounts[formattedDate] += 1

    # we will then print a nice table with the data formatted
    print("+" + ("-" * 10) + "+" +("-" * 8) + "+" + ("-" * 10) +"+")
    print("|{:>10}|{:>8}|{:>10}|".format("Month", "Total", "Average")) # heading bit
    print("+" + ("=" * 10) + "+" +("=" * 8) + "+" + ("=" * 10) +"+")
    for month, cases in caseCounts.items():
        print("|{}|{:>8}|{:>10.2f}|".format(month, cases, cases/dayCounts[month])) # actual data bit
    print("+" + ("-" * 10) + "+" +("-" * 8) + "+" + ("-" * 10) +"+")


#   __  __      _
#  |  \/  |__ _(_)_ _
#  | |\/| / _` | | ' \
#  |_|  |_\__,_|_|_||_|

def main():

    # constant values
    duplicatePath = "./duplicate_data.csv"
    copiedDataPath = "./copied_real_data.csv"

    # clearing out anything from before the program is run
    clear()

    # greeting the user
    print("Hello Welcome to the COVID Data Analysis CLI")
    print("Please verify that you have gotten the data file from the CDC website for the most accurate results")

    # getting the file path
    filePath = getFilePath()
    if filePath.upper() == "EXIT":
        return 0
    clear()

    # get the user verification of the data structure
    if not verifyStructure(filePath):
        return 0
    clear()

    # duplicates the file
    duplicated = duplicateFile(filePath, duplicatePath)
    if not duplicated in "YES":
        print("To ensure data safety we will need to make a copy of the data")
        return 0
    clear()

    # Copy the data from the duplicated file
    copiedData = copyTheData(duplicatePath, copiedDataPath)
    if not copiedData in "YES":
        print("To better parse the data we will need to copy the raw data")
        return 0
    clear()

    # Copy the data from the duplicated file
    rawDataAsLists = parseTheData(copiedDataPath)
    if len(rawDataAsLists) == 0:
        print("No data found")
        return 0
    clear()

    # we do everything before the menu because we never want to get to a point
    # we we do not know if the data will be there so we never will have to hide options
    # from the menu

    # gets users action and will keep looping until they want to leave
    option = printMenu()
    while(option.upper() != "EXIT"):
        clear()

        # Re-duplicate the file
        if option == "1":
            duplicateFile(filePath, duplicatePath)

        # Re-copy the data from the original data (data is all rows except rows 1,2,3)
        elif option == "2":
            copyTheData(duplicatePath, copiedDataPath)

        # Get the data title
        elif option == "3":
            with open(duplicatePath, 'r') as fileIn:
                print(fileIn.read().splitlines()[0])

        # Get the data generation/run-date
        elif option == "4":
            with open(duplicatePath, 'r') as fileIn:
                print(fileIn.read().splitlines()[1])

        # Get the column names
        elif option == "5":
            with open(duplicatePath, 'r') as fileIn:
                print(fileIn.read().splitlines()[2].split(","))

        # Re-extract and Display data from csv file as a list of lists
        elif option == "6":
            rawDataAsLists = parseTheData(copiedDataPath)
            for row in rawDataAsLists:
                print("\t{}".format(row))

        # Get the most recent five days of data
        elif option == "7":
            print("Five most recent days of data")
            for row in getTopRows(5, rawDataAsLists):
                print("\t{}".format(row))

        # Get the highest number of cases on a single day
        elif option == "8":
            print("Highest number of cases on a single day")
            for row in getTopRows(1, sortByColumn(2, rawDataAsLists)):
                print("\t{}".format(row))

        # Get the highest ten days of cases
        elif option == "9":
            print("Highest ten days of cases")
            for row in getTopRows(1, sortByColumn(2, rawDataAsLists)):
                print("\t{}".format(row))

        # Get a summary of each month of data provided
        elif option == "10":
            printSummaryByDate(rawDataAsLists)

        # Get matplot graph
        elif option == "11":

            # converts data into unix time
            convertTime = lambda x: time.mktime(datetime.datetime.strptime(x, "%b %d %Y").timetuple())

            # extracts the date column and cases column
            xPoints = [convertTime(row[1]) for row in rawDataAsLists]
            yPoints = [int(row[2]) for row in rawDataAsLists]

            # draws graph
            plt.plot(xPoints, yPoints)
            plt.show()

        # waits for user input before returning back to the menu in case they wanted to look at the stuff
        input("Press enter once you are ready to re-enter the menu [Enter]: ")
        clear()
        option = printMenu()

    return 0


if __name__ == "__main__":
    main()