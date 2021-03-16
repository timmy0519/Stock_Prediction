import pandas as pd
import pathlib
import glob
import os
import re
import argparse
def extract(year,month):
    year = year
    month = month
    streamFolder = 'streamData'
    month_folder = pathlib.Path(streamFolder,'raw',str(year),str(month))
    filename = "streaming.tsv"

    firstDay = min(os.listdir(str(month_folder)),key= lambda x: int(x))
    firstFolder = month_folder.joinpath(str(firstDay))

    lastDay = max(os.listdir(str(month_folder)),key= lambda x: int(x))
    lastFolder = month_folder.joinpath(str(lastDay))

    firstData = pd.read_csv(firstFolder.joinpath(filename),delimiter='\t')

    lastData = pd.read_csv(lastFolder.joinpath(filename),delimiter='\t')

    f_gspc = firstData[firstData.SYMB.str.match(r'(\^GSPC.*)')==True]

    l_gspc =  lastData[lastData.SYMB.str.match(r'(\^GSPC.*)')==True]

    if  not re.match("^\d{2}:\d{2}$",l_gspc.iloc[-1].TIME):
        l_gspc.drop(-1,inplace=True)

    filtered = pd.DataFrame([f_gspc.iloc[0], l_gspc.iloc[-1]])

    filtered.to_csv(streamFolder+'/filtered/'+str(year)+'-'+str(month)+'.csv')

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-y",
                        type=int,
                        help="year")
    PARSER.add_argument("-m",
                        type=int,
                        help="month")
    # parse the arguments
    ARGS = PARSER.parse_args()
    extract(ARGS.y, ARGS.m)