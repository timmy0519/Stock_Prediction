# coding: utf-8

import pandas as pd
import matplotlib as plt
import pathlib
import fastai
import pathlib
import argparse

def gen_train(x,y):
    folder_path = pathlib.Path('./preprocessed')
    filename = x
    file_path = folder_path.joinpath(filename)
    data = pd.read_csv(file_path)

    numeric_features = data.select_dtypes('number').columns
    id_feature = ['Stock_code']
    cat_features = data.select_dtypes(exclude = 'number').columns.drop(['Stock_code'])

    n_filename = y
    n_file_path = folder_path.joinpath(n_filename)
    n_data = pd.read_csv(n_file_path)

    # merged_data = pd.merge(left=data,right=n_data.loc[:,['Stock_code','current price']],how='left',left_on='Stock_code',right_on='Stock_code')
    merged_data = pd.merge(left=data,right=n_data.loc[:,['Stock_code','current_price','sp_average_change']],how='left',left_on='Stock_code',right_on='Stock_code')
## predict actual price change
    # target_var = 'price_change'
    # merged_data[target_var] = merged_data['current price_y'] - merged_data['current price_x']

    # merged_data = merged_data.drop('current price_y',axis=1,errors='ignore')
    # merged_data.rename({'current price_x': 'current_price'},axis=1,inplace=True)

    # merged_data[target_var] = merged_data[target_var].fillna(-merged_data['current_price'])

    # target_var = 'trend'
    # merged_data[target_var] = (merged_data['current price_y'] - merged_data['current price_x'])>0

    # merged_data = merged_data.drop('current price_y',axis=1,errors='ignore')
    # merged_data.rename({'current price_x': 'current_price'},axis=1,inplace=True)

    # merged_data[target_var] = merged_data[target_var].fillna(False)

    target_var = 'trend_sp'
    merged_data['price_change_percentage'] = (merged_data['current_price_y'] - merged_data['current_price_x']) /  merged_data['current_price_x'] *100.
    merged_data['trend_sp'] = (merged_data['price_change_percentage'] > merged_data['sp_average_change_y']) & (merged_data['sp_average_change_y']>0)
    merged_data = merged_data.drop(['current_price_y','sp_average_change_y','sp_average_change_x','price_change_percentage'],axis=1,errors='ignore')
    merged_data.rename({'current_price_x': 'current_price'},axis=1,inplace=True)

    merged_data[target_var] = merged_data[target_var].fillna(False)

    merged_data[target_var] = merged_data[target_var].fillna(False)
    target_folder = pathlib.Path('./').joinpath('train')
    if not target_folder.exists():
        target_folder.mkdir()
    file_path = target_folder.joinpath(filename)

    merged_data.to_csv(file_path.as_posix(),index=False)



if __name__ == '__main__':
    # create parser and handle arguments
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-x",
                        type=str,
                        help="train data")
    PARSER.add_argument("-y",
                        type=str,
                        help="the next month of the train data")
    # parse the arguments
    ARGS = PARSER.parse_args()
    gen_train(ARGS.x,ARGS.y)