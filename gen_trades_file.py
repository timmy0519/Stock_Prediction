#/usr/bin/python3
import sys
import os
import pathlib
import glob
def firstTradingDay(tradingPeriod):
	firstDayOfMonth = {
		"2001-10" : "-02",
		"2001-11" : "-01",
		"2001-12" : "-04",
		"2006-10" : "-02",
		"2006-11" : "-01",
		"2006-12" : "-01",
		"2011-10" : "-03",
		"2011-11" : "-01",
		"2011-12" : "-01"
	}
	y,m = tradingPeriod.split('-')
	streamFolder = pathlib.Path('streamData/raw',y,m) # current folder

	print(str(streamFolder))
	folder = pathlib.Path('.',y,m) #current folder/year/month
	days = []
	for d in glob.glob(str(streamFolder)+'/*'): # find folder in folder/year/month/*
		print(d)
		days.append(int(d.split('/')[-1]))
	firstDay = min(days)
	lastDay = max(days)
	# return firstDayOfMonth[tradingPeriod]
	return firstDay,lastDay

def lastTradingDay(tradingPeriod):
	lastDayOfMonth = {
		"2001-10" : "-31",
		"2001-11" : "-30",
		"2001-12" : "-31",
		"2006-10" : "-31",
		"2006-11" : "-30",
		"2006-12" : "-29",
		"2011-10" : "-31",
		"2011-11" : "-30",
		"2011-12" : "-30"
	}
	return lastDayOfMonth[tradingPeriod]

def writeBuysToTradesFile(topCompaniesFile, tradingPeriod):
	# Read in topCompanies file line by line
	count = 0
	while True:
		count = count + 1 # count incr
		line = topCompaniesFile.readline() # read one line from file
		# if line is empty, EOF reached
		if not line:
			break
		strippedLine = line.strip().split() # split line by spaces
		# strippedLine should only contain one element of company symbol
		companySymb = strippedLine[0]
		
		# TODO: for now our trading strategy is to buy 100 stocks from
		#	the top companies on opening time on the first day and
		#	sell on closing time on the last day 
		date = tradingPeriod + firstTradingDay(tradingPeriod)
		time = "09:30"
		BorS = "buy"
		ammt = 100

		# print trades to stdout
		print("{} {} {} {} shares of {}".format(date, time, BorS, ammt, companySymb))

def writeSellsToTradesFile(topCompaniesFile, tradingPeriod):
	# Read in topCompanies file line by line
	count = 0
	while True:
		count = count + 1 # count incr
		line = topCompaniesFile.readline() # read one line from file
		# if line is empty, EOF reached
		if not line:
			break
		# parse line from topCompanies
		strippedLine = line.strip().split() # split line by spaces
		# strippedLine should only contain one element of company symbol
		companySymb = strippedLine[0]

		
		# TODO: for now our trading strategy is to buy 100 stocks from
		#	the top companies on opening time on the first day and
		#	sell on closing time on the last day 
		date = tradingPeriod + lastTradingDay(tradingPeriod)
		time = "15:59"
		BorS = "sell"
		ammt = 100

		# print trades to stdout
		print("{} {} {} {} shares of {}".format(date, time, BorS, ammt, companySymb))

# expected arguements:
#     topCompanies - file containing the top k companies as predicted by our model
#     tradingPeriod - trading month in question in the form: /streamData/YYYY/MM/DD/streaming.csv
if __name__ == "__main__":
	# read command line inputs
	if len(sys.argv) == 3:
		topCompanies = sys.argv[1]
		tradingPeriod = sys.argv[2]
	else:
		usage = "expected arguements:\n\ttopCompanies - file containing the top k companies as predicted by our model\n\ttradingPeriod - trading month in question in the form: YYYY-MM"
		print(usage)
	print(firstTradingDay(tradingPeriod))
	#ls
	# currFolderAbsPath = os.getcwd()

	# # open topCompanies file
	# topCompaniesFile = open(topCompanies, "r")

	# # write buy trades for the companies in topCompaniesFile to writeDirectory
	# writeBuysToTradesFile(topCompaniesFile, tradingPeriod)

	# # reopen topCompanies file
	# topCompaniesFile.close()
	# topCompaniesFile = open(topCompanies, "r")

	# # write sell trades for the companies in topCompaniesFile to writeDirectory
	# writeSellsToTradesFile(topCompaniesFile, tradingPeriod)

	# #close file
	# topCompaniesFile.close()
